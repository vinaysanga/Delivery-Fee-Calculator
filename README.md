# Python API for Backend
Code for [Wolt backend assignment](https://github.com/woltapp/engineering-internship-2024) using Python. You can run the application either using **Docker** or using **Python**. Please follow the guides below for both the cases.

## Prerequisites
- **Docker**\
**OR**
- **Python:** Version 3.11.7 or later

## Frameworks & Libraries
- **Flask:** Version 3.0.0
  - Description: A micro web framework for building web applications in Python.
- **pydantic:** Version 2.5.3
  - Description: A data validation and parsing library.

## Running the backend
#### A. Using Docker
The app is containerized, and can be built and run as follows:
1. Open the terminal in the current folder. Build the image,
```
docker build -t vinay_sanga_backend . 
```

2. Run the image. The following command maps the container port `5000` to your local port `5001`. \
Please change the port if you get conflicts.
```
docker run -dp 5001:5000 vinay_sanga_backend
```
3. Make **POST** requests to the API endpoint at URL: [http://127.0.0.1:5001/](http://127.0.0.1:5001/). Please see [example](https://github.com/vinaysanga/Delivery-Fee-Calculator/edit/master/README.md#example) below.

4. After you are done using, please stop the docker container.

#### B. Locally using python 3.11.7
1. Install the required dependencies using pip:
```
pip3 install -r requirements.txt
```

2. Run the flask app `fee_calculator` as follows. Please change the port if you get conflicts:
```
flask --app fee_calculator run --host 0.0.0.0 --port 5001
```

3. Make **POST** requests to the API endpoint at URL: [http://127.0.0.1:5001/](http://127.0.0.1:5001/)

## Example
#### JSON for the POST request: 
```json
{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
```
#### Field details

| Field             | Type  | Description                                                               | Example value                             |
|:---               |:---   |:---                                                                       |:---                                       |
|cart_value         |Integer|Value of the shopping cart __in cents__.                                   |__790__ (790 cents = 7.90€)                |
|delivery_distance  |Integer|The distance between the store and customer’s location __in meters__.      |__2235__ (2235 meters = 2.235 km)          |
|number_of_items    |Integer|The __number of items__ in the customer's shopping cart.                   |__4__ (customer has 4 items in the cart)   |
|time               |String |Order time in UTC in [ISO format](https://en.wikipedia.org/wiki/ISO_8601). |__2024-01-15T13:00:00Z__                   |
#### Response:
```json
{"delivery_fee": 710}
```
#### Field details

| Field         | Type  | Description                           | Example value             |
|:---           |:---   |:---                                   |:---                       |
|delivery_fee   |Integer|Calculated delivery fee __in cents__.  |__710__ (710 cents = 7.10€)|

## Testing
There are two test suites:
1. Unit test for `Order` class, which tests all the calculations required for the delivery fee (`OrderTest.py`).
2. Integration test for the app, which tests missing values, invalid input, etc. (`AppTest.py`).

Please run the tests as follows:
1. To run the unit test:
```
python3 tests/OrderTest.py
```
Result should be,
```
......
----------------------------------------------------------------------
Ran 6 tests in 0.000s

OK
```
2. To run the integration test:
```
python3 tests/AppTest.py
```
The result should be,
```
....
----------------------------------------------------------------------
Ran 4 tests in 0.004s

OK
```
## Notes:
- The API includes input data validation. If any field is missing or contains an incorrect value (e.g., 0, negative, or a float instead of an int), you will receive a `ValidationError`.
- The rush hour fees are rounded to nearest integer.
