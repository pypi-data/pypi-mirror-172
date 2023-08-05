import hashlib
import requests
import json
import time
import pandas as pd

from quantplay.utils.constant import Constants
from quantplay.config.qplay_config import QplayConfig
import getpass
from quantplay.broker.generics.broker import Broker
import traceback

class Motilal(Broker):
    user_id = "motilal_user_id"
    api_key = "motilal_api_key"
    password = "password"
    auth_token = "motilal_auth_token"
    two_factor_authentication = "motilal_2FA"

    url = "https://uatopenapi.motilaloswal.com/rest/login/v3/authdirectapi"
    otp_url = "https://uatopenapi.motilaloswal.com/rest/login/v3/resendotp"
    verify_otp_url = "https://uatopenapi.motilaloswal.com/rest/login/v3/verifyotp"
    ltp_utl = "https://uatopenapi.motilaloswal.com/rest/report/v1/getltpdata"
    place_order_url = "https://uatopenapi.motilaloswal.com/rest/trans/v1/placeorder"
    modify_order_url = "https://uatopenapi.motilaloswal.com/rest/trans/v2/modifyorder"
    order_book_url = "https://uatopenapi.motilaloswal.com/rest/book/v1/getorderbook"

    headers = {
        "Accept": "application/json",
        "User-Agent": "MOSL/V.1.1.0",
        "vendorinfo": "EMUM755714",
        "SourceId": "WEB",
        "MacAddress": "00:50:56:BD:F4:0B",
        "ClientLocalIp": "192.168.165.165",
        "ClientPublicIp": "106.193.137.95",
        "osname": "Ubuntu",
        "osversion": "10.0.19041",
        "devicemodel": "AHV",
        "manufacturer": "DELL",
        "productname": "Your Product Name",
        "productversion": "Your Product Version",
        "installedappid": "AppID",
        "browsername": "Chrome",
        "browserversion": "105.0"
    }

    def update_headers(self):
        Constants.logger.info("Updating headers")
        quantplay_config = QplayConfig.get_config()

        auth_token = quantplay_config['DEFAULT'][Motilal.auth_token]
        api_key = quantplay_config['DEFAULT'][Motilal.api_key]
        user_id = quantplay_config['DEFAULT'][Motilal.user_id]

        Motilal.headers['vendorinfo'] = user_id
        Motilal.headers['Authorization'] = auth_token
        Motilal.headers['ApiKey'] = api_key

    def __init__(self):
        self.symbol_scripcode_map = {"NSE": {}, "NSEFO":{}}

        try:
            if not self.validate_config():
                self.generate_token()

            self.update_headers()
            self.get_orders()
        except Exception as e:
            Constants.logger.info(traceback.print_exc())
            self.generate_token()
            self.update_headers()


        self.load_instrument()

        self.order_type_sl = "STOPLOSS"

    def load_instrument(self):
        instrument_file_FO = pd.read_csv("https://openapi.motilaloswal.com/getscripmastercsv?name=NSEFO")
        instrument_file_EQ = pd.read_csv("https://openapi.motilaloswal.com/getscripmastercsv?name=NSE")

        self.symbol_scripcode_map = pd.Series(instrument_file_EQ.scripcode.values,
                                              index=instrument_file_EQ.scripshortname).to_dict()

    def validate_config(self):
        Constants.logger.info("Validating config file")
        quantplay_config = QplayConfig.get_config()

        if quantplay_config is None:
            return False
        if Motilal.api_key not in quantplay_config['DEFAULT']:
            return False
        if Motilal.two_factor_authentication not in quantplay_config["DEFAULT"]:
            return False
        if Motilal.user_id not in quantplay_config["DEFAULT"]:
            return False
        if Motilal.auth_token not in quantplay_config["DEFAULT"]:
            return False

        Constants.logger.info("config validation successful")
        return True

    def configure(self):
        quantplay_config = QplayConfig.get_config()

        print("Enter Motilal userId:")
        user_id = input()

        print("Enter Motilal API key:")
        api_key = input()

        print("Enter Motilal 2FA:")
        two_factor_authentication = input()

        quantplay_config['DEFAULT'][Motilal.api_key] = api_key
        quantplay_config['DEFAULT'][Motilal.user_id] = user_id
        quantplay_config['DEFAULT'][Motilal.two_factor_authentication] = two_factor_authentication

        with open('{}/config'.format(QplayConfig.config_path), 'w') as configfile:
            quantplay_config.write(configfile)

    def generate_token(self):
        if not self.validate_config():
            self.configure()

        quantplay_config = QplayConfig.get_config()
        password = getpass.getpass()

        # initializing string
        str = "{}{}".format(password, quantplay_config['DEFAULT'][Motilal.api_key])
        result = hashlib.sha256(str.encode())

        data = {
            "userid": quantplay_config['DEFAULT'][Motilal.user_id],
            "password": result.hexdigest(),
            "2FA": quantplay_config['DEFAULT'][Motilal.two_factor_authentication]
        }
        Motilal.headers['ApiKey'] = quantplay_config['DEFAULT'][Motilal.api_key]
        response = requests.post(Motilal.url, headers=Motilal.headers, data=json.dumps(data))

        resp_json = response.json()
        Constants.logger.info("login response {}".format(resp_json))
        auth_token = resp_json['AuthToken']

        quantplay_config['DEFAULT'][Motilal.auth_token] = auth_token
        with open('{}/config'.format(QplayConfig.config_path), 'w') as configfile:
            quantplay_config.write(configfile)

        if "isAuthTokenVerified" in resp_json and resp_json['isAuthTokenVerified'] == "FALSE":
            print("Please enter otp")
            self.send_otp()
            otp = input()
            self.verify_otp(otp)

    def send_otp(self):
        response = requests.post(Motilal.otp_url, headers=Motilal.headers)
        Constants.logger.info(response.json())

    def verify_otp(self, otp):
        data = {
            "otp": otp
        }
        response = requests.post(Motilal.verify_otp_url, headers=Motilal.headers, data=json.dumps(data))
        Constants.logger.info(response.json())

    def get_ltp(self, exchange=None, tradingsymbol=None):
        data = {
            "userid": "EMUM755714",
            "exchange": exchange,
            "scripcode": self.symbol_scripcode_map[tradingsymbol]
        }

        response = requests.post(Motilal.ltp_utl, headers=Motilal.headers, data=json.dumps(data))
        Constants.logger.info("Get LTP response {}".format(response.json()))
        return response.json()["data"]["ltp"]/100.0

    def get_orders(self):
        response = (requests.post(Motilal.order_book_url, headers=Motilal.headers)).json()
        if response["status"] == "ERROR":
            Constants.logger.info("Error while fetching order book [{}]".format(response["message"]))
            raise Exception(response["message"])
        orders = response["data"]
        return orders

    def modify_orders_till_complete(self, orders_placed):
        modification_count = {}
        while 1:
            time.sleep(10)
            orders = pd.DataFrame(self.get_orders())
            orders = orders[orders.uniqueorderid.isin(orders_placed)]

            #TODO add complete, cancelled, rejected status here
            orders = orders[~orders.status.isin(["Error"])]

            if len(orders) == 0:
                Constants.logger.info("ALL orders have be completed")
                break

            orders = orders.to_dict('records')
            for order in orders:
                order_id = order['uniqueorderid']

                ltp = self.get_ltp(order['exchange'], order['symbol'])
                order['price'] = ltp
                self.modify_order(order)

                if order_id not in modification_count:
                    modification_count[order_id] = 1
                else:
                    modification_count[order_id] += 1

                time.sleep(.1)

                if modification_count[order_id] > 5:
                    order['ordertype'] = "MARKET"
                    order['price'] = 0
                    Constants.logger.info("Placing MARKET order [{}]".format(order))
                    self.modify_order(order)

    def modify_order(self, order):
        data = {
          "uniqueorderid ": order['uniqueorderid'],
          "newordertype": order['ordertype'],
          "neworderduration": order['orderduration'],
          " newquantityinlot ": order['totalqtyremaining'],
          "newdisclosedquantity": 0,
          "newprice": order['price'],
          "newtriggerprice": order['triggerprice'],
          "qtytradedtoday": order['qtytradedtoday']
        }

        try:
            Constants.logger.info("Modifying order [{}] new price [{}]".format(order['uniqueorderid'], order['price']))
            response = requests.post(Motilal.modify_order_url, headers=Motilal.headers, data=json.dumps(data)).json()
        except Exception as e:
            exception_message = "OrderModificationFailed for {} failed with exception {}".format(order['uniqueorderid'], e)
            Constants.logger.error("{}".format(exception_message))

    def place_order(self, tradingsymbol=None, exchange=None, quantity=None, order_type=None, transaction_type=None,
                    tag=None, product=None, price=None, trigger_price=None):
        data = {
            "exchange": exchange,
            "symboltoken": self.symbol_scripcode_map[tradingsymbol],
            "buyorsell": transaction_type,
            "ordertype": order_type,
            "producttype": product,
            "orderduration": "DAY",
            "price": price,
            "triggerprice": trigger_price,
            "quantityinlot": quantity,
            "disclosedquantity": 0,
            "amoorder": "N",
            "algoid": "",
            "tag": tag
        }
        try:
            Constants.logger.info("Placing order {}".format(json.dumps(data)))
            response = requests.post(Motilal.place_order_url, headers=Motilal.headers, data=json.dumps(data)).json()
            if response['status'] == "ERROR":
                raise Exception(response['message'])
            return response['uniqueorderid']
        except Exception as e:
            exception_message = "Order placement failed with error [{}]".format(str(e))
            print(exception_message)