from django.test import TestCase
from ..models import Cart, User, MenuItem, Category

class CartModelTestCase(TestCase):
    def setUp(self):
        # Create sample User and MenuItem instances for testing
        self.user = User.objects.create(username="testuser")
        
        # Create a sample Category instance for testing
        self.category = Category.objects.create(
            slug="sample-category",
            title="Sample Category",
        )
        
        self.menu_item = MenuItem.objects.create(
            title="Sample Item",
            price=10.99,
            featured=True,
            description="A delicious sample item",
            category=self.category,  # Replace with actual category if needed
        )

        # Create a sample Cart instance for testing
        self.cart = Cart.objects.create(
            user=self.user,
            menuitem=self.menu_item,
            quantity=2,
            unit_price=10.99,
            price=21.98,
        )

    def test_cart_str(self):
        # Test the __str__ method
        expected_str = f"Cart for user: {self.user.username}"
        self.assertEqual(str(self.cart), expected_str)


    def test_cart_category(self):
        # Test the category field
        self.assertEqual(self.cart.menuitem, self.menu_item)
