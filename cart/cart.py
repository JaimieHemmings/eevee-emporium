from store.models import Product, Profile


class Cart():
    def __init__(self, request):
        """
        Initialize the cart with the request.
        """
        self.session = request.session
        # Get request
        self.request = request

        # Get current session if it exists
        cart = self.session.get('cart')
        if not cart or not isinstance(cart, dict):
            # Create a new session if it doesn't exist
            cart = self.session['cart'] = {}

        # Make available globally
        self.cart = cart

    def db_add(self, product, quantity):
        """
        Add a product to the cart with a specified quantity.
        :param product: Product object to add.
        :param quantity: Quantity of the product to add.
        """
        product_id = str(product)
        product_qty = int(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = product_qty
        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(
                user__id=self.request.user.id
            ).first()
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.old_cart = str(carty)

    def add(self, product_id, product_qty=1):
        """
        Add a product to the cart or update its quantity.
        """
        # Ensure product_id is a string, and product_qty is an integer
        if hasattr(product_id, 'id'):
            product_id = str(product_id.id)
        else:
            product_id = str(product_id)

        try:
            product_qty = int(product_qty)
        except ValueError:
            product_qty = 1

        self.cart[product_id] = product_qty
        self.session.modified = True
        if self.request.user.is_authenticated:
            # Get the current user
            current_user = Profile.objects.filter(
                user__id=self.request.user.id
            ).first()
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Update the user's cart in the database
            current_user.old_cart = str(carty)
            current_user.save()

    def remove(self, product_id):
        """
        Remove a product from the cart.
        :param product_id: ID of the product to remove.
        """
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        if self.request.user.is_authenticated:
            # Get the current user
            current_user = Profile.objects.filter(
                user__id=self.request.user.id
            ).first()
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Update the user's cart in the database
            current_user.old_cart = str(carty)
            current_user.save()
        # No else block needed as per original code's pass

    def __len__(self):
        """
        Return the total number of items in the cart.
        """
        quantity = 0
        for item in self.cart.values():
            if isinstance(item, dict) and 'quantity' in item:
                try:
                    quantity += int(item['quantity'])
                except ValueError:
                    # Handle cases where quantity might not be a valid integer
                    pass
            elif isinstance(item, (int, str)):
                # This branch handles older or inconsistent cart structures
                try:
                    quantity += int(item)
                except ValueError:
                    pass
        return quantity

    def get_prods(self):
        """
        Iterate over the items of cart and fetch product details efficiently.
        :return: List of products in the cart with their details.
        """
        # Ensure IDs are strings
        product_ids = [str(pid) for pid in self.cart.keys()]

        if not product_ids:
            return []

        # Fetch all products in one query
        products_queryset = Product.objects.filter(id__in=product_ids)
        products_by_id = {str(p.id): p for p in products_queryset}

        products_with_details = []

        for product_id in product_ids:
            if product_id in products_by_id:
                product = products_by_id[product_id]
                cart_item = self.cart.get(product_id, {})
                quantity = 0
                if isinstance(cart_item, dict) and 'quantity' in cart_item:
                    try:
                        quantity = int(cart_item['quantity'])
                    except ValueError:
                        pass
                elif isinstance(cart_item, (int, str)):
                    try:
                        quantity = int(cart_item)
                    except ValueError:
                        pass

                # Only add if quantity is positive
                if quantity > 0:
                    products_with_details.append({
                        'id': product_id,
                        'quantity': quantity,
                        'product': product,
                        'name': product.name,
                        'price': product.price,
                        'total': product.price * quantity,
                        'slug': product.slug
                    })

        return products_with_details

    def total(self):
        """
        Calculate the total price of the cart.
        :return: Total price of the cart.
        """
        total = 0
        # Iterate over values to access stored quantity directly
        for product_id, item in self.cart.items():
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                pass

            quantity = 0
            if isinstance(item, dict) and 'quantity' in item:
                try:
                    quantity = int(item['quantity'])
                except ValueError:
                    pass
            elif isinstance(item, (int, str)):
                try:
                    quantity = int(item)
                except ValueError:
                    pass

            total += product.price * quantity
        return total

    def save(self):
        """Save the cart data to the session."""
        self.session['cart'] = self.cart
        self.session.modified = True
