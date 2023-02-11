from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# class User(models.Model):
#     firstName = models.CharField(max_length=30)
#     lastName = models.CharField(max_length=30)
#     passwordHash = models.CharField(max_length=100)
#     email = models.CharField(unique=True, max_length=30)

#     def __str__(self):
#         return self.firstName + " " + self.lastName


# class Admin(models.Model):
#     firstName = models.CharField(max_length=30)
#     lastName = models.CharField(max_length=30)
#     passwordHash = models.CharField(max_length=100)
#     email = models.CharField(unique=True, max_length=30)

#     def __str__(self):
#         return self.firstName + " " + self.lastName


class ProductCategorie(models.Model):
    name = models.CharField(max_length=30)
    image = models.CharField(max_length=5000, null=True, blank=True)

    @staticmethod
    def get_all_categories():
        return ProductCategorie.objects.all()

    def __str__(self):
        return self.name


class Product(models.Model):
    productName = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    quantity = models.IntegerField()
    category = models.ForeignKey(
        ProductCategorie, default=1, on_delete=models.SET_DEFAULT
    )
    image = models.CharField(max_length=5000, null=True, blank=True)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

    def __str__(self):
        return self.productName


# class orderHistory(models.Model):
#     user = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
#     date = models.DateTimeField()
#     product = models.ForeignKey(Product, default=1, on_delete=models.SET_DEFAULT)

#     def __str__(self):
#         return self.date + " " + self.product


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateField(auto_now_add=True)
    transaction_id = models.CharField(max_length=200, null=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    buCode = models.CharField(max_length=30, default="0000")

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return (
            self.customer.username
            + "-" * 10
            + "Complete: "
            + str(self.complete)
            + "-" * 10
            + " id : "
            + str(self.transaction_id)
        )


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return str(self.product) + " : " + str(self.quantity)


# Cart
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Product = models
