from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import User
from django.db.models.fields import DateField
# from django.contrib.postgres.fields import ArrayField
# from django.contrib.gis.db import models
# Create your models here.


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, password, username, phone, first_name, last_name, gender, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')

        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, password, username, phone, first_name, last_name, gender, **other_fields)

    def create_user(self, email, password, username, phone, first_name, last_name, gender, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address.'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone=phone,
                          first_name=first_name, last_name=last_name, gender=gender, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone',
                       'first_name', 'last_name', 'gender']

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Document(models.Model):
    document_type = models.CharField(max_length=100)
    upload = models.FileField(upload_to='uploads')
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=False)


class Hospital(models.Model):
    address = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now_add=True)
    latitude = models.CharField(max_length=20, null=True)
    longitude = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.address


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True)
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    profile_pic = models.FileField(
        upload_to='uploads', default='static/images/default.png')
    created_date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200, null=True)
    dob = models.DateField(null=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, null=True)
    nationality = models.CharField(max_length=20, null=True)
    pit = models.CharField(max_length=20, null=True)
    poi = models.FileField(upload_to='uploads',
                           default='static/images/test.png')

    def __str__(self):
        return self.username


class Test(models.Model):
    test_name = models.CharField(max_length=200, null=True)
    marked_price = models.CharField(max_length=5, null=True)
    selling_price = models.CharField(max_length=5, null=True)

    def __str__(self):
        return self.test_name


class LabResult(models.Model):
    test_name = models.CharField(max_length=200, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    price = models.CharField(max_length=10, null=True)
    test_result = models.FileField(
        upload_to='tests', default='static/images/default.png')
    user_email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.user_email

class AddToCart(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=200, null=True)
    price = models.CharField(max_length=10, null=True)
    quantity = models.CharField(max_length=1, null=True)
    test_id = models.IntegerField(null=True)


class Order(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=200, null=True)
    total_amount = models.FloatField(null=True)
    ref_id = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=20, null=True)
    test_date = models.DateField(null=True)

    def __str__(self):
        return self.order_id

class Cart(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    total_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)


class ProductInCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " ProductInCart: " + str(self.id)

class VaccineBooking(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    ethnicity = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=50, null=True)
    dob = models.DateField(null=True)
    age = models.IntegerField(null=True)
    province = models.CharField(max_length=50, null=True)
    district = models.CharField(max_length=50, null=True)
    local_level_government = models.CharField(max_length=50,null=True)
    ward_no = models.IntegerField(null=True)
    nationality = models.CharField(max_length=50, null=True)
    identity_type = models.CharField(max_length=50, null=True)
    id_number = models.CharField(max_length=50, null=True)
    issue_office = models.CharField(max_length=50, null=True)
    occupation = models.CharField(max_length=50,  null=True)
    mobile = models.CharField(max_length=50, null=True)
    medical_condition = models.CharField(max_length=255, null=True)
    vaccination_center = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)