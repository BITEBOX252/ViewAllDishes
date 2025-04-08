from django.forms import ValidationError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics,status
from store.models import Dish,CartOrder,CartOrderItem,Review,Coupon,Notification
from store.serializers import SummarySerializer,DishSerializer,RestaurantSerializer,NotificationSerializer,NotificationSummarySerializer,CouponSummarySerializer,CouponSerializer,ReviewSerializer, CartOrderSerializer,CartOrderItemSerializer,SpecificationSerializer,SpiceLevelSerializer,PortionSizeSerializer,GallerySerializer
from .models import Restaurant
from .serializers import RestaurantCreateSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from math import radians, sin, cos, sqrt, atan2
from account.models import User,Profile
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication 
from django.db import models
from account.serializers import ProfileSerializer
from django.db import transaction


class RestaurantCreateView(generics.CreateAPIView):
    serializer_class = RestaurantCreateSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [AllowAny]
 
    def create(self, request, *args, **kwargs):
        payload = request.data

        user_id = payload.get('user_id')
        print(user_id)
        # Check if the user already has an associated restaurant
        if Restaurant.objects.filter(user_id=user_id).exists():
            return Response({"message": "User has already associated a restaurant with this account."}, status=status.HTTP_400_BAD_REQUEST)

        image = payload.get('image')
        name = payload.get('name')
        email = payload.get('email')
        description = payload.get('description')
        mobile = payload.get('mobile')
        latitude = payload.get('latitude')
        longitude = payload.get('longitude')

        # Create the restaurant
        Restaurant.objects.create(
            image=image,
            name=name,
            email=email,
            description=description,
            phone_number=mobile,
            user_id=user_id,
            latitude=latitude,
            longitude=longitude
        )

        return Response({"message": "Created vendor account"}, status=status.HTTP_201_CREATED)


   

class NearbyRestaurants(APIView):

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        # Radius of the Earth in kilometers
        R = 6371.0  # Radius of the Earth in kilometers
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        # print(lat1, lon1, lat2, lon2)
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        print ("Distance:-----------",distance)
        return distance

    def get(self, request):
        # Get user's current location from the database (assuming user's location is saved during registration)
        user = request.user
        print("User",user)
        # user=User.objects.get(email="wetucecoh@mailinator.com")
        user_latitude = user.latitude
        user_longitude=user.longitude  # Replace with your user model fields
        print("user_latitude",user_latitude)
        print("user_longitude",user_longitude)
        nearby_restaurants = []
        radius_km = 5  # Define the search radius in kilometers

        # Get all restaurants from the database
        restaurants = Restaurant.objects.all()
        print(restaurants)
        # Loop through all restaurants and calculate the distance using Haversine formula
        for restaurant in restaurants:
            restaurant_location = (restaurant.latitude, restaurant.longitude)
            print(restaurant_location)
            distance = self.haversine_distance(user_latitude, user_longitude, restaurant.latitude, restaurant.longitude)

            # Check if the restaurant is within the 5 km radius
            if distance <= radius_km:
                nearby_restaurants.append(restaurant)
        print(nearby_restaurants)
        # Serialize the filtered restaurants
        serializer = RestaurantCreateSerializer(nearby_restaurants, many=True)
        return Response(serializer.data)




class DashboardStatAPIView(generics.ListAPIView):
    serializer_class=SummarySerializer
    permission_classes=[AllowAny]
    def get_queryset(self):
        restaurant_id=self.kwargs['restaurant_id']
        restaurant=Restaurant.objects.get(id=restaurant_id)

        dish_count=Dish.objects.filter(restaurant=restaurant).count()
        order_count=CartOrder.objects.filter(restaurant=restaurant,payment_status="paid").count()
        # foriegn key
        revenue=CartOrderItem.objects.filter(restaurant=restaurant,order__payment_status="paid").aggregate(total_revenue=models.Sum(models.F('sub_total')+ models.F('shipping_amount')))['total_revenue'] or 0


        return [{
            'dishes':dish_count,
            'orders':order_count,
            'revenue':revenue,
        }]
    

    def list(self,*args, **kwargs):
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset,many=True)
        return Response(serializer.data)


class DishAPIView(generics.ListAPIView):
    serializer_class=DishSerializer
    permission_classes=[AllowAny]

    def get_queryset(self):
        restaurant_id=self.kwargs['restaurant_id']
        restaurant=Restaurant.objects.get(id=restaurant_id)
        print(Dish.objects.filter(restaurant=restaurant).order_by('-id'))
        return Dish.objects.filter(restaurant=restaurant).order_by('-id')
    

