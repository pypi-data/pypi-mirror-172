# This file is generated from the openapi spec
import json
from dataclasses import dataclass, asdict
from typing import List, Optional
import requests
import backoff

HTTP_ERROR_MAX_RETRIES = 20
HTTP_ERROR_MAX_TIME = 30

NETWORK_ERROR_MAX_RETRIES = 10
NETWORK_ERROR_MAX_TIME = 30

TIMEOUT_INTERVALS = (1, 5)


@dataclass
class ApiResult:
    message: str


@dataclass
class ApiError:
    message: str


@dataclass
class Policy:
    filename: Optional[str]
    src: str


@dataclass
class GetPolicyResult:
    policy: Optional[Policy]


@dataclass
class Value:
    type: Optional[str]
    id: Optional[str]


@dataclass
class Fact:
    predicate: str
    args: List[Value]


@dataclass
class Bulk:
    delete: List[Fact]
    tell: List[Fact]


@dataclass
class AuthorizeResult:
    allowed: bool


@dataclass
class AuthorizeQuery:
    actor_type: str
    actor_id: str
    action: str
    resource_type: str
    resource_id: str
    context_facts: List[Fact]


@dataclass
class AuthorizeResourcesResult:
    results: List[Value]


@dataclass
class AuthorizeResourcesQuery:
    actor_type: str
    actor_id: str
    action: str
    resources: List[Value]
    context_facts: List[Fact]


@dataclass
class ListResult:
    results: List[str]


@dataclass
class ListQuery:
    actor_type: str
    actor_id: str
    action: str
    resource_type: str
    context_facts: List[Fact]


@dataclass
class ActionsResult:
    results: List[str]


@dataclass
class ActionsQuery:
    actor_type: str
    actor_id: str
    resource_type: str
    resource_id: str
    context_facts: List[Fact]


@dataclass
class QueryResult:
    results: List[Fact]


@dataclass
class Query:
    fact: Fact
    context_facts: List[Fact]


@dataclass
class StatsResult:
    num_roles: int
    num_relations: int
    num_facts: int


def _fatal_retry_code(exc: Exception) -> bool:
    if isinstance(exc, requests.exceptions.HTTPError):
        # Allow retries on 429 rate-limits and 5xx errors only
        if exc.response.status_code == 429:
            return False
        return 400 <= exc.response.status_code < 500
    else:
        return False


