from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session

        # get the current session key if it exists
        cart = self.session.get('session_key')

        # if user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure cart is available on all pages of site
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = quantity

        # logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = product_qty

        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # get ids from cart
        product_ids = self.cart.keys()

        # use ids to get products in the database
        products = Product.objects.filter(id__in=product_ids)

        # return looked up products
        return products

    def get_quantities(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = quantity

        # get cart
        our_cart = self.cart
        # update dictionary/cart
        our_cart[product_id] = product_qty

        self.session.modified = True

        return self.cart

    def delete_item(self, product):
        product_id = str(product)

        # delete from dictionary
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def total(self):
        # get product ids
        product_ids = self.cart.keys()

        # look up those keys in our product database
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart

        # start counting from 0
        total = 0

        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += (product.sale_price * value)
                    else:
                        total += (product.price * value)

        return total