class OrderAPIView(generics.ListAPIView):
    serializer_class=CartOrderSerializer
    permission_classes=[AllowAny]

    def get_queryset(self):
        restaurant_id=self.kwargs['restaurant_id']
        restaurant=Restaurant.objects.get(id=restaurant_id)
        return CartOrder.objects.filter(restaurant=restaurant,payment_status='paid').order_by('-id')

class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class=CartOrderSerializer
    permission_classes=[AllowAny]

    def get_queryset(self):
        restaurant_id=self.kwargs['restaurant_id']
        order_id=self.kwargs['order_id']
        restaurant=Restaurant.objects.get(id=restaurant_id)
        return CartOrder.objects.get(restaurant=restaurant,oid=order_id)
    
class RevenueAPIView(generics.ListAPIView):
    serializer_class=CartOrderItemSerializer
    permission_classes=[AllowAny]


    def get_queryset(self):
        restaurant_id=self.kwargs['restaurant_id']
        restaurant=Restaurant.objects.get(id=restaurant_id)
        return CartOrderItem.objects.filter(restaurant=restaurant,order__payment_status="paid").aggregate(total_revenue=models.Sum(models.F('sub_total')+ models.F('shipping_amount')))['total_revenue'] or 0
    



class ReviewListAPIView(generics.ListAPIView):
    serializer_class=ReviewSerializer
    permission_classes=[AllowAny]

    def get_queryset(self):
        restaurant_id=self.kwargs['restaurant_id']
        restaurant=Restaurant.objects.get(id=restaurant_id)
        return Review.objects.filter(dish__restaurant=restaurant)
        

class ReviewDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class=ReviewSerializer
    permission_classes=[AllowAny]

    def get_object(self):
        restaurant_id=self.kwargs['restaurant_id']
        review_id=self.kwargs['review_id']

        restaurant=Restaurant.objects.get(id=restaurant_id)
        review=Review.objects.get(id=review_id,dish__restaurant=restaurant)


        return review


class CouponListAPIView(generics.ListAPIView):
    serializer_class=CouponSerializer
    permission_classes=[AllowAny]

    
    def get_queryset(self):
        restaurant_id=self.kwargs['restaurant_id']
        restaurant=Restaurant.objects.get(id=restaurant_id)

        return Coupon.objects.filter(restaurant=restaurant)

    def create(self,request,*args, **kwargs):
        payload=request.data
        restaurant_id=payload['restaurant_id']
        code=payload['code']
        discount=payload['discount']
        active=payload['active']

        restaurant=Restaurant.objects.get(id=restaurant_id)
        Coupon.objects.create(
            restaurant=restaurant,
            code=code,
            discount=discount,
            active=(active.lower()=='true')

        )
        return Response({"message":"Coupon created successfully"},status=status.HTTP_201_CREATED)
    

class CouponDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class=CouponSerializer
    permission_classes=[AllowAny]

    def get_object(self):
        restaurant_id=self.kwargs['restaurant_id']
        coupon_id=self.kwargs['coupon_id']

        restaurant=Restaurant.objects.get(id=restaurant_id)
        return Coupon.objects.get(restaurant=restaurant,id=coupon_id)
    
class CouponStatAPIView(generics.ListAPIView):
    serializer_class=CouponSerializer
    permission_classes=[AllowAny]

    def get_object(self):
        restaurant_id=self.kwargs['restaurant_id']
        restaurant=Restaurant.objects.get(id=restaurant_id)

        total_coupons=Coupon.objects.filter(
            restaurant=restaurant
        ).count()
        active_coupons=Coupon.objects.filter(restaurant=restaurant,active=True).count()
        return [{
            'total_coupons':total_coupons,
            'active_coupons':active_coupons,

        }]


    def list(self,*args, **kwargs):
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset,many=True)
        return Response(serializer.data)
    

class NotificationUnseenAPIView(generics.ListAPIView):
    serializer_class=CouponSummarySerializer
    permission_classes=[AllowAny]

    def get_queryset(self):
        restaurant_id=self.kwargs['restaurant_id']
        restaurant=Restaurant.objects.get(id=restaurant_id)
        return Notification.objects.filter(restaurant=restaurant,seen=False).order_by('-id')
    


