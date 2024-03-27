from datetime import datetime
from math import ceil
from pydantic import BaseModel, Field, StrictInt
from .constants import *


class Order(BaseModel):
    """
    Represents the item for calculating delivery fees.

    Attributes:
        cart_value: Total value of items in the shopping cart.
        delivery_distance: Distance of the delivery in meters.
        number_of_items: Number of items in the order.
        time: Delivery time as a datetime object. Valid datetime strings are automatically casted to datetime object.

    Note: All attributes are automatically validated by Pydantic.

    Methods:
        calculate_distance_fee(): Calculate the distance-based delivery fee.
        calculate_small_order_surcharge(): Calculate surcharge for small orders.
        calculate_item_surcharge(): Calculate surcharge for large item quantities.
        calculate_friday_rush(): Calculate delivery fee during rush hours on Fridays.
        calculate_total_delivery_fee(): Calculate the total delivery fee.
    """

    cart_value: StrictInt = Field(ge=MIN_CART_VALUE)
    delivery_distance: StrictInt = Field(ge=MIN_DELIVERY_DISTANCE)
    number_of_items: StrictInt = Field(ge=MIN_ITEMS_COUNT)
    time: datetime

    def calculate_distance_fee(self):
        """
        Calculate the distance-based delivery fee.

        Returns:
            int: Distance-based delivery fee in cents.
        """
        distance_fee = BASE_DELIVERY_FEE  # Initialise to the BASE_DELIVERY_FEE

        if self.delivery_distance > BASE_DISTANCE:
            excess_distance = self.delivery_distance - BASE_DISTANCE
            extra_distance_intervals = ceil(
                excess_distance / ADDITIONAL_DISTANCE_INTERVAL
            )
            excess_fee = FEE_PER_ADDITIONAL_INTERVAL * extra_distance_intervals
            distance_fee += excess_fee

        return distance_fee * CENTS_PER_EUR  # Converting to cents

    def calculate_small_order_surcharge(self):
        """
        Calculate surcharge for small orders.

        Returns:
            int: Surcharge amount in cents.
        """
        small_order_surcharge = 0  # Initialise with 0

        if self.cart_value < (SMALL_ORDER_CART_VALUE * CENTS_PER_EUR):
            small_order_surcharge = (
                SMALL_ORDER_CART_VALUE * CENTS_PER_EUR
            ) - self.cart_value

        return small_order_surcharge

    def calculate_item_surcharge(self):
        """
        Calculate surcharge for large item quantities.

        Returns:
            int: Surcharge amount in cents.
        """
        excess_item_surcharge = 0  # Initialise with 0

        if self.number_of_items >= SURCHARGEABLE_ITEMS_THRESHOLD:
            excess_items = self.number_of_items - (
                SURCHARGEABLE_ITEMS_THRESHOLD - 1
            )  # Subtracting 1 because no. of items including SURCHARGEABLE_ITEMS_THRESHOLD are considered as excess
            excess_item_surcharge = EXCESS_CHARGE_PER_ITEM * excess_items

        if self.number_of_items > BULK_ITEMS_THRESHOLD:
            excess_item_surcharge += BULK_FEE * CENTS_PER_EUR

        return excess_item_surcharge

    def calculate_friday_rush(self, fee):
        """
        Calculate delivery fee during rush hours on Fridays.

        Args:
            fee (int): The delivery fee.

        Returns:
            int: The delivery fee during rush hours in cents.
        """
        if (self.time.isoweekday() == FRIDAY) and (
            RUSH_HOUR_START <= self.time.hour < RUSH_HOUR_END
        ):
                return round(
                fee * RUSH_FEE_MULTIPLIER
            )  # Round up the decimal value to nearest whole cent
        else:
            return fee

    def calculate_total_delivery_fee(self):
        """
        Calculate the total delivery fee.

        Returns:
            int: Total delivery fee in cents.
        """
        # Free delivery for high cart value
        if self.cart_value >= (FREE_DELIVERY_CART_VALUE * CENTS_PER_EUR):
            return 0

        fee = 0  # Initialise with 0

        fee += self.calculate_distance_fee()

        fee += self.calculate_small_order_surcharge()

        fee += self.calculate_item_surcharge()

        fee = self.calculate_friday_rush(fee)

        # Cap the delivery fee
        fee = min(fee, (MAX_POSSIBLE_DELIVERY_FEE * CENTS_PER_EUR))

        return fee
