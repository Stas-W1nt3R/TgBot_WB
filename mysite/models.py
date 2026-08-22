from django.db import models


class TgUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'tg_user'
        verbose_name = 'Tg User'
        verbose_name_plural = 'Tg Users'


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    stock = models.BooleanField()
    url = models.URLField()
    shop_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class UserTracking(models.Model):
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    target_price = models.DecimalField(decimal_places=2, max_digits=10)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_tracking'
        unique_together = ('user', 'product')
        verbose_name = 'User Tracking'
        verbose_name_plural = 'User Tracking'
