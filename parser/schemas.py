from json import JSONEncoder
from typing import List, Tuple, Mapping


class StopSchema:
    def __init__(
        self,
        name: str,
        location: Tuple[float],
    ) -> None:
        self.name = name
        self.location = location

    def __str__(self) -> str:
        return f"StopSchema(name={self.name}, location={self.location})"


class RouteSchema:
    def __init__(
        self,
        type: str,
        short_name: str,
        long_name: str,
        direct_stops: List[StopSchema],
        reverse_stops: List[StopSchema],
    ) -> None:
        self.type = type
        self.short_name = short_name
        self.long_name = long_name
        self.direct_stops = direct_stops
        self.reverse_stops = reverse_stops

    def __str__(self) -> str:
        return f"""RouteSchema(
    type={self.type},
    short_name={self.short_name},
    long_name={self.long_name},
    direct_stops={self.direct_stops},
    reverse_stops={self.reverse_stops}
)
"""


class TramRouteSchema(RouteSchema):
    def __init__(
        self,
        short_name: str,
        long_name: str,
        direct_stops: List[StopSchema],
        reverse_stops: List[StopSchema],
    ) -> None:
        super().__init__("tram", short_name, long_name, direct_stops, reverse_stops)


class StopSchemaEncoder(JSONEncoder):
    def default(self, obj) -> Mapping:
        if isinstance(obj, StopSchema):
            return {
                "name": obj.name,
                "location": obj.location,
            }
        return super().default(obj)


class RouteSchemaEncoder(JSONEncoder):
    def default(self, route_schema: RouteSchema) -> Mapping:
        if isinstance(route_schema, RouteSchema):
            encoded_direct_stops = [
                StopSchemaEncoder().default(stop) for stop in route_schema.direct_stops
            ]
            encoded_reverse_stops = [
                StopSchemaEncoder().default(stop) for stop in route_schema.reverse_stops
            ]
            return {
                "type": route_schema.type,
                "short_name": route_schema.short_name,
                "long_name": route_schema.long_name,
                "direct_stops": encoded_direct_stops,
                "reverse_stops": encoded_reverse_stops,
            }
        return super().default(route_schema)
