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
                self.cart[product_id] = {'quantity': 1, 'price': str(product.price)}
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
        return len(self.cart)