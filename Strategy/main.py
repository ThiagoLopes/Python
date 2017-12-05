from collections import namedtuple
import promos
Buyer = namedtuple('Buyer', 'name points member')


class ItemToBuy(object):
    """This is a cart
    """

    def __init__(self, name, value, ammount):
        self.name = name
        self.value = value
        self.ammount = ammount

    def total(self):
        return self.value * self.ammount

    def __repr__(self):
        return self.name


def best_promo(order):
    best = max([f(order) for f in promos.list_promos])
    return best


class Order():
    """This is a order buy
    """

    def __init__(self, buyer, cart, promo=best_promo):
        self.buyer = buyer
        self.cart = list(cart)
        self.promo = promo

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def __repr__(self):
        return 'Byuer: {}\nItens: {}'.format(self.buyer.name, self.cart)

    def due(self):
        if self.promo is None:
            discount = 0
        else:
            discount = self.promo(self)
        return self.total() - discount
