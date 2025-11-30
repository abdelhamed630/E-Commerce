from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



class Coupon(models.Model):
    code=models.CharField(max_length=50, unique=True)
    vailed_from=models.DateTimeField()
    vailed_to=models.DateTimeField()
    discount=models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],help_text="discount percentage between 0 and 100")
    active=models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.code
