import time
import uuid
import urllib.parse
from typing import Union, Any, cast, Callable

import requests
import web3.middleware
from eth_typing import URI
from eth_utils import is_hex_address
from requests import Response
from web3 import Web3, HTTPProvider
from web3.types import RPCEndpoint, RPCResponse, TxParams


class EulithAuthException(Exception):
    pass


class EulithRpcException(Exception):
    pass


class ApiToken:
    def __init__(self, token: str, expire: int) -> None:
        self.token = token
        self.expire = expire

    def expires_in_hours(self) -> float:
        now = int(time.time())
        return (self.expire - now) / 3600


def get_api_access_token(eulith_url: URI, eulith_refresh_token: str) -> ApiToken:
    headers = {"Authorization": "Bearer " + eulith_refresh_token, "Content-Type": "application/json"}
    response = requests.get(eulith_url + "/api/access", headers=headers)
    handle_http_response(response)
    json = response.json()
    token = ApiToken(json['token'], json['exp'])
    # print("api token expires in {} hours", token_expires_in_hours())
    return token


def handle_http_response(resp: Response):
    if resp.status_code == 401:
        raise EulithAuthException("Status code: " + str(resp.status_code))
    if resp.status_code != 200:
        raise EulithRpcException("Status code: " + str(resp.status_code))


def handle_rpc_response(resp: RPCResponse):
    if 'error' in resp and resp['error'] != "":
        raise EulithRpcException("RPC Error: " + str(resp['error']))


def add_params_to_url(url: str, params) -> str:
    url_parts = urllib.parse.urlparse(url)
    query = dict(urllib.parse.parse_qsl(url_parts.query))
    query.update(params)

    return url_parts._replace(query=urllib.parse.urlencode(query)).geturl()


class EulithData:
    def __init__(self, eulith_url: Union[URI, str],
                 eulith_refresh_token: str, private: bool) -> None:
        self.eulith_url: URI = URI(eulith_url)
        self.private = private
        self.eulith_refresh_token: str = eulith_refresh_token
        self.atomic: bool = False
        self.tx_id: str = ""
        self.api_access_token: ApiToken = get_api_access_token(self.eulith_url, self.eulith_refresh_token)
        self.http = HTTPProvider(endpoint_uri=eulith_url, request_kwargs={
            'headers': {
                'Authorization': 'Bearer ' + self.api_access_token.token,
                'Content-Type': 'application/json'
            }
        })

    def send_transaction(self, params) -> RPCResponse:
        return self.http.make_request(RPCEndpoint("eth_sendTransaction"), params)

    def start_transaction(self, account: str, gnosis: str):
        self.atomic = True
        self.tx_id = str(uuid.uuid4())
        params = {'auth_address': account, 'atomic_tx_id': 1}  # self.tx_id
        if len(gnosis) > 0:
            params['gnosis_address'] = gnosis
        new_url = add_params_to_url(self.eulith_url, params)
        self.http.endpoint_uri = new_url

    def commit(self) -> TxParams:
        self.atomic = False  # we need to do this even if things fail
        params = {}
        response = self.http.make_request(RPCEndpoint("eulith_commit"), params)
        handle_rpc_response(response)
        self.tx_id = ""
        return cast(TxParams, response['result'])

    def rollback(self):
        self.commit()

    def refresh_api_token(self):
        self.api_access_token: ApiToken = get_api_access_token(self.eulith_url, self.eulith_refresh_token)
        self.http = HTTPProvider(endpoint_uri=self.eulith_url, request_kwargs={
            'headers': {
                'Authorization': 'Bearer ' + self.api_access_token.token,
                'Content-Type': 'application/json'
            }
        })

    def is_close_to_expiry(self) -> bool:
        return self.api_access_token.expires_in_hours() < 6


