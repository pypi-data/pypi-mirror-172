import base64
from datetime import datetime
import hashlib
import hmac
from typing import List
import simplejson as json
import requests
from uuid import UUID

from bitronit.models.market import Market
from bitronit.models.tradingpair import TradingPair
from bitronit.models.withdrawconfig import WithdrawConfig
from bitronit.models.network import NetworkConfig
from bitronit.models.asset import Asset
from bitronit.models.cryptoexternaltransaction import CryptoExternalTransaction
from bitronit.models.dailybalance import DailyBalance
from bitronit.models.fiatexternaltransaction import FiatExternalTransaction
from bitronit.models.iban import Iban
from bitronit.models.order import Order
from bitronit.models.ordercreateresponse import OrderCreateResponse
from bitronit.models.restriction import Restriction
from bitronit.models.totalbalance import TotalBalance
from bitronit.models.transaction import Transaction
from bitronit.models.wallet import Wallet
from bitronit.models.walletaddress import WalletAddress
from bitronit.models.apikeyinfo import ApiKeyInfo
from bitronit.models.transactionsummary import TransactionSummary
from bitronit.models.orderbook import Orderbook
from bitronit.utils import json_to_object
from bitronit.exceptions import ClientError, AuthenticationError
from bitronit.wrappers import authentication_required

BASE_URL = "https://bitronit.com/api/v2"

