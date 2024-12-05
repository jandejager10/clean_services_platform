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

### Shopping Cart
- Session-based cart storage
- Add/remove products
- Update quantities
- Tax calculation (20%)
- Subtotal and total calculations
- Persistent across sessions
- Real-time price updates

### Checkout
- Secure payment processing with Stripe
- Order summary
- Profile data auto-fill
- Email confirmations with detailed invoice
- Order history
- Webhook handling
- Automatic tax calculation
- Order total calculations
- Billing information storage

### Authentication & User Management
- User registration with email verification
- Login/Logout functionality
- Password reset capability
- User profile management
- Secure authentication flows
- Custom styled authentication templates
- Profile information storage
- Address management

### FAQ
- Categorized FAQ sections
- Searchable questions and answers
- Easy navigation between categories
- Dynamic content loading

### Service Booking System

The site now includes a booking system for services:

#### Features
- Calendar-based booking interface
- Time slot selection
- Booking status management (pending, confirmed, cancelled, completed)
- Staff approval workflow
- Email notifications for booking events
- Staff management interface
- Interactive calendar with event details
- Status-specific color coding
- Tooltips with booking information

#### Booking Process
1. Customer selects a service
2. Chooses available date and time slot
3. Submits booking request
4. Receives pending confirmation email
5. Staff reviews and confirms/rejects booking
6. Customer receives final confirmation/rejection email

#### Staff Features
- Dedicated staff menu in navigation
- Pending bookings counter
- Booking management interface
- Ability to confirm or reject bookings
- Access to all booking details
- Calendar view with customer details
- Quick access to booking management
- Streamlined approval workflow

#### Email Notifications
The system sends HTML emails for:
- Booking requests (pending)
- Booking confirmations
- Booking cancellations
- Order confirmations with invoice

#### Email Features
- Professional HTML formatting
- Detailed order/booking information
- Billing address details
- Line item breakdown
- Tax calculations
- Total summaries
- Responsive design for all devices

#### Calendar Features
- Interactive event display
- Status-based color coding
- Hover tooltips with details
- Click-through to booking details
- Staff/User specific views
- Booking time slot selection

#### Technical Details
- Built using Django's class-based views
- FullCalendar.js integration
- REST API endpoints for calendar events
- Custom management commands for time slots
- Staff-specific decorators for access control

#### Dependencies Added
```
djangorestframework==3.15.2
```

#### Environment Variables
```
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=the-app-specific-password
```

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

4. Cart
   - Session management
   - Price calculations
   - Quantity updates
   - Tax handling

5. Checkout
   - Payment processing
   - Order management
   - Email notifications
   - Webhook handling

6. Accounts
   - User authentication
   - Profile management
   - Email verification
   - Address storage
   - Custom templates

7. FAQ
   - FAQ categories
   - Question management
   - Search functionality

### Models
- Category (Services)
- Service
- Category (Products)
- Product
- UserProfile
- Order
- OrderLineItem
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
- Email verification
- User authentication
- Profile management
- Shopping cart
- Secure payments
- Order tracking

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

6. Create initial calendar time slots:
```bash
python manage.py create_timeslots
```

7. Configure email settings in .env:
```plaintext
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=the-app-password
```

8. Run the development server:
```bash
python manage.py runserver
```

## Dependencies
- Django
- Python 3.8+
- Bootstrap 5
- Pillow (for image handling)
- Font Awesome 5
- Django Allauth
- Django Crispy Forms
- Crispy Bootstrap5
- Stripe

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
├── cart/
│   ├── static/
│   └── templates/
├── checkout/
│   ├── static/
│   │   ├── js/
│   │   └── css/
│   └── templates/
├── accounts/
│   ├── templates/
│   │   └── account/
│   ├── static/
│   └── migrations/
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