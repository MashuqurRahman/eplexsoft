from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from pos_app.models import pos_models
from django.apps import apps


ROLE_CHOICES = (
    ('', "--SELECT--"),
    ('central_admin', 'Central Admin'),
    ('section_admin', 'Category Admin'),
    ('employee', 'Employee'),
)

GENDER_CHOICES = (
    ('', "--SELECT--"),
    ('male', "Male"),
    ('female', "Female"),
    ('custom', "Custom")
)

USER_TYPE_CHOICES = (
    ('', "--SELECT--"),
    ('ecommerce', "E-commerce"),
    ('pos', "POS"),
    ('both', "Both"),
)
POS_ROLE_CHOICES = (
    ('', "--SELECT--"),
    ('central_admin', "Central Admin"),
    ('branch_admin', "Branch Admin"),
    ('regular_user', "Regular User"),
)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None 
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    numeric_validator = RegexValidator(r'^\+?\d+$', 'Only numeric digits (start with optional +) are allowed.')
    phone = models.CharField(max_length=20, validators=[numeric_validator], blank=True, null=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    category = models.ManyToManyField("admin_app.Categories", related_name='user_category', blank=True)
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES, blank=True, null=True)
    pos_role = models.CharField(max_length=100, choices=POS_ROLE_CHOICES, blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)
    active_status = models.BooleanField(default=True)
    pos_branch = models.ForeignKey(pos_models.BrachName, related_name='pos_user_branch', on_delete=models.CASCADE, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # no username required

    objects = UserManager()
    @property
    def user_company(self):
        from admin_app.models import admin_dashboard_models

        obj = admin_dashboard_models.SiteSetting.objects.first()
        if obj:
            return obj.company_name
        return "N/A"
    @property
    def user_permissions(self):
        userpermission_model = apps.get_model('permission_app', 'AdminPanelPermissions')
        permissions = userpermission_model.objects.filter(user=self).values_list("permission", flat=True)
        return list(permissions)