class BitronitClient:

    def __init__(
        self,
        api_key: str = None,
        api_secret: str = None,
        base_url: str = BASE_URL,
        session: requests.Session = None
    ):
        """ 
        Creates a Client Object with given API Keys
        If user specifies both api_key and secret_key, constructor will try to authenticate the user
        by updating session headers and sending a request to Bitronit api with given credentials.
        :param api_key: str, optional, your api key
        :param api_secret: str, optional, your api secret
        """
        self._base_url = base_url
        self._api_key = api_key
        self._api_secret = api_secret
        self._authenticated = False

        if session:
            self._session = session
        else:
            self._session = self._init_session()

        if api_key and api_secret:
            self._authenticate()

    @staticmethod
    def _init_session():
        session = requests.session()
        headers = {"Content-Type": "application/json"}
        session.headers.update(headers)
        return session

    def _create_auth_headers(self, params=None, body=None):
        signature = self._create_signature(params, body)
        headers = {
            "Authorization": "Bearer {}".format(self._api_key),
            "Signature": signature
        }
        return headers

    def _authenticate(self):
        """ 
        Authenticates the Client
        Authenticates the clients by using api_key and api_secret
        Signature is a HMAC-SHA256 encoded message. The HMAC-SHA256 code must be generated using a secret key
        If authentication succeed, updates the session's header. raises AuthenticationError otherwise
        """
        url = "{}/users/api-key/info".format(self._base_url)
        signature = self._create_signature()
        headers = {
            "Authorization": "Bearer {}".format(self._api_key),
            "Signature": signature
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Authentication successful, update session header
            self._authenticated = True
        else:
            raise AuthenticationError(response)
                
    def _create_signature(self, params=None, body=None):
        msg = ""
        if params:
            total_params = len(params)
            count = 0
            for param in params:
                msg += param + "=" + str(params[param])
                count += 1
                if count < total_params:
                    msg += "&"           
        if body:
            msg += body
        msg = msg.encode('ASCII')
        api_secret = self._api_secret.encode('ASCII')
        signature = hmac.new(api_secret, msg, hashlib.sha256).digest()
        signature = base64.b64encode(signature)
        return signature.decode("utf-8")

    def _request(self, method, path, params=None, body=None, auth=False):
        url = "{}/{}".format(self._base_url, path)
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        if body:
            body = {k: v for k, v in body.items() if v is not None}
            body = json.dumps(body)
        auth_headers = None
        if auth:
            auth_headers = self._create_auth_headers(params, body)
        response = self._session.request(method, url, params, data=body, headers=auth_headers)
        if not response.ok:
            status = response.status_code
            if status // 100 == 4:
                raise ClientError(response)
        try: return response.json()
        except: pass

    def get_assets(self):
        """ 
        Get list of all assets.
        :return: List of Asset instance
        """
        path = "assets"
        response_list = self._request("get", path)
        asset_list: List[Asset] = []
        for item in response_list:
            asset_list.append(json_to_object(item, Asset()))
        return asset_list

    def get_asset(self, asset: str):
        """
        Get detail of an Asset.
        :param asset: str, required, Symbol(Ticker) of the asset
        :return: Asset instance
        """
        path = "assets/{}".format(asset)
        response_data = self._request("get", path)
        return json_to_object(response_data, Asset())

    def get_networks(self, asset: str = None):
        """ 
        Get list of network configurations.
        :param asset: str, optional, Symbol(Ticker) of the asset
        :return: List of NetworkConfig instance
        """
        path = "crypto-network"
        params = {"asset": asset}
        response_list = self._request("get", path, params)
        network_list: List[NetworkConfig] = []
        for item in response_list:
            network_list.append(json_to_object(item, NetworkConfig()))
        return network_list

    def get_crypto_withdraw_config(self, asset: str, network: str):
        """ 
        Get withdraw configuration for a crypto asset and network.
        :param asset: str, required, Symbol(Ticker) of the asset
        :param network: str, required, Network symbol
        :return: WithdrawConfig instance
        """
        path = "assets/{}/network/{}/crypto-withdraw-config".format(asset, network)
        response_data = self._request("get", path)
        return json_to_object(response_data, WithdrawConfig())

    def get_fiat_withdraw_config(self, asset: str):
        """ 
        Get withdraw configuration for a fiat asset.
        :param asset: str, required, Symbol(Ticker) of the asset
        :return: WithdrawConfig instance
    
        """
        path = "assets/{}/fiat-withdraw-config".format(asset)
        response_data = self._request("get", path)
        return json_to_object(response_data, WithdrawConfig())

    def get_candlesticks(
        self,
        base_asset: str,
        quote_asset: str,
        period: int,
        start_timestamp: int = None,
        end_timestamp: int = None,
        limit: int = None
    ) -> List[list] :
        """ 
        Get candlestick data for the pair.
        :param base_asset: str, required, Symbol(Ticker) of the base asset
        :param quote_asset: str, required, Symbol(Ticker) of the quote asset
        :param period: int, required, Period of the candlestick in minutes
        :param start_timestamp: int, optional, Timestamp
        :param end_timestamp: int, optional, Timestamp
        :param limit: int, optional, Maximum number of items [1-500] Default: 500
        :return: List of candlestick data lists
        [
            [opentime, open, high, low, close, volume],
            [Timestamp, BigDecimal, BigDecimal, BigDecimal, BigDecimal, BigDecimal],
            [1659529500000, 1671.78, 1671.78, 1671.78, 1671.780, 10.114269],
            ...
        ]
        """
        path = "candlesticks"
        params = {
            "baseAsset": base_asset,
            "quoteAsset": quote_asset,
            "period": period,
            "starTime": start_timestamp,
            "endTime": end_timestamp,
            "limit": limit
        }
        return self._request("get", path, params)

    def get_markets(self):
        """ 
        Get market info for all pairs
        :return: List of Market instance
        """
        path = "markets"
        response_list = self._request("get", path)
        market_list: List[Market] = []
        for item in response_list:
            market_list.append(json_to_object(item, Market()))
        return market_list


    def get_orderbook(self, base_asset: str, quote_asset: str, scale: int):
        """ 
        Get orderbook data for the given trading pair and scale
        :param base_asset: str, required, Symbol(Ticker) of the base asset
        :param quote_asset: str, required, Symbol(Ticker) of the quote asset
        :param scale: int, required
        :return: Orderbook instance
        """
        path = "orders/group"
        params = {
            "baseAsset": base_asset,
            "quoteAsset": quote_asset,
            "scale": scale
        }
        response_data = self._request("get", path, params)
        return json_to_object(response_data, Orderbook())

    def get_transactions(
        self,
        base_asset: str = None,
        quote_asset: str = None,
        page: int = None,
        size: int = None
    ):
        """ 
        Get all transactions paginated
        :param base_asset: str, optional, Symbol(Ticker) of the base asset
        :param quote_asset: str, optional, Symbol(Ticker) of the quote asset
        :param page: int, optional, Page number
        :param size: int, optional, Number of items per page [1-50] Default: 20
        :return: List of TransactionSummary instance
        """
        path = "transactions"
        params = {
            "baseAsset": base_asset,
            "quoteAsset": quote_asset,
            "page": page,
            "size": size
        }
        response_list = self._request("get", path, params)
        transaction_list: List[TransactionSummary] = []
        for item in response_list:
            transaction_list.append(json_to_object(item, TransactionSummary))
        return transaction_list

    def get_trading_pairs(self):
        """ 
        Get all trading pair details
        :return: List of TradingPair instance
        """
        path = "trading-pairs"
        response_list = self._request("get", path)
        trading_pair_list: List[TradingPair] = []
        for item in response_list:
            trading_pair_list.append(json_to_object(item, TradingPair()))
        return trading_pair_list

    def get_trading_pair(
        self,
        base_asset: str,
        quote_asset: str
    ):
        """ 
        Get trading pair detail
        :param base_asset: str, required, Symbol(Ticker) of the base asset
        :param quote_asset: str, required, Symbol(Ticker) of the quote asset
        :return: TradingPair instance
        """
        path = "trading-pairs/base-asset/{}/quote-asset/{}".format(base_asset, quote_asset)
        response_data = self._request("get", path)
        return json_to_object(response_data, TradingPair())

    @authentication_required
    def get_api_key_info(self):
        """ 
        Get userId and scope permissons of the api key (Authentication Required)
        :return: ApiKeyInfo instance
        """
        url = "users/me/api-key/info"
        response_data = self._request("get", url, auth=True)
        return json_to_object(response_data, ApiKeyInfo())

    @authentication_required
    def get_crypto_deposit_history(
        self,
        asset: str = None,
        page: int = None,
        size: int = None
    ):
        """ 
        Get crypto assets deposit history (Authentication Required)
        :param asset: str, optional, Symbol(Ticker) of the asset
        :param page: int, optional, Page number
        :param size: int, optional, Number of items per page
        :return: List of CryptoExternalTransaction instance
        """
        path = "users/me/deposits/crypto"
        params = {
            "asset": asset,
            "page": page,
            "size": size
        }
        response_list = self._request("get", path, params, auth=True)
        crypto_external_transaction_list: List[CryptoExternalTransaction] = []
        for item in response_list:
            crypto_external_transaction_list.append(json_to_object(item, CryptoExternalTransaction()))
        return crypto_external_transaction_list

    @authentication_required
    def get_fiat_deposit_history(
        self,
        asset: str = None,
        page: int = None,
        size: int = None
    ):
        """ 
        Get fiat assets deposit history (Authentication Required)
        :param asset: str, optional, Symbol(Ticker) of the asset
        :param page: int, optional, Page number
        :param size: int, optional, Number of items per page
        :return: List of FiatExternalTransaction instance
        """
        path = "users/me/deposits/fiat"
        params = {
            "asset": asset,
            "page": page,
            "size": size
        }
        response_list = self._request("get", path, params, auth=True)
        fiat_external_transaction_list: List[FiatExternalTransaction] = []
        for item in response_list:
            fiat_external_transaction_list.append(json_to_object(item, FiatExternalTransaction()))
        return fiat_external_transaction_list

    @authentication_required
    def get_crypto_withdraw_history(
        self,
        asset: str = None,
        page: int = None,
        size: int = None
    ):
        """ 
        Get crypto assets deposit history (Authentication Required)
        :param asset: str, optional, Symbol(Ticker) of the asset
        :param page: int, optional, Page number
        :param size: int, optional, Number of items per page
        :return: List of CryptoExternalTransaction instance
        """
        path = "users/me/withdrawals/crypto"
        params = {
            "asset": asset,
            "page": page,
            "size": size
        }
        response_list = self._request("get", path, params, auth=True)
        crypto_external_transaction_list: List[CryptoExternalTransaction] = []
        for item in response_list:
            crypto_external_transaction_list.append(json_to_object(item, CryptoExternalTransaction()))
        return crypto_external_transaction_list

    @authentication_required
    def get_fiat_withdraw_history(
        self,
        asset: str = None,
        page: int = None,
        size: int = None
    ):
        """ 
        Get fiat assets withdraw history paginated (Authentication Required)
        :param asset: str, optional, Symbol(Ticker) of the asset
        :param page: int, optional, Page number
        :param size: int, optional, Number of items per page
        :return: List of FiatExternalTransaction instance
        """
        path = "users/me/withdrawals/fiat"
        params = {
            "asset": asset,
            "page": page,
            "size": size
        }
        response_list = self._request("get", path, params, auth=True)
        fiat_external_transaction_list: List[FiatExternalTransaction] = []
        for item in response_list:
            fiat_external_transaction_list.append(json_to_object(item, FiatExternalTransaction()))
        return fiat_external_transaction_list

    @authentication_required
    def initiate_crypto_withdraw(
        self,
        asset: str,
        amount: float,
        target_address: str,
        uuid: UUID,
        network: str,
        fee: float
    ):
        """ 
        Initiate crypto asset withdraw (Authentication Required)
        :param asset: str, required, Symbol(Ticker) of the asset
        :param amount: float, required, amount of the asset to withdraw
        :param target_address: str, required, Address you want to withdraw
        :param uuid: UUID, required, Create using uuid.uuid4()
        :param network: str, required, Network symbol
        :param fee: float, required, withdraw fee for the asset that can be aquired from get_networks endpoint
        :return: CryptoExternalTransaction instance
        """
        path = "users/me/withdrawals/crypto"
        body = {
            "asset": asset,
            "amount": amount,
            "targetAddress": target_address,
            "uuid": str(uuid),
            "network": network,
            "withdrawCryptoFee": fee
        }
        response_data = self._request("post", path, body=body, auth=True)
        return json_to_object(response_data, CryptoExternalTransaction())

    @authentication_required
    def initiate_fiat_withdraw(
        self,
        asset: str,
        amount: float,
        uuid : UUID,
        iban: str
    ):
        """ 
        Initiate fiat asset withdraw (Authentication Required)
        :param asset: str, required, Symbol(Ticker) of the asset
        :param amount: float, required, amount of the asset to withdraw
        :param uuid: UUID, required, Create using uuid.uuid4()
        :param iban: str, required, IBAN receiving whitelisted iban
        :return: FiatExternalTransaction instance
        """
        path = "users/me/withdrawals/fiat"
        params = {
            "asset": asset,
            "amount": amount,
            "iban": iban,
            "uuid": uuid
        }
        response_data = self._request("post", path, params, auth=True)
        return json_to_object(response_data, FiatExternalTransaction())

    @authentication_required
    def cancel_fiat_withdraw(self, uuid: UUID):
        """ 
        Cancel fiat withdraw (Authentication Required)
        :param uuid: UUID, required, UUID of the fiat withdraw transaction
        """
        path = "users/withdrawals/fiat/{}/cancel".format(str(uuid))
        return self._request("post", path, auth=True)
    
    @authentication_required
    def get_ibans(self):
        """ 
        Get user ibans (Authentication Required)
        :return: List of Iban instance
        """
        path = "users/me/ibans"
        response_list = self._request("get", path, auth=True)
        iban_list: List[Iban] = []
        for item in response_list:
            iban_list.append(json_to_object(item, Iban()))
        return iban_list


    @authentication_required
    def get_open_orders(
        self,
        base_asset: str = None,
        quote_asset: str = None,
        order_type: str = None,
        after: datetime = None,
        before: datetime = None,
        page: int = None,
        size: int = None
    ):
        """ 
        Get open orders paginated (Authentication Required)
        :param base_asset: str, optional, Symbol(Ticker) of the base asset
        :param quote_asset: str, optional, Symbol(Ticker) of the quote asset
        :param order_type: str, optional, (Market, Limit, StopLimit, FillOrKill, ImmediateOrCancel)
        :param after: datetime, optional, get orders after this date
        :param before: datetime, optional, get orders before this date
        :param page: int, optional, Page number
        :param size: int, optional, Number of items per page
        :return: List of Order instance
        """
        path = "users/me/orders/open"
        if after: after = after.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        if before: before = before.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        params = {
            "baseAsset": base_asset,
            "quoteAsset": quote_asset,
            "orderType": order_type,
            "after": after,
            "before": before,
            "page": page,
            "size": size
        }   
        response_list = self._request("get", path, params, auth=True)
        order_list: List[Order] = []
        for item in response_list:
            order_list.append(json_to_object(item, Order()))
        return order_list

    @authentication_required
    def get_orders_history(
        self,
        base_asset: str = None,
        quote_asset: str = None,
        order_type: str = None,
        after: datetime = None,
        before: datetime = None,
        page: int = None,
        size: int = None
    ):
        """ 
        Get orders history paginated (Authentication Required)
        :param base_asset: str, optional, Symbol(Ticker) of the base asset
        :param quote_asset: str, optional, Symbol(Ticker) of the quote asset
        :param order_type: str, optional, (Market, Limit, StopLimit, FillOrKill, ImmediateOrCancel)
        :param after: datetime, optional, get orders after this date
        :param before: datetime, optional, get orders before this date
        :param page: int, optional, Page number
        :param size: int, optional, Number of items per page
        :return: List of Order instance
        """
        path = "users/me/orders/history"
        if after: after = after.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        if before: before = before.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        params = {
            "baseAsset": base_asset,
            "quoteAsset": quote_asset,
            "orderType": order_type,
            "after": after,
            "before": before,
            "page": page,
            "size": size
        }   
        response_list = self._request("get", path, params, auth=True)
        order_list: List[Order] = []
        for item in response_list:
            order_list.append(json_to_object(item, Order()))
        return order_list

    @authentication_required
    def get_order(self, uuid: UUID):
        """ 
        Get order by uuid (Authentication Required)
        :param uuid: str,required, Symbol(Ticker) of the base asset
        :return: Order instance
        """
        path = "users/me/orders/{}".format(str(uuid))
        response_data = self._request("get", path, auth=True)
        return json_to_object(response_data, Order())

    @authentication_required
    def create_order(
        self,
        base_asset: str,
        quote_asset: str,
        order_type: str,
        operation_direction: str,
        quantity: float,
        uuid: UUID,
        limit: float = None,
        stop_limit: float = None
    ):
        """ 
        Create an order (Authentication Required)
        :param base_asset: str, required, Symbol(Ticker) of the base asset
        :param quote_asset: str, required, Symbol(Ticker) of the quote asset
        :param order_type: str, required, (Market, Limit, StopLimit, FillOrKill, ImmediateOrCancel)
        :param operation_direction: str, required, (Sell, Buy)
        :param quantity: float, required, Order asset quantity
        :param uuid: str, required, Create using uuid.uuid4()
        :param limit: float, optional, Limit value for Limit orders
        :param stop_limit: float, optional, Stop limit value for StopLimit
        :return: OrderCreateResponse instance
        """
        path = "users/me/orders"
        body = {
            "baseAsset": base_asset,
            "quoteAsset": quote_asset,
            "orderType": order_type,
            "operationDirection": operation_direction,
            "quantity": quantity,
            "uuid": str(uuid),
            "limit": limit,
            "stopLimit": stop_limit
        }
        response_data = self._request("put", path, body=body, auth=True)
        return json_to_object(response_data, OrderCreateResponse())

    @authentication_required
    def cancel_orders(
        self,
        base_asset: str = None,
        quote_asset: str = None,
        operation_direction: str = None,
        price_below: float = None,
        price_above: float = None
    ):
        """ 
        Cancel orders (Authentication Required)
        :param base_asset: str, optional, Symbol(Ticker) of the base asset
        :param quote_asset: str, optional, Symbol(Ticker) of the quote asset
        :param operation_direction: str, optional, (Sell, Buy)
        :param price_below: float, optional, Cancel orders with price below
        :param price_above: float, optional, Cancel orders with price above
        """
        path = "users/me/orders/cancel"
        body = {
            "baseAsset": base_asset,
            "quoteAsset": quote_asset,
            "operationDirection": operation_direction,
            "priceBelow": price_below,
            "priceAbove": price_above
        }
        return self._request("post", path, body=body, auth=True)
    
    @authentication_required
    def cancel_order(self, uuid: UUID):
        """ 
        Cancel orders (Authentication Required)
        :param uuid: UUID, optional, Order uuid
        """
        path = "users/me/orders/{}/cancel".format(uuid)
        return self._request("post", path, auth=True)


    @authentication_required
    def get_restrictions(self, asset: str, type: str):
        """ 
        Get deposit & withdraw restrictions (Authentication Required)
        :param asset: str, required, Symbol(Ticker) of the asset
        :param type: str, required, (Withdraw, Deposit)
        :return: Restriction instance
        """
        path = "users/me/restrictions"
        params = {
            "asset": asset,
            "type": type 
        }
        response_data = self._request("get", path, params, auth=True)
        return json_to_object(response_data, Restriction())

    @authentication_required
    def get_user_transactions(
        self,
        base_asset: str = None,
        quote_asset: str = None,
        operation_direction: str = None,
        order_uuid: UUID = None,
        after: datetime = None,
        before: datetime  = None,
        page: int = None,
        size: int = None
    ):
        """ 
        Get user transactions (Authentication Required)
        :param base_asset: str, optional, Symbol(Ticker) of the base asset
        :param quote_asset: str, optional, Symbol(Ticker) of the quote asset
        :param operation_direction: str, optional, (Sell, Buy)
        :param order_uuid: str, optional, UUID of the order
        :param after: datetime, optional, get transactions after this date
        :param before: datetime, optional, get transactions before this date
        :param page: int, optional, Page number
        :param size: int, optional, Number of items per page
        :return: List of Transaction instance
        """
        path = "users/me/transactions"
        if after: after = after.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        if before: before = before.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        params = {
            "baseAsset": base_asset,
            "quoteAsset": quote_asset,
            "orderDirection": operation_direction,
            "orderUUID": order_uuid,
            "after": after,
            "before": before,
            "page": page,
            "size": size
        }
        response_list = self._request("get", path, params, auth=True)
        transaction_list: List[Transaction] = []
        for item in response_list:
            transaction_list.append(json_to_object(item, Transaction()))
        return transaction_list

    @authentication_required
    def get_daily_total_balance(
        self,
        after: datetime = None,
        before: datetime  = None
    ):
        """ 
        Get daily total balance (Authentication Required)
        :param after: datetime, optional, get items after this date
        :param before: datetime, optional, get items before this date
        :return: List of TotalBalance instance
        """
        path = "users/me/daily/total-balance"
        if after: after = after.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        if before: before = before.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        params = {
            "after": after,
            "before": before
        }
        response_list = self._request("get", path, params, auth=True)
        total_balance_list: List[TotalBalance] = []
        for item in response_list:
            total_balance_list.append(json_to_object(item, TotalBalance))
        return total_balance_list

    @authentication_required
    def get_daily_balances(
        self,
        after: datetime = None,
        before: datetime  = None
    ):
        """ 
        Get daily balances for each asset (Authentication Required)
        :param after: datetime, optional, get items after this date
        :param before: datetime, optional, get items before this date
        :return: List of DailyBalance instance
        """
        path = "users/me/daily/balance"
        if after: after = after.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        if before: before = before.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        params = {
            "after": after,
            "before": before
        }
        response_list = self._request("get", path, params, auth=True)
        daily_balance_list: List[DailyBalance] = []
        for item in response_list:
            daily_balance_list.append(DailyBalance.json_parse(item))
        return daily_balance_list

    @authentication_required
    def get_wallets(self):
        """ 
        Get wallets (Authentication Required)
        :return: List of Wallet instance
        """
        path = "users/me/wallets"
        response_list = self._request("get", path, auth=True)
        wallet_list: List[Wallet] = []
        for item in response_list:
            wallet_list.append(json_to_object(item, Wallet()))
        return wallet_list

    @authentication_required
    def get_wallet(self, asset):
        """ 
        Get wallet (Authentication Required)
        :param asset: str, required, Symbol(Ticker) of the asset
        :return: Wallet instance
        """
        url = "users/me/wallets/{}".format(asset)
        response_data = self._request("get", url, auth=True)
        return json_to_object(response_data, Wallet())

    @authentication_required
    def get_wallet_address(self, asset: str, network: str):
        """ 
        Get or Create deposit address for wallet (Authentication Required)
        :param asset: str, required, Symbol(Ticker) of the asset
        :param network: str, required, Network symbol
        :return: WalletAddress instance
        """
        url = "users/me/wallets/{}/network/{}/address".format(asset, network)
        response_data = self._request("get", url, auth=True)
        return json_to_object(response_data, WalletAddress())

    @authentication_required
    def create_socket_key(self) -> str:
        """ 
        Create a socket key (Authentication Required)
        :return: Socket key string
        """
        url = "users/me/socket/keys"
        response_data = self._request("post", url, auth=True)
        return response_data["key"]

    @authentication_required
    def delete_socket_key(self):
        """ 
        Deletes the socket key (Authentication Required)
        """
        url = "users/me/socket/keys"
        self._request("delete", url, auth=True)
