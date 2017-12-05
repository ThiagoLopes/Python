from unittest import TestCase
from promos import list_promos
from inspect import signature
from main import Buyer, Order, ItemToBuy


class TestBuyer(TestCase):
    def test_has_attr(self):
        self.assertTrue(hasattr(Buyer, 'name'))
        self.assertTrue(hasattr(Buyer, 'points'))
        self.assertTrue(hasattr(Buyer, 'member'))

    def test_count_attrs(self):
        sig = signature(Buyer)
        self.assertEqual(len(sig.parameters), 3)

    def test_create(self):
        B1 = Buyer('Bob', 2000, True)
        B2 = Buyer('Anna', 20, False)

        self.assertEqual(B1.name, 'Bob')
        self.assertEqual(B2.name, 'Anna')
        self.assertEqual(B1.points, 2000)
        self.assertEqual(B2.points, 20)
        self.assertEqual(B1.member, True)
        self.assertEqual(B2.member, False)


class TestItemToBuy(TestCase):
    def setUp(self):
        self.cart = ItemToBuy('Banana', 2.00, 6.00)

    def test_has_attr(self):
        self.assertTrue(hasattr(self.cart, 'total'))

    def test_create(self):
        self.assertTrue(isinstance(self.cart, ItemToBuy))

    def test_total(self):
        self.assertEqual(self.cart.total(), 12.00)


class TestOrder(TestCase):
    def setUp(self):
        self.buyer = Buyer('Thiago', 10, False)
        self.bananas = ItemToBuy('Banana', 2, 6)
        self.grapes = ItemToBuy('Grape', 15, 1.5)

    def test_create(self):
        order = Order(self.buyer, [self.bananas, self.grapes])
        self.assertIsInstance(order, Order)

    def test_total(self):
        order = Order(self.buyer, [self.bananas, self.grapes])
        self.assertEqual(order.total(), 34.5)

    def test_due(self):
        order = Order(self.buyer, [self.bananas, self.grapes])
        self.assertEqual(order.due(), order.total() * 0.65)


class TestPromos(TestCase):
    def setUp(self):
        self.buyer = Buyer('Thiago', 10, False)

    def test_promo_values(self):
        bananas = ItemToBuy('Banana', 5, 6)
        order = Order(self.buyer, [bananas])
        self.assertEqual(order.total(), 30)
        self.assertEqual(order.due(), 30 * 0.65)

    def test_promo_itens(self):
        bananas = ItemToBuy('Banana', 2, 1)
        order = Order(self.buyer, [bananas] * 6)
        self.assertEqual(order.total(), 12)
        self.assertEqual(order.due(), 12 - (12 * 0.3))

    def test_promo_vip(self):
        item = ItemToBuy('item', 1, 10)
        self.buyer = Buyer('Thiago', 110, False)
        order = Order(self.buyer, [item])
        self.assertEqual(order.due(), 5)


class TestPromosList(TestCase):
    def test_is_list(self):
        self.assertTrue(isinstance(list_promos, list))

    def test_is_callable(self):
        self.assertEqual([True] * len(list_promos),
                         [callable(i) for i in list_promos])

    def test_signature(self):
        sigs = [signature(x) for x in list_promos]
        looks_like = [1] * len(list_promos)
        self.assertEqual(looks_like, [len(i.parameters) for i in sigs])
