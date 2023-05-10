"""
This file defines dictionaries containing validation error messages and success messages
for the authentication app.
The FORGET_PASSWORD dictionary contains error messages for password validation,
while the RESET_PASSWORD dictionary contains success messages for various operations in the app.
"""
FORGET_PASSWORD = {
    'email': {
        'email_sent': 'Password reset email sent',
        'email_failed': 'Email verification failed',
        'email_not_exist': "Email does not exist",
        'link_expired': 'Forget password link expired. '
                        'Please submit the forget password form again.'
    },
}

RESET_PASSWORD = {
    'password_reset': {
        'successful': 'Password reset successful',
        'fail': 'Invalid password',
        'do_not_match': 'Passwords do not match'

    },
    'token': {
        'invalid': 'Invalid token',
        'expired': 'Your token has been expired',
    }
}