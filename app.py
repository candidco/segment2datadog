import hmac
import hashlib
import os
from flask import Flask, jsonify, request, abort
from datadog import initialize, statsd

# get keys from environment variables
GIT_SHA = os.environ.get("GIT_SHA")
SEGMENT_SHARED_SECRET = os.environ.get("SEGMENT_SHARED_SECRET", "")
SIGNATURE_DISABLED = os.environ.get("SIGNATURE_DISABLED", True)

# initialize datadog
options = {"statsd_host": os.environ.get("DATADOG_STATSD_HOST", "127.0.0.1")}

initialize(**options)

app = Flask(__name__)

ALLOWED_EVENTS = ["track"]


def emit(source, event, event_type):
    """Emits metric to datadog. Returns nothing."""
    if event_type in ALLOWED_EVENTS:
        statsd.increment(
            "segment.event",
            tags=[
                "source:" + source,
                "event:" + "-".join(event.split()),
                "type:" + event_type,
            ],
        )


def check_signature(signature, data):
    """Verifies signature (ensures matched shared secrets). Returns Bool."""
    if SIGNATURE_DISABLED:
        return True

    # check signature
    try:
        digest = hmac.new(
            SEGMENT_SHARED_SECRET.encode(), msg=data, digestmod=hashlib.sha1
        ).hexdigest()
        if digest == signature:
            return True
        else:
            print(f"Invalid signature. Expected {digest} but got {signature}")
    except KeyError:
        pass

    return False


@app.route("/")
def index():
    """Returns healthcheck."""
    print(f"Received request on /. {GIT_SHA}")
    return f"Segment2Datadog is up and running! {GIT_SHA}"


@app.route("/api/<string:source>", methods=["POST"])
def segment2datadog(source):
    """Main function. Accepts JSON payload on POST only."""
    print(f"Received request on /api/{source}")

    signature = request.headers.get("x-signature", "")

    if not check_signature(signature=signature, data=request.data):
        abort(403, "Signature not valid.")

    content = request.get_json()
    event = content["event"]
    event_type = content["type"]

    emit(source=source, event=event, event_type=event_type)

    return jsonify({"source": source, "data": content})
