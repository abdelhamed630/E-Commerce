from django.db import models
import string
import random
from store.models import Product

def generate_order_id(ref_length=8):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=ref_length))


class Order(models.Model):
    order_id=models.CharField(max_length=8, unique=True, default=generate_order_id)
    customer_name=models.CharField(max_length=100)
    email=models.EmailField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    address=models.CharField(max_length=255)
    paid=models.BooleanField(default=False)
    city=models.CharField(max_length=100)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]
        
    def __str__(self):
        return f"Order {self.order_id} by {self.customer_name}"
    
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = generate_order_id()
            while Order.objects.filter(order_id=self.order_id).exists():
                self.order_id = generate_order_id()
            self.order_id = self.order_id
        super().save(*args, **kwargs)
        
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
  
  
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"

    def get_cost(self):
        return self.price * self.quantity

    
class Orderpayment(models.Model):
    order=models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    pay_phone=models.CharField(max_length=11)
    pay_image=models.ImageField(upload_to='vodfonecash/')
    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for Order {self.order.order_id}"
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