class NotificationseenAPIView(generics.ListAPIView):
    serializer_class=CouponSummarySerializer
    permission_classes=[AllowAny]

    def get_queryset(self):
        restaurant_id=self.kwargs['restaurant_id']
        restaurant=Restaurant.objects.get(id=restaurant_id)
        return Notification.objects.filter(restaurant=restaurant,seen=True).order_by('-id')
    


class NotificationSummaryAPIView(generics.ListAPIView):
    serializer_class=NotificationSummarySerializer
    permission_classes=[AllowAny]

    def get_queryset(self):
        restaurant_id=self.kwargs['restaurant_id']
        restaurant=Restaurant.objects.get(id=restaurant_id)

        unread_notification=Notification.objects.filter(restaurant=restaurant,seen=False).count()
        read_notification=Notification.objects.filter(restaurant=restaurant,seen=True).count()
        all_notification=Notification.objects.filter(restaurant=restaurant).count()

        return[{
            'unread_notification':unread_notification,
            'read_notification':read_notification,
            'all_notification':all_notification,
        }]
    
    def list(self,*args, **kwargs):
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset,many=True)
        return Response(serializer.data)


class NotificationRestaurantMarkAsSeenAPIView(generics.RetrieveAPIView):
    serializer_class=NotificationSerializer
    permission_classes=[AllowAny]

    def get_object(self):
        restaurant_id=self.kwargs['restaurant_id']
        notification_id=self.kwargs['notification_id']

        restaurant=Restaurant.objects.get(id=restaurant_id)
        notification=Notification.objects.get(restaurant=restaurant,id=notification_id)

        notification.seen=True
        notification.save()

        return notification
    


class RestaurantOwnerProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset=Profile.objects.all()
    serializer_class=ProfileSerializer
    permission_classes=[AllowAny]


class RestaurantUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset=Profile.objects.all()
    serializer_class=RestaurantSerializer
    permission_classes=[AllowAny]


class RestaurantAPIView(generics.RetrieveUpdateAPIView):
    serializer_class=RestaurantSerializer
    permission_classes=[AllowAny]

    def get_object(self):
        restaurant_slug=self.kwargs['restaurant_slug']
        return Restaurant.objects.get(slug=restaurant_slug)
    

class RestaurantDishAPIView(generics.RetrieveUpdateAPIView):
    serializer_class=DishSerializer
    permission_classes=[AllowAny]

    def get_object(self):
        restaurant_slug=self.kwargs['restaurant_slug']
        restaurant=Restaurant.objects.get(slug=restaurant_slug)

        return Dish.objects.filter(restaurant=restaurant)


class DishCreateAPIView(generics.CreateAPIView):
    queryset=Dish.objects.all()
    serializer_class=DishSerializer


    @transaction.atomic
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # dish_instance=serializer.instance
        # specification_data=[]
        # level_data=[]
        # size_data=[]
        # gallery_data=[]
        
        # for key,value in self.request.data.item():
        #     if key.startwith('specifications') and ['title'] in key:
        #         index=key.split('[')[1].split(']')[0]
        #         title=value
        #         content_key=f'specifications[{index}][content]'
        #         content=self.request.data.get(content_key)
        #         specification_data.append({'title':title,'content':content})

        #     elif key.startwith('spiceLevel') and ['level_name'] in key:
        #         index=key.split('[')[1].split(']')[0]
        #         level_name=value
        #         additional_price_key=f'spiceLevel[{index}][additional_price]'
        #         additional_price=self.request.data.get(additional_price_key)
        #         level_data.append({'level_name':level_name,'additional_price':additional_price})
            
        #     elif key.startwith('sizes') and ['name'] in key:
        #         index=key.split('[')[1].split(']')[0]
        #         name=value
        #         price_key=f'sizes[{index}][price]'
        #         price=self.request.data.get(price_key)
        #         size_data.append({'name':name,'price':price})
            
        #     elif key.startwith('gallery') and ['image'] in key:
        #         index=key.split('[')[1].split(']')[0]
        #         image=value
        #         gallery_data.append({'image':image})

        dish_instance = serializer.instance
        specification_data = []
        level_data = []
        size_data = []
        gallery_data = []

        for key, value in self.request.data.items():  # ✅ Fix items() method
            if key.startswith('specifications') and 'title' in key:  # ✅ Fix startswith() and key checking
                index = key.split('[')[1].split(']')[0]
                title = value
                content_key = f'specifications[{index}][content]'
                content = self.request.data.get(content_key)
                specification_data.append({'title': title, 'content': content})

            elif key.startswith('spiceLevel') and 'level_name' in key:
                index = key.split('[')[1].split(']')[0]
                level_name = value
                additional_price_key = f'spiceLevel[{index}][additional_price]'
                additional_price = self.request.data.get(additional_price_key)
                level_data.append({'level_name': level_name, 'additional_price': additional_price})

            elif key.startswith('sizes') and 'size_name' in key:
                index = key.split('[')[1].split(']')[0]
                size_name = value
                price_key = f'sizes[{index}][price]'
                price = self.request.data.get(price_key)
                size_data.append({'size_name': size_name, 'price': price})

            elif key.startswith('gallery') and 'image' in key:
                index = key.split('[')[1].split(']')[0]
                image = value
                gallery_data.append({'image': image})  # ✅ Remove the extra comma

        
        print('specifications',specification_data)
        print('levels',level_data)
        print('sizes',size_data)
        print('gallery',gallery_data)
        self.save_nested_data(dish_instance,SpecificationSerializer,specification_data)
        self.save_nested_data(dish_instance,SpiceLevelSerializer,level_data)
        self.save_nested_data(dish_instance,PortionSizeSerializer,size_data)
        self.save_nested_data(dish_instance,GallerySerializer,gallery_data)
        # return super().perform_create(serializer)

    def save_nested_data(self,dish_instance,serializer_class,data):
            serializer=serializer_class(data=data,many=True,context={'dish_instance':dish_instance})
            serializer.is_valid(raise_exception=True)
            serializer.save(dish=dish_instance)


