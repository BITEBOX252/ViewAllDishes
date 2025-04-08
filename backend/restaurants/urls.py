from django.urls import path, include
from .views import NearbyRestaurants,CouponStatAPIView,CouponListAPIView,CouponDetailAPIView,ReviewListAPIView,ReviewDetailAPIView,RestaurantCreateView,DashboardStatAPIView,RevenueAPIView,DishAPIView,OrderAPIView,OrderDetailAPIView,NotificationUnseenAPIView,NotificationseenAPIView,NotificationSummaryAPIView,NotificationRestaurantMarkAsSeenAPIView,RestaurantUpdateAPIView,RestaurantOwnerProfileUpdateAPIView,RestaurantAPIView,RestaurantDishAPIView,DishCreateAPIView,DishDeleteAPIView,DishUpdateAPIView
urlpatterns = [

    path('nearby-restaurants/', NearbyRestaurants.as_view(), name='nearby_restaurants'),
    path('register/', RestaurantCreateView.as_view()),
    path('stats/<restaurant_id>/', DashboardStatAPIView.as_view()),
    path('dishes/<restaurant_id>/', DishAPIView.as_view()),
    path('orders/<restaurant_id>/', OrderAPIView.as_view()),
    path('orders/<restaurant_id>/<order_id>/', OrderDetailAPIView.as_view()),
    path('revenue/<restaurant_id>/', RevenueAPIView.as_view()),
    path('reviews/<restaurant_id>/', ReviewListAPIView.as_view()),
    path('reviews/<restaurant_id>/review_id/', ReviewDetailAPIView.as_view()),
    path('coupons/<restaurant_id>/', CouponListAPIView.as_view()),
    path('coupon-detail/<restaurant_id>/<coupon_id>/', CouponDetailAPIView.as_view()),
    path('coupon-stats/<restaurant_id>/', CouponStatAPIView.as_view()),
    path('unseen-notifications/<restaurant_id>/', NotificationUnseenAPIView.as_view()),
    path('seen-notifications/<restaurant_id>/', NotificationseenAPIView.as_view()),
    path('notifications-summary/<restaurant_id>/', NotificationSummaryAPIView.as_view()),
    path('notifications-mark-as-seen/<restaurant_id>/', NotificationRestaurantMarkAsSeenAPIView.as_view()),
    path('profile-update/<int:pk>/', RestaurantOwnerProfileUpdateAPIView.as_view()),
    path('settings-update/<int:pk>/', RestaurantUpdateAPIView.as_view()),
    path('shop/<restaurant_slug>/', RestaurantAPIView.as_view()),
    path('dishes/<restaurant_slug>/', RestaurantDishAPIView.as_view()),
    path('create-dish/<restaurant_id>/', DishCreateAPIView.as_view()),
    path('delete-dish/<restaurant_id>/<dish_did>/', DishDeleteAPIView.as_view()),
    path('update-dish/<restaurant_id>/<dish_did>/', DishUpdateAPIView.as_view()),

]