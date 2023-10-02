import asyncio
import aiohttp
import json
from typing import List, Mapping, Tuple

from schemas import StopSchema, TramRouteSchema, RouteSchemaEncoder


API_URL = "https://api.lad.lviv.ua/"
URL_PATH = "routes/static/"
DATA_PATH = "./data/"


def build_url(tram_code: str) -> str:
    return API_URL + URL_PATH + tram_code


def read_tram_codes() -> Tuple[str]:
    with open(DATA_PATH + "tram_numbers.json", "r") as f:
        data = json.load(f)
        return tuple(number["number"] for number in data["numbers"])  # type: ignore


async def fetch_tram_info(tram_code: str) -> Mapping:
    async with aiohttp.ClientSession() as session:
        async with session.get(build_url(tram_code)) as response:
            print("Status:", response.status)
            return await response.json()


async def parse_tram_info(data: Mapping) -> TramRouteSchema:
    async def parse_stops_at(index: int) -> List[StopSchema]:
        return [
            StopSchema(
                stop["name"],
                (stop["loc"][0], stop["loc"][1]),  # type: ignore
            )
            for stop in data["stops"][index]
        ]

    stops = await asyncio.gather(
        parse_stops_at(0),
        parse_stops_at(1),
    )

    short_name = data["route_short_name"]
    long_name = data["route_long_name"]

    return TramRouteSchema(short_name, long_name, stops[1], stops[0])


async def get_tram_info(tram_code: str) -> TramRouteSchema:
    info = await fetch_tram_info(tram_code)
    return await parse_tram_info(info)


def tram_info_to_file(path: str, tram_route_schema: TramRouteSchema) -> None:
    with open(path, "w", encoding="UTF-8") as f:
        json.dump(
            tram_route_schema, f, cls=RouteSchemaEncoder, indent=4, ensure_ascii=False
        )


async def main():
    codes = read_tram_codes()
    trams_info = await asyncio.gather(
        *(get_tram_info(code) for code in codes),
    )

    for tram_info in trams_info:
        tram_info_to_file(DATA_PATH + f"{tram_info.short_name}.json", tram_info)


if __name__ == "__main__":
    asyncio.run(main())
