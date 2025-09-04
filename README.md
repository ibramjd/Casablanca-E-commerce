# Casablanca


Casablanca is an online clothing store, developed using the Django framework

***
## Features Included

- 🛍️ Product Management: Organized product display with categories, details, and images.

- 🛒 Shopping Cart: Dynamic cart that updates automatically when items are added, or removed.

- 💳 Payment System: Integrated with Bank of Khartoum (Bankak), with manual confirmation.

- 👤 User Accounts: Login, registration, password reset, and profile management using Django authentication.

- 📦 Order & Payment Tracking: Clear order statuses linked with payments.

- 🛠️ Admin Panel: Manage customers, products, orders, payments, and deliveries efficiently.

- 🔒 Security: Built-in authentication for safe and reliable user experience.

***
## Installation

1.Install Python:
Download and install the latest stable version of Python for your system from python.org
. Make sure to check “Add Python to PATH” during installation.

2.Clone the Repository:
```bash
git clone https://github.com/ibramjd/Casablanca-E-commerce.git
cd Casablanca-E-commerce
```

3.Create Virtual Environment
```bash
python -m venv env

  *Activate the environment

  *On Windows:

env\Scripts\activate

  *On macOS/Linux:
source env/bin/activate
```

4.Install Required Packages
```bash
pip install -r requirements.txt
```

5.Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

6.Collect Static Files
```bash
python manage.py collectstatic
```

7.Run the Server
```bash
python manage.py runserver
```

***
## Usage Example

1.Register / Login

- Go to http://127.0.0.1:8000/
- Go to register page to create a new account or log in with your credentials in login page.

2.Browse Products
  
- Use filters, categories (Men, Women, Kids), type of clothe, price to find products easily.

3.Shopping Cart

- Add items to cart our delete them.
- See automatic updates to total price.

4.Checkout & Payment

- Proceed to checkout.
- Enter transacion ID from Bankak App and Amount.
- After manual confirmation, the payment status updates.

5.Admin Panel

- Login to django admin panel.
- Manage products, customers, orders, order items, payments, and shipping addresses.

***
## Contributor Credits 

- **Ibrahim Amjad** - Project Developer ( Frontend & Backend ).
- **Django Framework** - For authentication and admin panel features.
- **Copilot & ChatGPT** - Assisting in coding and project structure.
