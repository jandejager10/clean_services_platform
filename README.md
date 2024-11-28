# Clean Services Platform

A comprehensive platform for managing cleaning services and products, built with Django.

## Features

### Home
- Landing page with service overview
- Quick access to quotes and booking
- Featured services showcase
- Featured cleaning products section
- Company information section

### Services
- Complete service catalog
- Category-based organization:
  - Residential Cleaning
  - Commercial Cleaning
  - Deep Cleaning
  - Move-In/Move-Out Cleaning
  - Post-Renovation Cleaning
  - Recurring Services
- Service filtering and search
- Detailed service pages
- Booking functionality

### Products
- Complete cleaning products catalog
- Category-based organization:
  - Floor Cleaning Tools
  - Wet Work Tools
  - All-Purpose Tools
  - Common Cleaning Products
  - Personal Protection
  - Commercial Cleaning Supplies
  - Household Cleaning Supplies
- Product filtering and search
- Detailed product pages
- Admin product management
- Featured product categories:
  - Cleaning Tools
  - Detergents
  - Disinfectants

### FAQ
- Categorized FAQ sections
- Searchable questions and answers
- Easy navigation between categories
- Dynamic content loading

## Technical Details

### Apps
1. Home
   - Main landing page
   - About page
   - Contact functionality

2. Services
   - Service catalog
   - Category management
   - Service details
   - Booking system

3. Products
   - Product catalog
   - Category management
   - Product details
   - Admin CRUD functionality
   - Image handling

4. FAQ
   - FAQ categories
   - Question management
   - Search functionality

### Models
- Category (Services)
- Service
- Category (Products)
- Product
- FAQCategory
- FAQItem

### Features
- Responsive design
- Bootstrap 5 integration
- Custom CSS styling
- Dynamic content loading
- Search functionality
- Category filtering
- Interactive UI elements
- Image upload handling
- Admin product management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/clean_services_platform.git
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Load fixture data:
```bash
python manage.py loaddata service_categories
python manage.py loaddata service_products
python manage.py loaddata product_categories
python manage.py loaddata product_list
python manage.py loaddata faq_data
```

6. Run the development server:
```bash
python manage.py runserver
```

## Dependencies
- Django
- Python 3.8+
- Bootstrap 5
- Pillow (for image handling)
- Font Awesome 5

## Project Structure
```
clean_services_platform/
├── home/
├── services/
│   ├── fixtures/
│   ├── static/
│   └── templates/
├── products/
│   ├── fixtures/
│   ├── static/
│   └── templates/
├── faq/
├── static/
└── templates/
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.