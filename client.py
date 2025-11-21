from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from threading import Thread
import time


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        print("Connected successfully. Next Order ID:", orderId)

    def error(self, reqId, errorCode, errorString):
        print("IB ERROR", reqId, errorCode, errorString)


def main():
    app = IBapi()

    print("Connecting to TWS...")
    app.connect("127.0.0.1", 4001, clientId=1)

    # Start network loop in thread
    thread = Thread(target=app.run, daemon=True)
    thread.start()

    time.sleep(5)  # give time to print messages

    print("Disconnecting...")
    app.disconnect()


if __name__ == "__main__":
    main()
