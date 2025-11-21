from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from threading import Thread
import time


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        print("Connected. Next Order ID:", orderId)

    def error(self, reqId, errorCode, errorString):
        print("IB ERROR", reqId, errorCode, errorString)

    def tickPrice(self, reqId, tickType, price, attrib):
        print("Tick Price:", "Ticker:", reqId, "Type:", tickType, "Price:", price)


def stock_contract(symbol: str):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    return contract


def main():
    app = IBapi()
    print("Connecting to TWS…")
    app.connect("127.0.0.1", 4001, clientId=1)

    # Start socket listener
    api_thread = Thread(target=app.run, daemon=True)
    api_thread.start()

    time.sleep(2)  # wait for connection

    # THIS SYMBOL ALWAYS RETURNS DELAYED DATA IF ENABLED:
    ibkr = stock_contract("IBKR")

    # Request delayed snapshot = True
    app.reqMktData(1, ibkr, "", True, False, [])

    time.sleep(5)  # allow time for response
    app.disconnect()


if __name__ == "__main__":
    main()
