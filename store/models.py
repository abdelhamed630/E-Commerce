from django.db import models
from django.utils.text import slugify  # ← استخدم دي بدل Django slugify

states = [
    ('available', 'available'),
    ('unavailable', 'unavailable'),
]

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        new_slug = slugify(self.name, allow_unicode=True)
        if not self.slug or self.slug != new_slug:
            self.slug = new_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/images/')
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=states, default='available')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        new_slug = slugify(self.name, allow_unicode=True)
        if not self.slug or self.slug != new_slug:
            self.slug = new_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug', 'id']),
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]
