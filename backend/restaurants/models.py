from django.db import models
from account.models import User
from django.utils.text import slugify

class Restaurant(models.Model):
    # Basic information
    user = models.OneToOneField(User, on_delete=models.SET_NULL,null=True,default=1) 
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True,null=True, )
    image = models.ImageField(upload_to='restaurants/', blank=True)
    slug=models.SlugField(max_length=500)
    # Location tracking
    latitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True,)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True,null=True,)
    address = models.CharField(max_length=255,blank=True,null=True,)
    city = models.CharField(max_length=100,blank=True,null=True,)
    state = models.CharField(max_length=100,blank=True,null=True,)
    zip_code = models.CharField(max_length=10,blank=True,null=True,)

    # Operational hours
    opening_time = models.TimeField(null=True,blank=True)
    closing_time = models.TimeField(null=True,blank=True)

    # Additional settings
    is_open = models.BooleanField(default=True)
    max_delivery_distance_km = models.DecimalField(max_digits=5, decimal_places=2, default=10.00,blank=True,null=True,)  # Max distance for delivery in km

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    def save(self,*args, **kwargs):
        if self.slug==""or self.slug ==None:
            self.slug=slugify(self.name)
        super().save(*args, **kwargs)


# class Vendor(models.Model):
#     user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name="vendor")
#     image = models.ImageField(upload_to=user_directory_path, default="shop-image.jpg", blank=True)
#     name = models.CharField(max_length=100, help_text="Shop Name", null=True, blank=True)
#     email = models.EmailField(max_length=100, help_text="Shop Email", null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     mobile = models.CharField(max_length = 150, null=True, blank=True)
#     verified = models.BooleanField(default=False)
#     active = models.BooleanField(default=True)
#     vid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
#     date = models.DateTimeField(auto_now_add=True)
#     slug = models.SlugField(blank=True, null=True)

#     class Meta:
#         verbose_name_plural = "Vendors"

#     def vendor_image(self):
#         return mark_safe('  <img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.shop_image.url))

#     def __str__(self):
#         return str(self.name)
        

#     def save(self, *args, **kwargs):
#         if self.slug == "" or self.slug == None:
#             self.slug = slugify(self.name)
#         super(Vendor, self).save(*args, **kwargs) 




# class MenuItem(models.Model):
#     restaurant = models.ForeignKey(Restaurant, related_name='menu_items', on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     image = models.ImageField(upload_to='menu_items/', blank=True)
#     is_available = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Menu Item"
#         verbose_name_plural = "Menu Items"


# class Order(models.Model):
#     restaurant = models.ForeignKey(Restaurant, related_name='orders', on_delete=models.CASCADE)
#     customer_name = models.CharField(max_length=255)
#     customer_phone = models.CharField(max_length=15)
#     customer_address = models.CharField(max_length=255)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Order #{self.id} from {self.restaurant.name}"

#     class Meta:
#         verbose_name = "Order"
#         verbose_name_plural = "Orders"


# class Delivery(models.Model):
#     order = models.OneToOneField(Order, on_delete=models.CASCADE)
#     rider_name = models.CharField(max_length=255)
#     rider_phone = models.CharField(max_length=15)
#     status = models.CharField(max_length=50, choices=[
#         ('pending', 'Pending'),
#         ('on_the_way', 'On the Way'),
#         ('delivered', 'Delivered'),
#         ('canceled', 'Canceled'),
#     ])
#     current_latitude = models.DecimalField(max_digits=9, decimal_places=6)
#     current_longitude = models.DecimalField(max_digits=9, decimal_places=6)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Delivery for Order #{self.order.id} by {self.rider_name}"

#     class Meta:
#         verbose_name = "Delivery"
#         verbose_name_plural = "Deliveries"
