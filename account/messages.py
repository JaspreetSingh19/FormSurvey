"""
This file defines dictionaries containing validation error messages and success messages
for the account app.
The VALIDATION dictionary contains error messages for form validation,
while the SUCCESS_MESSAGES dictionary contains success messages for various operations in the app.
"""
SIGNUP_VALIDATION_ERROR = {
    'first_name': {
        "blank": "first name can not be blank",
        "invalid": "first name must contain only alphabets",
        "required": "first name required",
    },
    'last_name': {
        "blank": "last name can not be blank",
        "invalid": "last name must contains only alphabets",
        "required": "last name required",
    },
    'username': {
        "blank": "username can not be blank",
        "invalid": "username must contain alphabet and special character",
        "required": "username required",
        "exists": "username already exist"
    },
    'email': {
        "blank": "Email can not be blank",
        "required": "Email required",
        "exists": "email already exist"
    },
    'contact': {
        "blank": "contact can not be blank",
        "required": "contact required",
        "invalid": "invalid contact"
    },
    'password': {
        "blank": "password can not be blank",
        "invalid": "Password must contain uppercase, lowercase, digit and special character",
        "required": "password required"
    },

}

SIGNUP_MESSAGE = {
    'created': "Account created successfully",
    'email': "A set password email has been send to this email",
    'delete': "User Deleted Successfully"
}

SIGNIN_VALIDATION_ERROR = {
    'username': {
        "blank": "username can not be blank",
        "invalid": "username must contain alphabet and special character",
        "required": "username required",
        "exits": "username already exist"
    },
    'password': {
        "blank": "password can not be blank",
        "invalid": "Password must contain uppercase, lowercase, digit and special character",
        "required": "password required"
    },
    "invalid credentials": "Invalid Credentials",
}

SET_PASSWORD_VALIDATION = {
    'exists': "User has already set his password",
    'time': "A set password link has already send to this email"
}

TOKEN_ERROR = {
    'Invalid': "Invalid Token",
    'Expired': "Your link has been expired"
}

SUCCESS_MESSAGE = {
    'success': "Updated Successfully"
}

ERROR_MESSAGE = {
    'error': "Update Failed"
}

PASSWORD_MESSAGE = {
    'Success': "Password set successfully",
    'failed': "Password set failed"
}

EMAIL_SEND = {
    'success': "The link has been send to this email",
    'failed': "Link send failed"
}

