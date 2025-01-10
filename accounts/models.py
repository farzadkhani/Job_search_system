from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from shared_features.mixins import ModelMixin, SoftDeleteMixinManager
from shared_features.models import Skill
from .choices import USAGE_TYPE_CHOICES, GENDER_CHOICES, EDUCATION_CHOICES


class UserManager(BaseUserManager, SoftDeleteMixinManager):
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
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("usage_type") != None:
            raise ValueError("Superuser must have usage_type=none.")
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
    usage_type = models.CharField(
        max_length=10,
        choices=USAGE_TYPE_CHOICES,
        help_text="Type of user (JobSeeker or Employer).",
        null=True,
        blank=True,
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
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text="Designates that this user has all permissions without explicitly assigning them.",
    )
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Address(ModelMixin):
    """
    Address model for reverse related in JobSeeker and Company.
    generic relation with JobSeeker or Company.
    """

    address_text = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    city = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        unique_together = ("content_type", "object_id")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return f"{self.address_text}, {self.city}"

    # TODO: prevent each user have more than one active address


class JobSeeker(ModelMixin):
    """
    JobSeeker model with relation to User and Address.
    """

    user = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name="job_seeker_user"
    )
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES, null=True, blank=True
    )
    education = models.CharField(
        max_length=100, choices=EDUCATION_CHOICES, null=True, blank=True
    )

    active_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="job_seeker_active_address",
    )
    skills = models.ManyToManyField(Skill, related_name="job_seekers_skills")

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
        User, on_delete=models.CASCADE, related_name="company_user"
    )
    active_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="company_active_address",
    )
    industry_areas = models.ManyToManyField(
        IndustryArea, related_name="company_industry_areas"
    )

    def __str__(self):
        return self.name
