from django.db import models
from shared_features.mixins import ModelMixin

from accounts.models import Company
from accounts.models import IndustryArea, JobSeeker
from shared_features.models import Skill
from .choices import APPLICATION_STATUS_CHOICES


class JobPosting(ModelMixin):
    """
    class that represents a job posting with relations to Company and IndustryArea
    """

    title = models.CharField(max_length=255)
    description = models.TextField()
    expiry_date = models.DateField()
    salary_range_start = models.PositiveIntegerField(null=True, blank=True)
    salary_range_end = models.PositiveIntegerField(null=True, blank=True)
    working_hours = models.CharField(max_length=50)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="job_posting_company"
    )
    industry_areas = models.ManyToManyField(
        IndustryArea, related_name="job_posting_industry_areas"
    )
    skills = models.ManyToManyField(Skill, related_name="job_posting_skills")
    # TODO: Use object storages and pass address
    active_photo = models.ForeignKey(
        "JobPostingPhoto",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="job_posting_active_photo",
        help_text="Current active photo for the job posting.",
    )

    class Meta:
        # indexing
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["company"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        TODO: index in elasticsearch
        """
        super().save(*args, **kwargs)


class JobPostingPhoto(ModelMixin):
    """
    class for storing JobPosting photos
    """

    job_posting = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name="job_posting_photo_job_posting",
    )
    file_path = models.ImageField(upload_to="job_posting_photos/")
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Photo for {self.job_posting.title}"

    def save(self, *args, **kwargs):
        # TODO: define signal for updating active_photo and deactivated old one
        if not self.pk:  # If creating a new photo
            # Set all other photos for this JobPosting to not active
            self.__class__.objects.filter(
                job_posting=self.job_posting, is_active=True
            ).update(is_active=False)
            self.is_active = True
        super().save(*args, **kwargs)

        # Update the JobPosting's active_photo
        if self.is_active:
            self.job_posting.active_photo = self
            self.job_posting.save()


class Application(ModelMixin):
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=APPLICATION_STATUS_CHOICES, default="Pending"
    )
    job_seeker = models.ForeignKey(
        JobSeeker, on_delete=models.CASCADE, related_name="applications_job_seeker"
    )
    job_posting = models.ForeignKey(
        JobPosting, on_delete=models.CASCADE, related_name="applications_job_posting"
    )

    def __str__(self):
        return f"Application by {self.job_seeker} for {self.job_posting}"
