from django.contrib.auth import get_user_model

from rest_framework import generics, permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    JobSeekerRegisterSerializer,
    EmployerRegisterSerializer,
    StaffRegisterSerializer,
    CustomTokenObtainPairSerializer,
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    LOGIN ROUTE (CustomTokenObtainPairView)

        **Permissions**
        ---------------
        - **Allow Any**: This endpoint is accessible to all users, including unauthenticated users, to allow login.

        **Request Method**
        ------------------
        - `POST`

        **URL Patterns**
        ----------------
        - **Endpoint**:
            ```
            /api/accounts/v1login/
            ```

        **Request Parameters**
        -----------------------
        - **Body Parameters**:
            - **`email`** (`str`, **Required**):
                - **Description**: Email address of the user.
            - **`password`** (`str`, **Required**):
                - **Description**: Password of the user.

        **Processing & Output**
        -----------------------
        1. **Validate Input Data**:
            - Ensures both `email` and `password` are provided.
        2. **Authenticate User**:
            - Checks if the user with the provided email exists and the password is correct.
        3. **Generate JWT Tokens**:
            - If authentication is successful, generates an access token and a refresh token.
        4. **Response Preparation**:
            - Returns the tokens along with additional user information as defined in the custom serializer.

        **Returns**
        ----------
        - **On Success**:
            - **Status Code**: `200 OK`
            - **Body**:
                ```json
                {
                    "refresh": "refresh_token_here",
                    "access": "access_token_here",
                    "username": "johndoe",
                    "email": "johndoe@example.com",
                    "usage_type": "JobSeeker"
                }
                ```

        - **On Failure**:
            - **Invalid Credentials**:
                ```json
                {
                    "detail": "No active account found with the given credentials"
                }
                ```
            - **Missing `email` or `password`**:
                ```json
                {
                    "email": ["This field is required."],
                    "password": ["This field is required."]
                }
                ```

        **Examples**
        -------------
        - **Success**:
            ```
            POST /api/accounts/v1/login/
            ```
            **Request Body**:
            ```json
            {
                "email": "johndoe@example.com",
                "password": "StrongPassword123!"
            }
            ```
            **Response**:
            ```json
            {
                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "username": "johndoe",
                "email": "johndoe@example.com",
                "usage_type": "JobSeeker"
            }
            ```

        - **Failure (Invalid Credentials)**:
            ```
            POST /api/accounts/v1/login/
            ```
            **Request Body**:
            ```json
            {
                "email": "johndoe@example.com",
                "password": "WrongPassword!"
            }
            ```
            **Response**:
            ```json
            {
                "detail": "No active account found with the given credentials"
            }
            ```

        **Test**
        --------
        - **Location in Test Suite**: `accounts/tests/test_api.py::`
        TODO: should implement tests

    """

    serializer_class = CustomTokenObtainPairSerializer


class StaffRegisterCreateAPIView(generics.CreateAPIView):
    """
    REGISTER ROUTE (StaffRegisterCreateAPIView)

        **Permissions**
        ---------------
        - **Allow Any**: This endpoint is accessible to all users, including unauthenticated users, to allow registration.

        **Request Method**
        ------------------
        - `POST`

        **URL Patterns**
        ----------------
        - **Endpoint**:
            ```
            /api/accounts/v1/staff-register/
            ```

        **Request Parameters**
        -----------------------
        - **Body Parameters**:
            - **`email`** (`str`, **Required**):
                - **Description**: Unique email address of the user.
            - **`password`** (`str`, **Required**):
                - **Description**: Password for the user account.
            - **`password2`** (`str`, **Required**):
                - **Description**: Confirmation of the password.

        **Processing & Output**
        -----------------------
        1. **Validate Input Data**:
            - Ensures all required fields (`email`, `password`, `password2`) are present and valid.
        2. **Check Passwords Match**:
            - Confirms that `password` and `password2` are identical.
        3. **Validate Password Strength**:
            - Utilizes Django's built-in password validators to ensure password strength.
        4. **Create User**:
            - Uses `UserManager.create_user` to create a new user instance with the provided data.
        5. **Save User**:
            - Saves the new user to the database.
        6. **Response Preparation**:
            - Returns the serialized user data (excluding password fields).

        **Returns**
        ----------
        - **On Success**:
            - **Status Code**: `201 Created`
            - **Body**:
                ```json
                {
                    "email": "johndoe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "usage_type": ""
                }
                ```

        - **On Failure**:
            - **Missing or Invalid `username`, `email`, `password`, `password2`**:
                ```json
                {
                    "email": ["This field is required."],
                    "password": ["This field is required."],
                    "password2": ["This field is required."]
                }
                ```
            - **Passwords Do Not Match**:
                ```json
                {
                    "password": "Password fields didn't match."
                }
                ```
            - **Password Validation Errors**:
                ```json
                {
                    "password": ["This password is too short. It must contain at least 8 characters."]
                }
                ```

        **Examples**
        -------------
        - **Success**:
            ```
            POST /api/accounts/v1/staff-register/
            ```
            **Request Body**:
            ```json
            {
                "email": "johndoe@example.com",
                "password": "StrongPassword123!",
                "password2": "StrongPassword123!",
                "usage_type": ""
            }
            ```
            **Response**:
            ```json
            {
                "email": "johndoe@example.com",
                "usage_type": ""
            }
            ```

        - **Failure (Passwords Do Not Match)**:
            ```
            POST /api/accounts/v1/staff-register/
            ```
            **Request Body**:
            ```json
            {
                "email": "johndoe@example.com",
                "password": "StrongPassword123!",
                "password2": "DifferentPassword456!",
                "usage_type": ""
            }
            ```
            **Response**:
            ```json
            {
                "password": "Password fields didn't match."
            }
            ```

        **Test**
        --------
        - **Location in Test Suite**: `accounts/tests/test_api.py::`
        TODO: should implement tests
    """

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = StaffRegisterSerializer


# TODO: implement rate limit
class EmployerRegisterCreateAPIView(generics.CreateAPIView):
    """
    REGISTER ROUTE (EmployerRegisterCreateAPIView)

        **Permissions**
        ---------------
        - **Allow Any**: This endpoint is accessible to all users, including unauthenticated users, to allow registration.

        **Request Method**
        ------------------
        - `POST`

        **URL Patterns**
        ----------------
        - **Endpoint**:
            ```
            /api/accounts/v1/employer-register/
            ```

        **Request Parameters**
        -----------------------
        - **Body Parameters**:
            - **`email`** (`str`, **Required**):
                - **Description**: Unique email address of the user.
            - **`password`** (`str`, **Required**):
                - **Description**: Password for the user account.
            - **`password2`** (`str`, **Required**):
                - **Description**: Confirmation of the password.

        **Processing & Output**
        -----------------------
        1. **Validate Input Data**:
            - Ensures all required fields (`email`, `password`, `password2`) are present and valid.
        2. **Check Passwords Match**:
            - Confirms that `password` and `password2` are identical.
        3. **Validate Password Strength**:
            - Utilizes Django's built-in password validators to ensure password strength.
        4. **Create User**:
            - Uses `UserManager.create_user` to create a new user instance with the provided data.
        5. **Save User**:
            - Saves the new user to the database.
        6. **Response Preparation**:
            - Returns the serialized user data (excluding password fields).

        **Returns**
        ----------
        - **On Success**:
            - **Status Code**: `201 Created`
            - **Body**:
                ```json
                {
                    "email": "johndoe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "usage_type": "Employer"
                }
                ```

        - **On Failure**:
            - **Missing or Invalid `username`, `email`, `password`, `password2`**:
                ```json
                {
                    "email": ["This field is required."],
                    "password": ["This field is required."],
                    "password2": ["This field is required."]
                }
                ```
            - **Passwords Do Not Match**:
                ```json
                {
                    "password": "Password fields didn't match."
                }
                ```
            - **Password Validation Errors**:
                ```json
                {
                    "password": ["This password is too short. It must contain at least 8 characters."]
                }
                ```

        **Examples**
        -------------
        - **Success**:
            ```
            POST /api/accounts/v1/employer-register/
            ```
            **Request Body**:
            ```json
            {
                "email": "johndoe@example.com",
                "password": "StrongPassword123!",
                "password2": "StrongPassword123!",
            }
            ```
            **Response**:
            ```json
            {
                "email": "johndoe@example.com",
                "usage_type": "Employer"
            }
            ```

        - **Failure (Passwords Do Not Match)**:
            ```
            POST /api/accounts/v1/employer-register/
            ```
            **Request Body**:
            ```json
            {
                "email": "johndoe@example.com",
                "password": "StrongPassword123!",
                "password2": "DifferentPassword456!",
                "usage_type": "JobSeeker"
            }
            ```
            **Response**:
            ```json
            {
                "password": "Password fields didn't match."
            }
            ```

        **Test**
        --------
        - **Location in Test Suite**: `accounts/tests/test_api.py::`
        TODO: should implement tests
    """

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = EmployerRegisterSerializer


# TODO: implement rate limit
class JobSeekerRegisterCreateAPIView(generics.CreateAPIView):
    """
    REGISTER ROUTE (JobSeekerRegisterCreateAPIView)

        **Permissions**
        ---------------
        - **Allow Any**: This endpoint is accessible to all users, including unauthenticated users, to allow registration.

        **Request Method**
        ------------------
        - `POST`

        **URL Patterns**
        ----------------
        - **Endpoint**:
            ```
            /api/accounts/v1/jobseeker-register/
            ```

        **Request Parameters**
        -----------------------
        - **Body Parameters**:
            - **`email`** (`str`, **Required**):
                - **Description**: Unique email address of the user.
            - **`password`** (`str`, **Required**):
                - **Description**: Password for the user account.
            - **`password2`** (`str`, **Required**):
                - **Description**: Confirmation of the password.

        **Processing & Output**
        -----------------------
        1. **Validate Input Data**:
            - Ensures all required fields (`email`, `password`, `password2`) are present and valid.
        2. **Check Passwords Match**:
            - Confirms that `password` and `password2` are identical.
        3. **Validate Password Strength**:
            - Utilizes Django's built-in password validators to ensure password strength.
        4. **Create User**:
            - Uses `UserManager.create_user` to create a new user instance with the provided data.
        5. **Save User**:
            - Saves the new user to the database.
        6. **Response Preparation**:
            - Returns the serialized user data (excluding password fields).

        **Returns**
        ----------
        - **On Success**:
            - **Status Code**: `201 Created`
            - **Body**:
                ```json
                {
                    "email": "johndoe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "usage_type": "JobSeeker"
                }
                ```

        - **On Failure**:
            - **Missing or Invalid `username`, `email`, `password`, `password2`**:
                ```json
                {
                    "email": ["This field is required."],
                    "password": ["This field is required."],
                    "password2": ["This field is required."]
                }
                ```
            - **Passwords Do Not Match**:
                ```json
                {
                    "password": "Password fields didn't match."
                }
                ```
            - **Password Validation Errors**:
                ```json
                {
                    "password": ["This password is too short. It must contain at least 8 characters."]
                }
                ```

        **Examples**
        -------------
        - **Success**:
            ```
            POST /api/accounts/v1/jobseeker-register/
            ```
            **Request Body**:
            ```json
            {
                "email": "johndoe@example.com",
                "password": "StrongPassword123!",
                "password2": "StrongPassword123!",
            }
            ```
            **Response**:
            ```json
            {
                "email": "johndoe@example.com",
                "usage_type": "JobSeeker"
            }
            ```

        - **Failure (Passwords Do Not Match)**:
            ```
            POST /api/accounts/v1/jobseeker-register/
            ```
            **Request Body**:
            ```json
            {
                "email": "johndoe@example.com",
                "password": "StrongPassword123!",
                "password2": "DifferentPassword456!",
            }
            ```
            **Response**:
            ```json
            {
                "password": "Password fields didn't match."
            }
            ```

        **Test**
        --------
        - **Location in Test Suite**: `accounts/tests/test_api.py::`
        TODO: should implement tests
    """

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = JobSeekerRegisterSerializer


# Logout View using Token Blacklisting
class LogoutGenericAPIView(generics.GenericAPIView):
    """
    LOGOUT ROUTE (LogoutGenericAPIView)

        **Permissions**
        ---------------
        - **Token Authentication Required**: Only authenticated users can access this endpoint to logout.

        **Request Method**
        ------------------
        - `POST`

        **URL Patterns**
        ----------------
        - **Endpoint**:
            ```
            /api/accounts/v1/logout/
            ```

        **Request Parameters**
        -----------------------
        - **Body Parameters**:
            - **`refresh`** (`str`, **Required**):
                - **Description**: Refresh token to be blacklisted, effectively logging out the user.

        **Processing & Output**
        -----------------------
        1. **Authenticate User**:
            - Ensures the request includes a valid access token in the `Authorization` header.
        2. **Retrieve Refresh Token**:
            - Extracts the `refresh` token from the request body.
        3. **Blacklist Refresh Token**:
            - Uses SimpleJWT's token blacklisting feature to blacklist the provided refresh token, preventing its future use.
        4. **Response Preparation**:
            - Returns a confirmation of successful logout.

        **Returns**
        ----------
        - **On Success**:
            - **Status Code**: `205 Reset Content`
            - **Body**: *(No content)*

        - **On Failure**:
            - **Missing or Invalid `refresh` Token**:
                ```json
                {
                    "refresh": ["This field is required."]
                }
                ```
            - **Token Blacklisting Error**:
                ```json
                {
                    "detail": "Token is invalid or expired"
                }
                ```

        **Examples**
        -------------
        - **Success**:
            ```
            POST /api/accounts/v1/logout/
            ```
            **Request Body**:
            ```json
            {
                "refresh": "refresh_token_here"
            }
            ```
            **Response**:
            ```
            HTTP 205 Reset Content
            ```

        - **Failure (Missing `refresh` Token)**:
            ```
            POST /api/accounts/v1/logout/
            ```
            **Request Body**:
            ```json
            {
                "refresh": ""
            }
            ```
            **Response**:
            ```json
            {
                "refresh": ["This field is required."]
            }
            ```

        - **Failure (Invalid `refresh` Token)**:
            ```
            POST /api/accounts/v1/logout/
            ```
            **Request Body**:
            ```json
            {
                "refresh": "invalid_refresh_token"
            }
            ```
            **Response**:
            ```json
            {
                "detail": "Token is invalid or expired"
            }
            ```

        **Test**
        --------
        - **Location in Test Suite**: `accounts/tests/test_api.py::`
        TODO: should implement tests
    """

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            # Assume the user has provided their refresh token in the request data
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
