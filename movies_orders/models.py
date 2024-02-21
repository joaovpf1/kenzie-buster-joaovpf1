from django.db import models


# Create your models here.
class MovieOrder(models.Model):
    purchased_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    user_order = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
    )
    movie_order = models.ForeignKey(
        "movies.Movie",
        on_delete=models.PROTECT,
    )
