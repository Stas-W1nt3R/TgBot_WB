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


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100)
    coin_id = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(decimal_places=8, max_digits=15)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cryptocurrency'
        verbose_name = 'Cryptocurrency'


class UserTracking(models.Model):
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    target_price = models.DecimalField(decimal_places=2, max_digits=10)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_tracking'
        unique_together = ('user', 'cryptocurrency')
        verbose_name = 'User Tracking'
        verbose_name_plural = 'User Tracking'
