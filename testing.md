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


## Issues and Solutions (Cart & Checkout Implementation)

### 1. Site Configuration Error
**Issue:** Site matching query does not exist error when accessing login page
**Solution:** 
- Created management command to ensure site exists
```python
# accounts/management/commands/create_default_site.py
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if Site.objects.exists():
            Site.objects.all().delete()
        Site.objects.create(
            id=1,
            domain='127.0.0.1:8000',
            name='Clean Services Platform'
        )
```

### 2. Profile Data Not Loading in Checkout
**Issue:** User profile data not pre-filling checkout form
**Solution:**
- Added UserProfile import to checkout views
- Updated checkout view to pull profile data
```python
# checkout/views.py
from accounts.models import UserProfile  # Changed from profiles to accounts

if request.user.is_authenticated:
    try:
        profile = UserProfile.objects.get(user=request.user)
        order_form = OrderForm(initial={
            'full_name': profile.user.get_full_name(),
            'email': profile.user.email,
            'phone_number': profile.default_phone_number,
            # ... other fields
        })
```

### 3. Admin Interface Profile Visibility
**Issue:** Admin couldn't see user profile details
**Solution:**
- Added inline admin configuration for UserProfile
```python
# accounts/admin.py
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'last_login')
```

### 4. Order-Profile Relationship
**Issue:** Orders not linked to user profiles
**Solution:**
- Added UserProfile relationship to Order model
```python
# checkout/models.py
class Order(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
```

### 5. Module Import Error
**Issue:** ModuleNotFoundError: No module named 'profiles'
**Solution:**
- Fixed import statement in checkout views
- Changed from `profiles.models` to `accounts.models`
- Updated related imports across the project

### 6. Migration Conflicts
**Issue:** Conflicting migrations in accounts app
**Solution:**
- Removed conflicting migration files
- Created new migration for site creation
- Applied migrations in correct order:
```bash
python manage.py migrate sites
python manage.py migrate accounts
python manage.py migrate
```

### 7. Cart Price Formatting
**Issue:** Tax and Total amounts in cart showing too many decimal places
**Solution:**
- Updated Cart class to use Decimal quantize with ROUND_HALF_UP
- Added template filters for display formatting
```python
# cart/cart.py
from decimal import Decimal, ROUND_HALF_UP

def get_tax(self):
    """Calculate tax amount."""
    tax = self.get_subtotal_price() * Decimal(settings.TAX_RATE)
    return tax.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
```

```html
<!-- cart/templates/cart/detail.html -->
<td colspan="2">
    <strong>£{{ cart.get_tax|floatformat:2 }}</strong>
</td>
```

The changes:
- Added ROUND_HALF_UP 
- Used quantize to ensure 2 decimal places in calculations
- Added floatformat:2 filter in templates
- Applied to subtotal, tax, and total amounts

### 8. Profile Update on Checkout
**Issue:** Profile address not updating when selecting "Update profile" in checkout
**Solution:**
- Fixed session handling of save_info flag
- Updated checkout success view to properly handle profile updates
```python
# checkout/views.py
def checkout_success(request, order_number):
    save_info = request.session.get('save_info')
    if request.user.is_authenticated and save_info:
        profile = UserProfile.objects.get(user=request.user)
        profile.default_phone_number = order.phone_number
        profile.default_street_address1 = order.street_address1
        # ... other fields ...
        profile.save()
```

### 9. Checkout Form Save Info Checkbox
**Issue:** Confusing "False" label on save info checkbox
**Solution:**
- Updated checkbox label and styling
- Added help text for clarity
```html
<!-- checkout/templates/checkout/checkout.html -->
<div class="form-check">
    <input class="form-check-input" type="checkbox" name="save_info" 
           id="id_save_info" checked>
    <label class="form-check-label" for="id_save_info">
        Update my profile with this delivery information
    </label>
    <small class="form-text text-muted">
        Check this box to update your saved delivery information
    </small>
</div>
```

### 10. Session Cleanup
**Issue:** Save info preference persisting in session
**Solution:**
- Added session cleanup after successful checkout
```python
# checkout/views.py
def checkout_success(request, order_number):
    # ... process order ...
    if 'save_info' in request.session:
        del request.session['save_info']
```

### 11. Stripe Postal Code Field
**Issue:** US ZIP code format conflicting with UK postcodes
**Solution:**
- Disabled Stripe's postal code field
- Used our own postcode field instead
```javascript
// checkout/static/checkout/js/stripe_elements.js
var card = elements.create('card', {
    style: style,
    hidePostalCode: true,
    zipCode: false
});

stripe.confirmCardPayment(clientSecret, {
    payment_method: {
        card: card,
        billing_details: {
            address: {
                postal_code: null
            }
        }
    }
});
```


