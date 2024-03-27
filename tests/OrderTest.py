import unittest
import sys
import os

# This allows for importing modules from the parent directory. It is done just for the purpose of running this test.
# Usually this is handled by test frameworks, but for the current scenario, we can go with the following.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fee_calculator.Order import Order
from fee_calculator.constants import RUSH_HOUR_START, RUSH_HOUR_END, RUSH_FEE_MULTIPLIER


class TestOrderMethods(unittest.TestCase):
    """
    Test suite for testing the calculation of various fees associated with an Order in a Flask application.

    Methods:
        test_distance_fee: Tests the calculation of the distance fee based on different delivery distances.
        test_small_order_surcharge: Tests the calculation of the surcharge for small orders based on cart value.
        test_item_surcharge: Tests the calculation of the surcharge based on the number of items.
        test_max_delivery_fee: Tests the capping of delivery fee to a maximum of 1500.
        test_free_delivery: Tests free delivery scenarios based on cart value.
        test_rush_hour_fee: Tests rush hour fee calculation on Fridays.
    """

    def test_distance_fee(self):
        """
        Test the calculation of distance fee for different delivery distances.

        This method tests the following scenarios, based on boundary conditions:
        - 1 meter expecting a fee of 200.
        - 1000 meters expecting a fee of 200.
        - 1499 meters expecting a fee of 300.
        - 1500 meters expecting a fee of 300.
        - 1501 meters expecting a fee of 400.
        """

        min_distance_item = Order(
            cart_value=1500,
            delivery_distance=1000,
            number_of_items=3,
            time="2024-01-15T13:00:00Z",
        )
        self.assertEqual(min_distance_item.calculate_distance_fee(), 200)

        short_distance_item_1 = Order(
            cart_value=1500,
            delivery_distance=1000,
            number_of_items=3,
            time="2024-01-15T13:00:00Z",
        )
        self.assertEqual(short_distance_item_1.calculate_distance_fee(), 200)

        medium_distance_item_1 = Order(
            cart_value=1500,
            delivery_distance=1499,
            number_of_items=3,
            time="2024-01-15T13:00:00Z",
        )
        self.assertEqual(medium_distance_item_1.calculate_distance_fee(), 300)

        medium_distance_item_2 = Order(
            cart_value=1500,
            delivery_distance=1500,
            number_of_items=3,
            time="2024-01-15T13:00:00Z",
        )
        self.assertEqual(medium_distance_item_2.calculate_distance_fee(), 300)

        long_distance_item = Order(
            cart_value=1500,
            delivery_distance=1501,
            number_of_items=3,
            time="2024-01-15T13:00:00Z",
        )
        self.assertEqual(long_distance_item.calculate_distance_fee(), 400)

    def test_small_order_surcharge(self):
        """
        Test the calculation of small order surcharge for different cart values.

        This method tests two scenarios:
        - Cart value of 1001 expecting a surcharge of 0.
        - Cart value of 500 expecting a surcharge of 500.
        - Cart value of 1 expecting a surcharge of 999.
        """
        no_surcharge_item = Order(
            cart_value=1001,
            delivery_distance=1000,
            number_of_items=3,
            time="2024-01-15T13:00:00Z",
        )
        self.assertEqual(no_surcharge_item.calculate_small_order_surcharge(), 0)

        surcharge_item = Order(
            cart_value=500,
            delivery_distance=1000,
            number_of_items=3,
            time="2024-01-15T13:00:00Z",
        )
        self.assertEqual(surcharge_item.calculate_small_order_surcharge(), 500)

        max_surcharge_item = Order(
            cart_value=1,
            delivery_distance=1000,
            number_of_items=3,
            time="2024-01-15T13:00:00Z",
        )
        self.assertEqual(max_surcharge_item.calculate_small_order_surcharge(), 999)

    def test_item_surcharge(self):
        """
        Test the calculation of item surcharge for different quantities of items.

        This method tests the following scenarios, based on boundary conditions:
        - 4 items expecting no surcharge (0).
        - 5 items expecting a surcharge of 50.
        - 12 items expecting a surcharge of 8 * 50 = 400.
        - 13 items expecting a surcharge of 9 * 50 + 120 = 570.
        """
        no_surcharge_item = Order(
            cart_value=1500,
            delivery_distance=1000,
            number_of_items=4,
            time="2024-01-15T13:00:00Z",
        )
        self.assertEqual(no_surcharge_item.calculate_item_surcharge(), 0)

        small_surcharge_item = Order(
            cart_value=1500,
            delivery_distance=1000,
            number_of_items=5,
            time="2024-01-15T13:00:00Z",
        )
        self.assertEqual(small_surcharge_item.calculate_item_surcharge(), 50)

        high_surcharge_item = Order(
            cart_value=1500,
            delivery_distance=1000,
            number_of_items=12,
            time="2024-01-15T13:00:00Z",
        )
        self.assertEqual(high_surcharge_item.calculate_item_surcharge(), 400)

        bulk_surcharge_item = Order(
            cart_value=1500,
            delivery_distance=1000,
            number_of_items=13,
            time="2024-01-15T13:00:00Z",
        )
        self.assertEqual(bulk_surcharge_item.calculate_item_surcharge(), 570)

    def test_max_delivery_fee(self):
        """
        Test the capping of delivery fee to a maximum of 1500 cents.

        This method tests the following scenarios, based on boundary conditions.
        - Total calculated delivery is less than 1500 (total fee is 600)
        - Total calculated delivery is slightly more than 1500 (total fee is  501 + 700 + (6 * 50) = 1501, but capped at 1500)
        """
        under_limit_fee_item = Order(
            cart_value=1000,
            delivery_distance=1000,
            number_of_items=12,
            time="2024-01-15T13:00:00Z",
        )
        self.assertEqual(under_limit_fee_item.calculate_total_delivery_fee(), 600)

        over_limit_fee_item = Order(
            cart_value=499,
            delivery_distance=3001,
            number_of_items=10,
            time="2024-01-15T13:00:00Z",
        )
        self.assertEqual(over_limit_fee_item.calculate_total_delivery_fee(), 1500)

    def test_free_delivery(self):
        """
        Test the free delivery.

        This method tests the following scenarios, based on boundary conditions.
        - Total cart value is slightly less than 20000, i.e. 19999
        - Total cart value is equal to 20000
        - Total cart value is more than 20000
        """
        no_free_delivery_item = Order(
            cart_value=19999,
            delivery_distance=1000,
            number_of_items=4,
            time="2024-01-28T13:00:00Z",
        )
        self.assertEqual(no_free_delivery_item.calculate_total_delivery_fee(), 200)

        free_delivery_item_1 = Order(
            cart_value=20000,
            delivery_distance=1000,
            number_of_items=4,
            time="2024-01-28T13:00:00Z",
        )
        self.assertEqual(free_delivery_item_1.calculate_total_delivery_fee(), 0)

        free_delivery_item_2 = Order(
            cart_value=20001,
            delivery_distance=3001,
            number_of_items=4,
            time="2024-01-28T13:00:00Z",
        )
        self.assertEqual(free_delivery_item_2.calculate_total_delivery_fee(), 0)

    def test_rush_hour_fee(self):
        """
        Test the calculation of Friday rush hour fee.

        This method tests the following scenarios:
        - The time is inside rush hours on Friday
        - The time is outside rush hours on Friday
        - The time is on the days other than Friday
        """

        inside_rush_hours_item_1 = Order(
            cart_value=991,
            delivery_distance=1000,
            number_of_items=4,
            time="2024-01-26T15:00:00Z",
        )
        total_fee = inside_rush_hours_item_1.calculate_total_delivery_fee()
        self.assertEqual(inside_rush_hours_item_1.calculate_friday_rush(total_fee), 301)

        inside_rush_hours_item_2 = Order(
            cart_value=2000,
            delivery_distance=1500,
            number_of_items=4,
            time="2024-01-26T18:59:59Z",
        )
        total_fee = inside_rush_hours_item_2.calculate_total_delivery_fee()
        self.assertEqual(inside_rush_hours_item_2.calculate_friday_rush(total_fee), 432)

        outside_rush_hours_item = Order(
            cart_value=2000,
            delivery_distance=1500,
            number_of_items=4,
            time="2024-01-26T13:00:00Z",
        )
        total_fee = outside_rush_hours_item.calculate_total_delivery_fee()
        self.assertEqual(
            outside_rush_hours_item.calculate_friday_rush(total_fee), total_fee
        )

        outside_Friday_item = Order(
            cart_value=2000,
            delivery_distance=1500,
            number_of_items=4,
            time="2024-01-26T13:00:00Z",
        )
        total_fee = outside_Friday_item.calculate_total_delivery_fee()
        self.assertEqual(
            outside_Friday_item.calculate_friday_rush(total_fee), total_fee
        )


if __name__ == "__main__":
    unittest.main()
