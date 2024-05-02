
# ADHD Project

- Registration has been added

- Login and logout has been added

- Done the Reset Password through Email

- Social Auth config has been added

- Create & List API Views for tasks in patients have been added

# Registration

## Doctor Registration Endpoint

### Endpoint URL

- **URL:**  `http://127.0.0.1:8000/doctor/register/`

- **Method:**  `POST`

- **Content-Type:**  `application/json`

### Request Body Parameters

- `username` (string, required): The desired username for the new doctor account.

- `email` (string, required): The email address for the new doctor account.

- `password` (string, required): The password for the new doctor account.

- `password2` (string, required): The confirmation of the password.

#### Response

    {
    
    "response": "Account for Doctor has been created",
    
    "username": "omar",
    
    "email": "omar@omar.com",
    
    "token": "J2E9G5gDd3SwZtCDOzvEiiWyR9WX09",
    
    "refresh_token": "iweDaxcDmE8Qx2n2Tc2e1RGgtl7Oim",
    
    "expires": "2033-12-13T19:36:29.357345Z"
    
    }

## Patient Registration Endpoint

### Endpoint URL

- **URL:**  `http://127.0.0.1:8000/patient/register/`

- **Method:**  `POST`

- **Content-Type:**  `application/json`

### Request Body Parameters

- `username` (string, required): The desired username for the new patient account.

- `email` (string, required): The email address for the new patient account.

- `password` (string, required): The password for the new patient account.

- `password2` (string, required): The confirmation of the password.

#### Response

    {
    
    "response": "Account for Patient has been created",
    
    "username": "john",
    
    "email": "john@example.com",
    
    "token": "A3B5C7E9G1I3K5M7",
    
    "refresh_token": "R1E3F5R7E9S1H3",
    
    "expires": "2033-12-13T19:36:29.357345Z"
    
    }

## Login

### Endpoint URL

- **URL:**  `http://127.0.0.1:8000/auth/token`

- **Method:**  `POST`

- **Content-Type:**  `application/x-www-form-urlencoded`

### Request Body Parameters

- `username` (string, required): The username of the user.

- `password` (string, required): The password of the user.

- `grant_type` (string, required): The grant type, typically set to "password" in this scenario.

- `client_id` (string, required): The client ID associated with the application.

- `client_secret` (string, required): The client secret associated with the application.

#### Response

    {

    "access_token": "vwDrDrqLi1bopyYsHfq1xu2MO7TnpP",
    
    "expires_in": 3600,
    
    "token_type": "Bearer",
    
    "scope": "read write",
    
    "refresh_token": "CtHisFbhBiKfvJ3aZF53HVjVLMrOlE"

}

## Password Reset

### Endpoint URL

- **URL:**  `http://127.0.0.1:8000/api/password_reset/`

- **Method:**  `POST`

- **Content-Type:**  `application/json`

### Request Body Parameters

- `email` (string, required): The email address of the user for whom a password reset is requested.

#### Response

    {  "status":  "OK"  }

## Password Reset Confirmation Endpoint

### Endpoint URL

- **URL:**  `http://127.0.0.1:8000/api/password_reset/confirm/`

- **Method:**  `POST`

- **Content-Type:**  `application/json`

### Request Body Parameters

- `password` (string, required): The new password to set.

- `token` (string, required): The token received during the password reset request.

#### Response

    {  "status":  "OK"  }

## Token Conversion Endpoint for social auth

### Endpoint URL

- **URL:**  `http://127.0.0.1:8000/auth/convert-token`

- **Method:**  `POST`

- **Content-Type:**  `application/x-www-form-urlencoded`

### Request Body Parameters

- `token` (string, required): The token to be converted.

- `backend` (string, required): The authentication backend to use for conversion (e.g., "google-oauth2", "apple").

- `grant_type` (string, required): The grant type, typically set to "convert_token" in this scenario in **Google** it will be `google-oauth2`  in **Facebook** will be `facebook` in **Apple** will be `apple`

- `client_id` (string, required): The client ID associated with the application.

- `client_secret` (string, required): The client secret associated with the application.

#### Response

    {
    
    "access_token": "vwDrDrqLi1bopyYsHfq1xu2MO7TnpP",
    
    "expires_in": 3600,
    
    "token_type": "Bearer",
    
    "scope": "read write",
    
    "refresh_token": "CtHisFbhBiKfvJ3aZF53HVjVLMrOlE"
    
    }
