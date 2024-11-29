# Testing Documentation

## FAQ Fixture Data Loading Issue

### Problem
When attempting to load the FAQ fixture data, the following error occurred:
```bash
django.db.utils.IntegrityError: NOT NULL constraint failed: faq_faqcategory.created_at
```

### Solution
The issue was caused by the `created_at` field in the `FAQCategory` model not being set to a default value. To fix this, the `created_at` field was set to a default value of `now()` in the fixture data. 

The fixture data was updated and loaded successfully.

## ImageField Dependency Issue

### Problem
When running the development server, the following error occurred:
```bash
django.core.management.base.SystemCheckError: SystemCheckError: System check identified some issues:

ERRORS:
services.Service.image: (fields.E210) Cannot use ImageField because Pillow is not installed.
        HINT: Get Pillow at https://pypi.org/project/Pillow/ or run command "python -m pip install Pillow".
```

### Cause
The `Service` model uses Django's `ImageField`, which requires the Pillow library for image processing. This dependency was not installed in the virtual environment.

### Solution
Installed the Pillow library using pip:
```bash
python -m pip install Pillow
```

After installing Pillow, the development server ran successfully.

## Accounts App Implementation

### 1. Django Allauth Installation
**Issue:** ModuleNotFoundError: No module named 'accounts.apps'
**Solution:** 
- Created apps.py in accounts directory
- Added proper app configuration
- Created signals.py for user profile creation
```python
# accounts/apps.py
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals
```

### 2. Email Configuration
**Issue:** SMTPSenderRefused error when trying to send verification emails
**Solution:**
- Updated email settings in settings.py
- Created app-specific password in Gmail
- Updated environment variables
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

### 3. Template Rendering
**Issue:** Invalid filter: 'crispy'
**Solution:**
- Installed django-crispy-forms and crispy-bootstrap5
- Added to INSTALLED_APPS
- Added crispy forms configuration
```python
# settings.py
INSTALLED_APPS = [
    ...
    'crispy_forms',
    'crispy_bootstrap5',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
```

### 4. User Profile Creation
**Issue:** Profile not automatically created for new users
**Solution:**
- Moved signal from models.py to dedicated signals.py
- Ensured signal registration in apps.py
```python
# accounts/signals.py
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
```

### 5. Authentication Flow
**Issue:** Incorrect redirect after login/logout
**Solution:**
- Added proper redirect settings in settings.py
```python
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

### 6. Form Styling
**Issue:** Inconsistent form styling across templates
**Solution:**
- Created consistent CSS classes
- Added to auth templates
```css
.auth-card {
    border: none;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    border-radius: 10px;
}

.auth-card .card-header {
    background-color: var(--primary-color);
    color: white;
}
```

### 7. Dependencies
**Issue:** Missing required packages
**Solution:**
- Updated requirements.txt with all necessary packages
```plaintext
django-allauth==65.2.0
django-crispy-forms==2.1
crispy-bootstrap5==2024.2
```

### 8. Environment Variables
**Issue:** Email configuration not working in production
**Solution:**
- Updated .env file with correct variables
- Ensured proper loading in settings.py
```plaintext
EMAIL_HOST_USER=cleanservicesplatform@gmail.com
EMAIL_HOST_PASSWORD=my-app-password
```

### Recommendations
1. Always test email functionality in development using console backend
2. Use environment variables for sensitive information
3. Keep authentication templates consistent with site design
4. Implement proper error handling for auth flows
5. Test all authentication paths (login, logout, signup, password reset)
6. Ensure proper signal handling for user profile creation
7. Maintain consistent styling across all auth templates

### Future Improvements
1. Add social authentication
2. Implement enhanced password policies
3. Add two-factor authentication
4. Create custom email templates
5. Add user profile completion tracking
6. Implement account deletion functionality