class EulithWeb3(Web3):
    def __init__(self,
                 eulith_url: Union[URI, str],
                 eulith_refresh_token: str,
                 signing_middle_ware: Any = None,
                 private: bool = False,
                 **kwargs
                 ) -> None:
        self.eulith_data = EulithData(eulith_url, eulith_refresh_token, private)
        http = self._make_http()
        kwargs.update(provider=http)
        super().__init__(**kwargs)
        if signing_middle_ware:
            self.middleware_onion.add(signing_middle_ware)
        self.middleware_onion.add(eulith_atomic_middleware)
        self.middleware_onion.add(web3.middleware.request_parameter_normalizer)
        self.middleware_onion.add(web3.middleware.pythonic_middleware, "eulith_pythonic")
        self.middleware_onion.add(eulith_api_token_middleware)

    def _eulith_send_atomic(self, params) -> RPCResponse:
        return self.eulith_data.send_transaction(params)

    def eulith_start_transaction(self, account: str, gnosis: str = "") -> None:
        if not is_hex_address(account):
            raise TypeError("account must be a hex formatted address")
        if len(gnosis) > 0 and not is_hex_address(gnosis):
            raise TypeError("gnosis must either be blank or a hex formatted address")
        self.eulith_data.start_transaction(account, gnosis)

    def eulith_commit_transaction(self) -> TxParams:
        return self.eulith_data.commit()

    def eulith_rollback_transaction(self):
        self.eulith_data.rollback()

    def eulith_contract_address(self, account: str) -> str:
        if not is_hex_address(account):
            raise TypeError("account must be a hex formatted address")
        params = {}
        response = self.manager.provider.make_request("eulith_get_contracts", params)
        handle_rpc_response(response)
        # print(f'response: {response}')
        contracts = response['result']['contracts']
        # print(f'contracts: {contracts}')
        for c in contracts:
            if c['authorized_address'].lower() == account.lower():
                return c['contract_address']
        return ""

    def eulith_create_contract_if_not_exist(self, account: str) -> str:
        c = self.eulith_contract_address(account)
        if c == "":
            c = self.eulith_create_contract(account)

        return c

    def eulith_create_contract(self, account: str) -> str:
        if not is_hex_address(account):
            raise TypeError("account must be a hex formatted address")
        params = [{'authorized_address': account}]
        response = self.manager.provider.make_request("eulith_new_contract", params)
        handle_rpc_response(response)
        result = response['result']
        self.eth.wait_for_transaction_receipt(result['new_contract_tx_hash'])

        return result['contract_address']

    def eulith_refresh_api_token(self):
        self.eulith_data.refresh_api_token()
        http = self._make_http()
        self.provider = http

    def eulith_refresh_api_token_if_necessary(self):
        if self.eulith_data.is_close_to_expiry():
            self.eulith_refresh_api_token()

    def _make_http(self):
        url = self.eulith_data.eulith_url
        if self.eulith_data.private:
            url = add_params_to_url(url, {'private', 'true'})
        http = HTTPProvider(endpoint_uri=url, request_kwargs={
            'headers': {
                'Authorization': 'Bearer ' + self.eulith_data.api_access_token.token,
                'Content-Type': 'application/json'
            }
        })
        return http


def eulith_atomic_middleware(
        make_request: Callable[[RPCEndpoint, Any], Any], web3: "Web3"
) -> Callable[[RPCEndpoint, Any], RPCResponse]:
    def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
        if method != "eth_sendTransaction" or not web3.eulith_data.atomic:
            return make_request(method, params)

        return cast(EulithWeb3, web3)._eulith_send_atomic(params)

    return middleware


def eulith_api_token_middleware(
        make_request: Callable[[RPCEndpoint, Any], Any], web3: "Web3"
) -> Callable[[RPCEndpoint, Any], RPCResponse]:
    def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
        ew3 = cast(EulithWeb3, web3)
        ew3.eulith_refresh_api_token_if_necessary()

        return make_request(method, params)

    return middleware
