from django.contrib import admin


from .models import JobPosting, JobPostingPhoto, Application

admin.site.register(JobPosting)
admin.site.register(JobPostingPhoto)
admin.site.register(Application)
