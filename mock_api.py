from flask import Flask, Response, stream_with_context
import time
import uuid
import random

APP = Flask(__name__)

@APP.route("/very_large_request/<int:rowcount>", methods=["GET"])
def get_large_request(rowcount):
    """returns N rows of data"""
    def f():
        """generates mock data"""
        for _ in range(rowcount):
            time.sleep(0.01)
            txid = uuid.uuid4()
            print(txid)
            uid = uuid.uuid4()
            amount = round(random.uniform(-1000,1000), 2)
            yield f"('{txid}','{uid}','{amount}')\n"
    return Response(stream_with_context(f()))

if __name__ == "__main__":
    APP.run(debug=True)