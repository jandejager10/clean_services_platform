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

