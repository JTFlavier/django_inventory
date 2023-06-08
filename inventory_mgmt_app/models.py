from django.db import models

class Item(models.Model):
    sku = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length = 255, unique=True, default="")
    price = models.DecimalField(decimal_places = 2, max_digits = 20, default=0)
    description = models.TextField(default="")
    quantity = models.IntegerField(default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sku)
    
    def save(self, *args, **kwargs):
        self.status = self.quantity > 0
        return super(Item, self).save(*args, **kwargs)

class Customer(models.Model):
    email = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200, default="")
    address = models.CharField(max_length=200, default="")

    def __str__(self):
        return str(self.email)
    
class Order(models.Model):
    order_number = models.IntegerField()
    items = models.ManyToManyField(Item)
    customer = models.ForeignKey('Customer', on_delete = models.DO_NOTHING, null=False)

    def __str__(self):
        return str(self.order_number)
