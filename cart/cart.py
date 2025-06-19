from store.models import Product

class Cart():
    def __init__(self, request):
        """
        Initialize the cart with the request.
        """
        self.session = request.session

        # Get current session if it exists
        cart = self.session.get('session_key')
        if not cart or not isinstance(cart, dict):
            # Create a new session if it doesn't exist
            cart = self.session['session_key'] = {}

        # Make available globally
        self.cart = cart

    def add(self, product):
        """
        Add a product to the cart.
        :param product: Product object to add to the cart.
        """
        if product.id:
            product_id = str(product.id)
            if product_id not in self.cart:
                self.cart[product_id] = {
                    'quantity': 1, 'price': str(product.price)
                }
            else:
                self.cart[product_id]['quantity'] += 1
            self.session.modified = True
        else:
            pass

    def __len__(self):
        """
        Return the total number of items in the cart.
        :return: Total number of items in the cart.
        """
        quantity = 0
        for product in self.cart.keys():
            quantity += self.cart[product]['quantity']
        return quantity

    def get_prods(self):
        """
        Iterate over the items in the cart.
        :return: List of products in the cart with their details.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        # Create a list to hold products with their quantities
        cart_products = []
        for product in products:
            prod_id = str(product.id)
            cart_products.append({
                'product': product,
                'slug': product.slug,
                'name': product.name,
                'quantity': self.cart[prod_id]['quantity'],
                'price': self.cart[prod_id]['price'],
                'image': product.image.url if product.image else None,
                'total': float(self.cart[prod_id]['price']) * self.cart[prod_id]['quantity']
            })
        return cart_products
            