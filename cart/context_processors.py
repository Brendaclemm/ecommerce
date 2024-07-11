from .cart import Cart


# create context processor so that our cart can work on all pages of our site
def cart(request):
    # return the default data from our Cart
    return {'cart': Cart(request)}
