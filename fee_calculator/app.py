from flask import Flask, request, jsonify
from .Order import Order
from pydantic import ValidationError
from http import HTTPStatus

app = Flask(__name__)


@app.errorhandler(ValidationError)
def handle_value_error(error):
    """
    Handle ValidationError that may arise due to wrong values.

    Args:
        error: The ValidationError object containing details about the validation error.

    Returns:
        Response: A JSON response containing details of the validation error with a 400 status code.
    """
    error_details = {error["loc"][0]: error["msg"] for error in error.errors()}
    response = jsonify({"Validation Error": error_details})
    response.status_code = HTTPStatus.BAD_REQUEST
    return response


@app.route("/", methods=["POST"])
def index():
    """
    Route all the requests with '/' here. Accepts only POST requests, others will be met with a 405 response.

    Returns:
        Response: A JSON response containing the calculated delivery fee with a 200 status code.
    """
    data = request.json
    order = Order(**data)
    delivery_fee = order.calculate_total_delivery_fee()
    return jsonify({"delivery_fee": delivery_fee})


if __name__ == "__main__":
    app.run(debug=True)
