# 🛠 Django Backend for E-Commerce Platform

This repository contains the **backend** of a full-stack E-Commerce website built with **Django** and **Django REST Framework**. It provides secure authentication, email verification, product management, cart & order management, and payment processing via Stripe.

---

## 📌 Features

* ✅ **User Authentication**

  * User Registration and Login features
  * JWT token-based login/logout
  * Password reset functionality

* 🛍 **Product Management**

  * CRUD operations for products
  * Stock management
  * Categorization and search

* 🛒 **Cart & Orders based on user**

  * Add/remove products to cart
  * Manage cart items
  * Place and track orders

* 💳 **Checkout & Payments**

  * Stripe integration for secure payments
  * Order confirmation and status updates

* 📬 **Email Notifications**

  * Emails for registration, password reset, and order confirmations

---

## 🚀 Getting Started

### Prerequisites

* **Python** 3.9 or higher
* **Django** 4.x
* **pip** for dependencies

### Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/SakarDahal04/E-Commerce_Internship.git
cd E-Commerce_Internship
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory with your configuration:

```env
SECRET_KEY="your-secret-key"
DEBUG=True
DATABASE_URL="postgres://user:password@localhost:5432/dbname"
STRIPE_PUBLIC_KEY="your-stripe-public-key"
STRIPE_SECRET_KEY="your-stripe-secret-key"
```

5. **Run migrations**

```bash
python manage.py migrate
```

6. **Start the development server**

```bash
python manage.py runserver
```

Backend will run at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔗 Frontend Integration

The frontend connects to this backend at the base URL.
For frontend setup, refer to the repository:

* **Frontend Repo:** [React E-Commerce Frontend](https://github.com/SakarDahal04/E-Commerce_Internship_Frontend)

---

## 🤝 Contributing

This project is actively being developed. Contributions, issues, and feature requests are welcome!

---

## 📫 Contact

Connect with me on [LinkedIn](https://www.linkedin.com/in/sakar-dahal-30a560277/) for questions or collaboration.

---

Made with ❤️ and 🐍 Django.