class DishDeleteAPIView(generics.DestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = (AllowAny, )

    def get_object(self):
        restaurant_id = self.kwargs['restaurant_id']
        dish_did = self.kwargs['dish_did']

        restaurant = Restaurant.objects.get(id=restaurant_id)
        dish = Dish.objects.get(restaurant=restaurant, did=dish_did)
        return dish



class DishUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset=Dish.objects.all()
    serializer_class=DishSerializer
    

    def get_object(self):
        restaurant_id = self.kwargs['restaurant_id']
        dish_did = self.kwargs['dish_did']

        restaurant = Restaurant.objects.get(id=restaurant_id)
        dish = Dish.objects.get(restaurant=restaurant, did=dish_did)
        return dish



    @transaction.atomic
    def update(self,request,*args, **kwargs ):
       
        dish = self.get_object()
        serializer=self.get_serializer(dish,data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        dish.specification().delete()
        dish.spice_level().delete()
        dish.portion_size().delete()
        dish.gallery().delete()



        specification_data = []
        level_data = []
        size_data = []
        gallery_data = []

        for key, value in self.request.data.items():  # ✅ Fix items() method
            if key.startswith('specifications') and 'title' in key:  # ✅ Fix startswith() and key checking
                index = key.split('[')[1].split(']')[0]
                title = value
                content_key = f'specifications[{index}][content]'
                content = self.request.data.get(content_key)
                specification_data.append({'title': title, 'content': content})

            elif key.startswith('spiceLevel') and 'level_name' in key:
                index = key.split('[')[1].split(']')[0]
                level_name = value
                additional_price_key = f'spiceLevel[{index}][additional_price]'
                additional_price = self.request.data.get(additional_price_key)
                level_data.append({'level_name': level_name, 'additional_price': additional_price})

            elif key.startswith('sizes') and 'size_name' in key:
                index = key.split('[')[1].split(']')[0]
                size_name = value
                price_key = f'sizes[{index}][price]'
                price = self.request.data.get(price_key)
                size_data.append({'size_name': size_name, 'price': price})

            elif key.startswith('gallery') and 'image' in key:
                index = key.split('[')[1].split(']')[0]
                image = value
                gallery_data.append({'image': image})  # ✅ Remove the extra comma

        
        print('specifications',specification_data)
        print('levels',level_data)
        print('sizes',size_data)
        print('gallery',gallery_data)
        self.save_nested_data(dish,SpecificationSerializer,specification_data)
        self.save_nested_data(dish,SpiceLevelSerializer,level_data)
        self.save_nested_data(dish,PortionSizeSerializer,size_data)
        self.save_nested_data(dish,GallerySerializer,gallery_data)
        # return super().perform_create(serializer)
        return Response({'message': 'Product Updated'}, status=status.HTTP_200_OK)

    def save_nested_data(self,dish_instance,serializer_class,data):
            serializer=serializer_class(data=data,many=True,context={'dish_instance':dish_instance})
            serializer.is_valid(raise_exception=True)
            serializer.save(dish=dish_instance)