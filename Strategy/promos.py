def promo_more_five_itens(order):
    if len(order.cart) > 5:
        # 30%
        return order.total() * 0.30
    return 0


def promo_more_30_value(order):
    total = order.total()
    if total >= 30:
        # 35%
        return total * 0.35
    else:
        return 0


def promo_premium_user(order):
    if float(order.buyer.points) > 100:
        # 50%
        return order.total() * 0.5
    else:
        return 0


list_promos = [k for p, k in globals().items() if p.startswith('promo_')]
