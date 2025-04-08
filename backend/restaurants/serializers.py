
from rest_framework import serializers
from .models import Restaurant
from account.serializers import UserSerializer
class RestaurantCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Restaurant
        fields = '__all__'

    def validate(self, data):
        """
        Custom validation logic for creating a Restaurant
        """
        # Ensure that latitude and longitude are either both present or both absent
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        if (latitude and not longitude) or (longitude and not latitude):
            raise serializers.ValidationError("Both latitude and longitude must be provided together.")

        # Validate operational hours (opening_time should be before closing_time)
        if data['opening_time'] >= data['closing_time']:
            raise serializers.ValidationError("Opening time must be earlier than closing time.")

        return data

        
    def __init__(self, *args, **kwargs):
        super(RestaurantCreateSerializer, self).__init__(*args, **kwargs)
        # Customize serialization depth based on the request method.
        request = self.context.get('request')
        if request and request.method == 'POST':
            # When creating a new cart order, set serialization depth to 0.
            self.Meta.depth = 0
        else:
            # For other methods, set serialization depth to 3.
            self.Meta.depth = 3


    # def create(self, validated_data):
    #     """
    #     Create a new Restaurant instance
    #     """
    #     # Create the Restaurant object using the validated data
    #     restaurant = Restaurant.objects.create(**validated_data)
    #     return restaurant
    


# class VendorSerializer(serializers.ModelSerializer):
#     # Serialize related CartOrderItem models
#     user = UserSerializer(read_only=True)

#     class Meta:
#         model = Vendor
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(VendorSerializer, self).__init__(*args, **kwargs)
#         # Customize serialization depth based on the request method.
#         request = self.context.get('request')
#         if request and request.method == 'POST':
#             # When creating a new cart order, set serialization depth to 0.
#             self.Meta.depth = 0
#         else:
#             # For other methods, set serialization depth to 3.
#             self.Meta.depth = 3


    # def __init__(self,*args, **kwargs):
    #     super(RestaurantCreateSerializer,self).__init__(*args, **kwargs)
    #     request=self.context.get("request")
    #     if request and request.method == "POST":
    #         self.Meta.depth=0
    #     else:
    #         self.Meta.depth=3

# class RestaurantSerializer(serializers.ModelSerializer):
#     # Custom fields for displaying certain data or validation if needed
#     image_url = serializers.SerializerMethodField()  # For returning the full image URL

#     class Meta:
#         model = Restaurant
#         fields = [
#             'id', 'name', 'description', 'phone_number', 'email', 'website', 'image', 
#             'image_url', 'latitude', 'longitude', 'address', 'city', 'state', 'zip_code',
#             'opening_time', 'closing_time', 'is_open', 'max_delivery_distance_km',
#             'created_at', 'updated_at'
#         ]

#     def get_image_url(self, obj):
#         """Return the full image URL for the restaurant image"""
#         request = self.context.get('request')
#         if obj.image:
#             return request.build_absolute_uri(obj.image.url)
#         return None

#     def validate_max_delivery_distance_km(self, value):
#         """Ensure that the max delivery distance is a reasonable value"""
#         if value <= 0:
#             raise serializers.ValidationError("Max delivery distance must be greater than 0.")
#         return value
