from django.db import models

# Create your models here.

class User(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    passwordHash = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=30)

    def __str__(self):
        return self.firstName + " " + self.lastName


class Admin(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    passwordHash = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=30)

    def __str__(self):
        return self.firstName + " " + self.lastName


class ProductCategorie(models.Model):
    name = models.CharField(max_length=30)

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

    def __str__(self):
        return self.productName


class orderHistory(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
    date = models.DateTimeField()
    product = models.ForeignKey(Product, default=1, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return self.date + " " + self.product
