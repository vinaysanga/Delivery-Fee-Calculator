"""
This file contains the constants for the fee calculator application backend:

Constants for field validation:
  MIN_CART_VALUE: The minimum cart value below which an order cannot be placed.
  MIN_DELIVERY_DISTANCE: The minimum delivery distance in meters.
  MIN_ITEMS_COUNT: The minimum number of items in an order.

Constants for fee calculations:
  BASE_DELIVERY_FEE: The base delivery fee in Euros.
  BASE_DISTANCE: The base distance in meters for which the BASE_DELIVERY_FEE_EUR applies.
  FEE_PER_ADDITIONAL_INTERVAL: The fee in Euros for every ADDITIONAL_DISTANCE_INTERVAL interval.
  ADDITIONAL_DISTANCE_INTERVAL: The interval (in meters) after BASE_DISTANCE_METERS, for which FEE_PER_ADDITIONAL_INTERVAL is charged throughout the interval.
  CENTS_PER_EUR: The number of cents per Euro.
  SMALL_ORDER_CART_VALUE: The cart value in Euros above below which small order surcharge is applied.
  SURCHARGEABLE_ITEMS_THRESHOLD: The items count threshold, including and above which a surcharge of EXCESS_CHARGE_PER_ITEM is applicable per item.
  EXCESS_CHARGE_PER_ITEM: The surcharge per item in Euros when the number of items exceeds MIN_SURCHARGEABLE_ITEMS.
  BULK_ITEMS_THRESHOLD: The limit for the number of items beyond which a BULK_FEE is applied.
  BULK_FEE: The extra 'bulk' fee in Euros, that is applied for items above BULK_FEE_THRESHOLD.
  FRIDAY: The integer representing Friday in Python's datetime module (0=Monday, 6=Sunday).
  RUSH_HOUR_START: The start hour (24-hour format) for rush hour.
  RUSH_HOUR_END: The end hour (24-hour format) for rush hour.
  RUSH_FEE_MULTIPLIER: The multiplier to be applied to the base fee during rush hours.
  FREE_DELIVERY_CART_VALUE: The cart value in Euros above which delivery is free.
  MAX_POSSIBLE_DELIVERY_FEE: The maximum possible delivery fee in Euros.

These constants are used in the calculation of delivery fees, taking into account factors such as cart value, delivery distance, time of the order, and the number of items in the order.
"""
# Validation constants
MIN_CART_VALUE = 1
MIN_DELIVERY_DISTANCE = 1
MIN_ITEMS_COUNT = 1

# Fee calculation constants
BASE_DELIVERY_FEE = 2
BASE_DISTANCE = 1000
FEE_PER_ADDITIONAL_INTERVAL = 1
ADDITIONAL_DISTANCE_INTERVAL = 500
CENTS_PER_EUR = 100
SMALL_ORDER_CART_VALUE = 10
SURCHARGEABLE_ITEMS_THRESHOLD = 5
EXCESS_CHARGE_PER_ITEM = 50
BULK_ITEMS_THRESHOLD = 12
BULK_FEE = 1.2
FRIDAY = 5
RUSH_HOUR_START = 15
RUSH_HOUR_END = 19
RUSH_FEE_MULTIPLIER = 1.2
FREE_DELIVERY_CART_VALUE = 200
MAX_POSSIBLE_DELIVERY_FEE = 15
