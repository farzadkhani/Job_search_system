from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import (
    StaffRegisterCreateAPIView,
    JobSeekerRegisterCreateAPIView,
    EmployerRegisterCreateAPIView,
    LogoutGenericAPIView,
    CustomTokenObtainPairView,
)

urlpatterns = [
    path(
        "v1/staff-register/",
        StaffRegisterCreateAPIView.as_view(),
        name="v1_staff_register",
    ),
    path(
        "v1/jobseeker-register/",
        JobSeekerRegisterCreateAPIView.as_view(),
        name="v1_jobseeker_register",
    ),
    path(
        "v1/employer-register/",
        EmployerRegisterCreateAPIView.as_view(),
        name="v1_employer_register",
    ),
    path("v1/login/", CustomTokenObtainPairView.as_view(), name="v1_token_obtain_pair"),
    path("v1/token/refresh/", TokenRefreshView.as_view(), name="v1_token_refresh"),
    path("v1/logout/", LogoutGenericAPIView.as_view(), name="v1_logout"),
]
