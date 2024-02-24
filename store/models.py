import datetime
from django.contrib.auth.hashers import make_password
from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    """
    Represents a product category.
    """

    name = models.CharField(max_length=50)

    def __str__(self):
        """
        Returns a string representation of the category.
        """
        return self.name

    class Meta:
        verbose_name_plural = "categories"

class Customer(models.Model):
    """
    Represents a customer in the system.
    """

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        """
        Returns a string representation of the customer.
        """
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        """
        Overrides the save method to hash the password before saving.
        """
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    Represents a product available for purchase.
    """

    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00)],
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to="uploads/product/")

    def __str__(self):
        """
        Returns a string representation of the product.
        """
        return self.name


class Order(models.Model):
    """
    Represents a customer's order.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    address = models.CharField(max_length=255, default="")
    phone = PhoneNumberField(null=True, blank=True)
    date = models.DateField(default=datetime.date.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns a string representation of the order.
        """
        return f"Order {self.id} - {self.customer} - {self.product}"
