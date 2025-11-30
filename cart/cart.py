from decimal import Decimal
from django.conf import settings
from store.models import Product
from coupons.models import Coupon

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            cart_item = self.cart[str(product.id)]
            cart_item['product'] = product
            cart_item['price'] = Decimal(cart_item['price'])
            cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
            yield cart_item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    # --------------------------
    # السعر الأصلي بدون خصم أو ضريبة
    # --------------------------
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    # --------------------------
    # الكوبون
    # --------------------------
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            discount_percent = Decimal(self.coupon.discount) / Decimal('100')
            total_price = self.get_total_price()
            return total_price * discount_percent
        return Decimal('0')

    # --------------------------
    # السعر بعد الخصم فقط
    # --------------------------
    def get_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

    # --------------------------
    # الضريبة على السعر بعد الخصم
    # --------------------------
    def set_tax(self):
        TAX_RATE = Decimal('0.07')  # 7% ضريبة
        return self.get_total_price() * TAX_RATE

    # --------------------------
    # السعر النهائي بعد الخصم والضريبة
    # --------------------------
    def get_total_price_after_discount(self):
        return self.get_price_after_discount() + self.set_tax()
     
     
    def get_total_salary_after_tax(self):
        return self.get_total_price() + self.set_tax()
