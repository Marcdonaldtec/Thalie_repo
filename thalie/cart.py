
from .models import CartItem

class Carts:
    def __init__(self, user):
        self.user = user

    @property
    def cart_items(self):
        return CartItem.objects.filter(cart__user=self.user)

    def get_total(self):
        # Calculate total amount based on cart items
        total = sum(item.product.price * item.quantity for item in self.cart_items)
        return total

    def clear(self):
        # Clear the user's cart
        self.cart_items.delete()
