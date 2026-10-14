import math

from flask import Flask, jsonify, request

from duckfine import DuckFine

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/fine")
def fine():
    try:
        days = float(request.args.get("days", ""))
    except ValueError:
        return jsonify(error="days must be a non-negative number"), 400

    if not math.isfinite(days) or days < 0:
        return jsonify(error="days must be a non-negative number"), 400

    fee = DuckFine("api").charge(days, deluxe=request.args.get("deluxe") == "1")
    return jsonify(fee=fee)
