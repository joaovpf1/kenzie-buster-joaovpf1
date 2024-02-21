from django.urls import path
from movies_orders.views import OrderView

urlpatterns = [
    path("movies/<int:movie_id>/orders/", OrderView.as_view()),
]
