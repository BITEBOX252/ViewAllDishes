from django.urls import path
from .views import CategoryListAPIView,DishListAPIView,DishDetailAPIView,CartAPIView,CartLisAPItView
urlpatterns = [
    path('categories/',CategoryListAPIView.as_view()),
    path('dishes/',DishListAPIView.as_view()),
    path('dish/<slug>',DishDetailAPIView.as_view()),
    path('cart/',CartAPIView.as_view()),
    path('cart-list/<str:cart_id>/<int:user_id>/',CartLisAPItView.as_view()),
    path('cart-list/<str:cart_id>/',CartLisAPItView.as_view()),
]