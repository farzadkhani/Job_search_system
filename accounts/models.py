from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from django.db.models import Q

from shared_features.models import ModelMixin
from .choices import USER_TYPE_CHOICES


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("user_type", "SuperUser")
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("user_type") != "SuperUser":
            raise ValueError("Superuser must have user_type=SuperUser.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, ModelMixin):
    """
    Custom user model inheriting from AbstractBaseUser and PermissionsMixin.
    Uses email as the unique identifier.
    """

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
    )
    email = models.EmailField(unique=True, help_text="Required. Unique email address.")
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default="JobSeeker",
        help_text="Type of user (JobSeeker or Employer).",
    )
    first_name = models.CharField(
        max_length=150, blank=True, help_text="User's first name."
    )
    last_name = models.CharField(
        max_length=150, blank=True, help_text="User's last name."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Address(ModelMixin):
    """
    Address model for reverse related in JobSeeker and Company.
    """

    address_text = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address_text}, {self.city}"
    
    # TODO: prevent each user have more than one active address


class JobSeeker(ModelMixin):
    """
    JobSeeker model with relation to User and Address.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="job_seeker_profile"
    )
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=20)
    education = models.CharField(max_length=100)
    addresses = models.ManyToManyField(Address, related_name="job_seekers")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class FileStore(ModelMixin):
    """
    FileStore model for storing files for JobSeeker.
    """
    file_path = models.FileField(upload_to="files/")
    is_active = models.BooleanField(default=True)
    job_seeker = models.ForeignKey(
        JobSeeker,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="file_stores",
    )

    def __str__(self):
        return self.file_path.name


class IndustryArea(ModelMixin):
    """
    class for store industry areas of companies
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Company(ModelMixin):
    """
    Company model with relation to User,  Address and IndustryArea.
    """
    name = models.CharField(max_length=255)
    establishment_year = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=20)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="company_profile"
    )
    addresses = models.ManyToManyField(Address, related_name="companies")
    industry_areas = models.ManyToManyField(IndustryArea, related_name="companies")

    def __str__(self):
        return self.name
