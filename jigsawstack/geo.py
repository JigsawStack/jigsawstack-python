from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from typing import List, Union
from ._config import ClientConfig


class BaseResponse:
    success: bool


class GeoParams(TypedDict):
    search_value: str
    lat: str
    lng: str
    country_code: str
    proximity_lat: str
    proximity_lng: str
    types: str
    city_code: str
    state_code: str
    limit: int


class GeoSearchParams(TypedDict):
    search_value: str
    country_code: NotRequired[str] = None
    proximity_lat: NotRequired[str] = None
    proximity_lng: NotRequired[str] = None
    types: NotRequired[str] = None


class Geoloc(TypedDict):
    type: str
    coordinates: List[float]


class Region(TypedDict):
    name: str
    region_code: str
    region_code_full: str


class Country(TypedDict):
    name: str
    country_code: str
    country_code_alpha_3: str


class GeoSearchResult(TypedDict):
    type: str
    full_address: str
    name: str
    place_formatted: str
    postcode: str
    place: str
    region: Region
    country: Country
    language: str
    geoloc: Geoloc
    poi_category: List[str]
    additional_properties: Dict[str, any]


class CityResult(TypedDict):
    state_code: str
    name: str
    city_code: str
    state: "StateResult"


class CountryResult(TypedDict):
    country_code: str
    name: str
    iso2: str
    iso3: str
    capital: str
    phone_code: str
    region: str
    subregion: str
    currency_code: str
    geoloc: Geoloc
    currency_name: str
    currency_symbol: str
    tld: str
    native: str
    emoji: str
    emojiU: str
    latitude: float
    longitude: float


class StateResult(TypedDict):
    state_code: str
    name: str
    country_code: str
    country: CountryResult


class GeoSearchResponse(BaseResponse):
    data: List[GeoSearchResult]


class GeocodeParams(TypedDict):
    search_value: str
    lat: str
    lng: str
    country_code: str
    proximity_lat: str
    proximity_lng: str
    types: str
    limit: int


class GeoCityParams(TypedDict):
    country_code: str
    city_code: str
    state_code: str
    search_value: str
    lat: str
    lng: str
    limit: int


class GeoCityResponse(BaseResponse):
    city: List[CityResult]


class GeoCountryParams(TypedDict):
    country_code: str
    city_code: str
    search_value: str
    lat: str
    lng: str
    limit: int
    currency_code: str


class GeoCountryResponse(BaseResponse):
    country: List[CountryResult]


class GeoStateParams(TypedDict):
    country_code: str
    state_code: str
    search_value: str
    lat: str
    lng: str
    limit: int


class GeoStateResponse(BaseResponse):
    state: List[StateResult]


class GeoDistanceParams(TypedDict):
    unit: NotRequired[str] = None  # "K" or "N"
    lat1: str
    lng1: str
    lat2: str
    lng2: str


class GeoDistanceResponse(BaseResponse):
    distance: float


class GeoTimezoneParams(TypedDict):
    lat: str
    lng: str
    city_code: NotRequired[str] = None
    country_code: NotRequired[str] = None


class GeoTimezoneResponse(BaseResponse):
    timezone: Dict[str, any]


class GeohashParams(TypedDict):
    lat: str
    lng: str
    precision: int


class GeohashResponse(BaseResponse):
    geohash: str


class GeohashDecodeResponse(BaseResponse):
    latitude: float
    longitude: float


class Geo(ClientConfig):

    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        api_url: str,
        disable_request_logging: Union[bool, None] = False,
    ):
        super().__init__(api_key, api_url, disable_request_logging)
        self.config = RequestConfig(
            api_url=api_url,
            api_key=api_key,
            disable_request_logging=disable_request_logging,
        )

    def search(self, params: GeoSearchParams) -> GeoSearchResponse:
        path = "/geo/search"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="get",
        ).perform_with_content()
        return resp

    def geocode(self, params: GeocodeParams) -> GeohashDecodeResponse:
        path = "/geo/geocode"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="get",
        ).perform_with_content()
        return resp

    def city(self, params: GeoCityParams) -> GeoCityResponse:
        path = "/geo/city"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="get",
        ).perform_with_content()
        return resp

    def country(self, params: GeoCountryParams) -> GeoCountryResponse:
        path = "/geo/country"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="get",
        ).perform_with_content()
        return resp

    def state(self, params: GeoStateParams) -> GeoStateResponse:
        path = "/geo/state"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="get",
        ).perform_with_content()
        return resp

    def distance(self, params: GeoDistanceParams) -> GeoDistanceResponse:
        path = "/geo/distance"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="get",
        ).perform_with_content()
        return resp

    def timezone(self, params: GeoTimezoneParams) -> GeoTimezoneResponse:
        path = "/geo/timezone"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="get",
        ).perform_with_content()
        return resp

    def geohash(self, params: GeohashParams) -> GeohashResponse:
        path = "/geo/geohash"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="get",
        ).perform_with_content()
        return resp

    def geohash(self, key: str) -> GeohashDecodeResponse:
        path = f"/geo/geohash/decode/{key}"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params={}),
            verb="get",
        ).perform_with_content()
        return resp
