from django.test import TestCase
from ..models import Booking

class BookingModelTestCase(TestCase):
    def setUp(self):
        # Create a sample Booking instance for testing
        self.booking = Booking.objects.create(
            first_name="John",
            reservation_date="2023-05-15",
            reservation_slot=5,
        )

    def test_booking_str(self):
        # Test the __str__ method
        self.assertEqual(str(self.booking), "John")

    def test_booking_defaults(self):
        # Test default values
        self.assertEqual(self.booking.reservation_slot, 5)

    def test_booking_date(self):
        # Test reservation date
        self.assertEqual(self.booking.reservation_date, "2023-05-15")
