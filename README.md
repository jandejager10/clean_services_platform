# CodInstProj4
Full Stack Development Final Project for Code Institute

# Clean Services and Supplies Platform

## Overview
The **Clean Services and Supplies Platform** is a web application that offers a comprehensive solution for individuals and businesses to book professional cleaning services and purchase high-quality cleaning products. The platform caters to various user needs, including eco-friendly options, subscription services, and flexible booking for home and business cleaning.

## Target Users
- **Homeowners and Renters**: Individuals needing regular or one-time cleaning services and access to cleaning products.
- **Busy Professionals**: Users with limited time who prefer outsourcing cleaning services for convenience.
- **Environmentally Conscious Consumers**: Customers who prefer eco-friendly cleaning products and services.
- **Property Managers and Landlords**: Professionals managing multiple properties who need bulk services and products.
- **Families with Young Children or Pets**: Families looking for child-safe and pet-friendly products and specialized cleaning services.
- **Small Business Owners**: Owners of small businesses requiring commercial cleaning services or products.

## Key Features
### For Users
- **Browse and Purchase Cleaning Products**: Users can browse a wide range of cleaning supplies, including eco-friendly and specialized options.
- **Book Cleaning Services**: Users can book services such as deep cleaning, move-in/move-out cleaning, and more, with flexible scheduling options.
- **Subscription Plans**: Users can subscribe to regular cleaning services (e.g., weekly or bi-weekly) at discounted rates.
- **User Accounts**: Users can register, log in, and manage their profiles, including viewing order history, managing subscriptions, and saving payment methods.
- **Review and Rating System**: Users can rate and review both products and services, providing feedback for improvement.

### For Admins
- **Product and Service Management**: Admins can add, edit, or remove products and services from the platform.
- **Booking Management**: Admins can approve, reject, and manage service bookings.
- **Sales Reports**: Admins can generate and view sales reports for products and services.
- **User Management**: Admins can manage user accounts, including banning or deactivating users when necessary.
- **Promotions and Discounts**: Admins can create and manage promotional offers and discount codes.

## Technologies Used
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Backend**: Python, Django, Django REST Framework (for API development)
- **Database**: SQLite (for local development) and PostgreSQL (for deployment)
- **Payments**: Stripe (for secure transactions)
- **Version Control**: Git (GitHub for repository management)
- **Deployment**: Heroku (for backend), AWS S3 (for static files)

## Project Structure
home-cleaning-platform/ │ ├── apps/ │ ├── products/ # Manages cleaning products (models, views, templates) │ ├── services/ # Manages cleaning services (models, views, templates) │ ├── carts/ # Manages user shopping carts │ ├── orders/ # Manages order processing and history │ ├── appointments/ # Manages service bookings and schedules │ └── users/ # Manages user authentication and profiles │ ├── templates/ # Contains HTML templates for the frontend ├── static/ # Holds static files (CSS, JavaScript, images) ├── manage.py # Django’s command-line utility └── README.md # Project documentation


## Installation and Setup
1. **Clone the repository**:
    ```bash
    git clone https://github.com/jandejager10/CodInstProj4.git
    cd home-cleaning-platform
    ```

2. **Create a virtual environment and activate it**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/macOS
    venv\Scripts\activate     # For Windows
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the environment variables**:
    - Create a `.env` file in the root directory and add your environment variables:
        ```
        SECRET_KEY=your_secret_key
        DEBUG=True
        DATABASE_URL=your_database_url
        STRIPE_API_KEY=your_stripe_api_key
        ```

5. **Apply database migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser for admin access**:
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

8. **Access the application**:
    - Visit `http://127.0.0.1:8000/` to view the platform.
    - Access the admin dashboard at `http://127.0.0.1:8000/admin/`.

## Deployment
1. **Heroku Deployment**:
    - Ensure that you have a Heroku account and the Heroku CLI installed.
    - Log in to Heroku and create a new application:
      ```bash
      heroku login
      heroku create home-cleaning-platform
      ```
    - Set up PostgreSQL as the database:
      ```bash
      heroku addons:create heroku-postgresql:hobby-dev
      ```
    - Deploy the application:
      ```bash
      git push heroku main
      ```
      
2. **AWS S3 Configuration for Static Files**:
    - Set up an S3 bucket for storing static files.
    - Configure your Django settings to use `django-storages` and connect to your S3 bucket using the appropriate environment variables.

## Testing
- The project includes unit tests and integration tests for critical components.
- Run the tests using:
    ```bash
    python manage.py test
    ```

## Additional Resources
- **Django Documentation**: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
- **Stripe Python Library**: [https://docs.stripe.com/get-started/development-environment?lang=python](https://docs.stripe.com/get-started/development-environment?lang=python)
- **Bootstrap**: [https://getbootstrap.com/](https://getbootstrap.com/)
- **Django REST Framework**: [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)

## Future Enhancements
- **Mobile App Integration**: Develop a mobile app using React Native or Flutter, integrated with Django REST API.
- **Loyalty Program**: Implement a points-based system for loyal customers.
- **Multi-Language Support**: Add support for multiple languages to reach a wider audience.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your improvements or bug fixes.

---

**Thank you for using Clean Services and Supplies Platform! We hope it brings convenience and quality cleaning to your life.**