class API:
    def __init__(self, url="https://cloud.osohq.com", api_key=None):
        self.url = url
        self.api_base = "api"
        if api_key:
            self.token = api_key
        else:
            raise ValueError("Must set an api_key")

    def _handle_result(self, result):
        if not result.ok:
            code, text = result.status_code, result.text
            msg = f"Got unexpected error from Oso Service: {code}\n{text}"
            raise Exception(msg)
        try:
            return result.json()
        except json.decoder.JSONDecodeError:
            return result.text

    def _default_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "Oso Cloud (python)",
            "X-OsoApiVersion": "0",
        }

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.ConnectionError, requests.exceptions.Timeout),
        max_time=NETWORK_ERROR_MAX_TIME,
        max_tries=NETWORK_ERROR_MAX_RETRIES,
    )
    @backoff.on_exception(
        backoff.expo,
        requests.exceptions.HTTPError,
        max_time=HTTP_ERROR_MAX_TIME,
        max_tries=HTTP_ERROR_MAX_RETRIES,
        giveup=_fatal_retry_code,
    )
    def _do_post(self, url, params, json):
        return requests.post(
            url,
            params=params,
            json=json,
            headers=self._default_headers(),
            timeout=TIMEOUT_INTERVALS,
        )

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.ConnectionError, requests.exceptions.Timeout),
        max_time=NETWORK_ERROR_MAX_TIME,
        max_tries=NETWORK_ERROR_MAX_RETRIES,
    )
    @backoff.on_exception(
        backoff.expo,
        requests.exceptions.HTTPError,
        max_time=HTTP_ERROR_MAX_TIME,
        max_tries=HTTP_ERROR_MAX_RETRIES,
        giveup=_fatal_retry_code,
    )
    def _do_get(self, url, params, json):
        return requests.get(
            url,
            params=params,
            json=json,
            headers=self._default_headers(),
            timeout=TIMEOUT_INTERVALS,
        )

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.ConnectionError, requests.exceptions.Timeout),
        max_time=NETWORK_ERROR_MAX_TIME,
        max_tries=NETWORK_ERROR_MAX_RETRIES,
    )
    @backoff.on_exception(
        backoff.expo,
        requests.exceptions.HTTPError,
        max_time=HTTP_ERROR_MAX_TIME,
        max_tries=HTTP_ERROR_MAX_RETRIES,
        giveup=_fatal_retry_code,
    )
    def _do_delete(self, url, params, json):
        return requests.delete(
            url,
            params=params,
            json=json,
            headers=self._default_headers(),
            timeout=TIMEOUT_INTERVALS,
        )

    def get_policy(self):
        params = None
        json = None
        result = self._do_get(
            f"{self.url}/{self.api_base}/policy", params=params, json=json
        )
        response = self._handle_result(result)
        return GetPolicyResult(**response)

    def post_policy(self, data):
        params = None
        json = asdict(data)
        result = self._do_post(
            f"{self.url}/{self.api_base}/policy", params=params, json=json
        )
        response = self._handle_result(result)
        return ApiResult(**response)

    def post_facts(self, data):
        params = None
        json = asdict(data)
        result = self._do_post(
            f"{self.url}/{self.api_base}/facts", params=params, json=json
        )
        response = self._handle_result(result)
        return Fact(**response)

    def delete_facts(self, data):
        params = None
        json = asdict(data)
        result = self._do_delete(
            f"{self.url}/{self.api_base}/facts", params=params, json=json
        )
        response = self._handle_result(result)
        return ApiResult(**response)

    def post_bulk_load(self, data):
        params = None
        json = list(map(asdict, data))
        result = self._do_post(
            f"{self.url}/{self.api_base}/bulk_load", params=params, json=json
        )
        response = self._handle_result(result)
        return ApiResult(**response)

    def post_bulk_delete(self, data):
        params = None
        json = list(map(asdict, data))
        result = self._do_post(
            f"{self.url}/{self.api_base}/bulk_delete", params=params, json=json
        )
        response = self._handle_result(result)
        return ApiResult(**response)

    def post_bulk(self, data):
        params = None
        json = asdict(data)
        result = self._do_post(
            f"{self.url}/{self.api_base}/bulk", params=params, json=json
        )
        response = self._handle_result(result)
        return ApiResult(**response)

    def post_authorize(self, data):
        params = None
        json = asdict(data)
        result = self._do_post(
            f"{self.url}/{self.api_base}/authorize", params=params, json=json
        )
        response = self._handle_result(result)
        return AuthorizeResult(**response)

    def post_authorize_resources(self, data):
        params = None
        json = asdict(data)
        result = self._do_post(
            f"{self.url}/{self.api_base}/authorize_resources", params=params, json=json
        )
        response = self._handle_result(result)
        return AuthorizeResourcesResult(**response)

    def post_list(self, data):
        params = None
        json = asdict(data)
        result = self._do_post(
            f"{self.url}/{self.api_base}/list", params=params, json=json
        )
        response = self._handle_result(result)
        return ListResult(**response)

    def post_actions(self, data):
        params = None
        json = asdict(data)
        result = self._do_post(
            f"{self.url}/{self.api_base}/actions", params=params, json=json
        )
        response = self._handle_result(result)
        return ActionsResult(**response)

    def get_stats(self):
        params = None
        json = None
        result = self._do_get(
            f"{self.url}/{self.api_base}/stats", params=params, json=json
        )
        response = self._handle_result(result)
        return StatsResult(**response)

    def clear_data(self):
        params = None
        json = None
        result = self._do_post(
            f"{self.url}/{self.api_base}/clear_data", params=params, json=json
        )
        response = self._handle_result(result)
        return ApiResult(**response)

    # NOTE: the args stuff here doesn not show up in the openapi spec
    # so we don't codegen this correctly
    def get_facts(self, predicate, *args):
        params = {}
        params["predicate"] = predicate
        for i, arg in enumerate(args):
            if arg.type is not None:
                params[f"args.{i}.type"] = arg.type
            if arg.id is not None:
                params[f"args.{i}.id"] = arg.id
        json = None
        result = self._do_get(
            f"{self.url}/{self.api_base}/facts", params=params, json=json
        )
        response = self._handle_result(result)
        result = []
        for item in response:
            result.append(Fact(**item))
        return result

    def post_query(self, data):
        params = None
        json = asdict(data)
        result = self._do_post(
            f"{self.url}/{self.api_base}/query", params=params, json=json
        )
        response = self._handle_result(result)
        # this doesn't get codegen'd properly either
        return QueryResult(
            [
                Fact(fact["predicate"], [Value(**arg) for arg in fact["args"]])
                for fact in response["results"]
            ]
        )
