# django-online-cafe
An online operating platform for menu, orders and customers in a cafe managed by cafe manager/admin.
☕ Online Café Management System (Django)

A Django-based café management system with modular apps:

👤 users → User management, comments, replies, working shifts

💳 payment → Orders & payments

🍽 servehub → Tables, categories, products, discounts

🚀 0 → 100 Setup Guide
📌 1. Prerequisites

Make sure you have:

Python 3.10+

pip

Git

Virtualenv (optional but recommended)

PostgreSQL (or SQLite for development)

Check versions:

python --version
pip --version
git --version

📂 2. Clone the Repository
git clone https://github.com/your-username/online-cafe.git
cd online-cafe

🐍 3. Create Virtual Environment
On Mac/Linux:
python -m venv venv
source venv/bin/activate

On Windows:
python -m venv venv
venv\Scripts\activate


You should now see:

(venv)

📦 4. Install Dependencies
pip install -r requirements.txt


If requirements.txt doesn’t exist yet:

pip install django psycopg2-binary
pip freeze > requirements.txt

⚙️ 5. Project Structure
online-cafe/
│
├── users/              # Users, Comments, Replies, Working Shifts
├── payment/            # Orders & Payments
├── servehub/           # Tables, Categories, Products, Discounts
├── cafe_project/       # Main project settings
├── manage.py
└── requirements.txt

🔐 6. Environment Variables

Create a .env file in the root directory:

SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=cafe_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432


Install dotenv:

pip install python-dotenv


Update settings.py:

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"

🗄 7. Database Setup
Option A: SQLite (Simple Development)

In settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


Then:

python manage.py migrate

Option B: PostgreSQL (Recommended)

Create database:

CREATE DATABASE cafe_db;


Update settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}


Then migrate:

python manage.py migrate

👤 8. Create Superuser
python manage.py createsuperuser


Follow prompts.

🧠 9. Apps Overview
👤 Users App

Custom User model

WorkingShift

Comment

Reply

💳 Payment App

Order

Payment

🍽 ServeHub App

Table

Category

Product

Discount

Make sure they are registered in INSTALLED_APPS:

INSTALLED_APPS = [
    ...
    'users',
    'payment',
    'servehub',
]

🧱 10. Run Migrations for Apps

If new models are added:

python manage.py makemigrations
python manage.py migrate

▶️ 11. Run the Server
python manage.py runserver


Open:

http://127.0.0.1:8000/


Admin panel:

http://127.0.0.1:8000/admin/

🏗 Development Workflow
🌿 Create New Feature Branch
git checkout -b feature/add-discount-logic

💾 Commit Changes
git add .
git commit -m "Add discount calculation logic"

🚀 Push to GitHub
git push origin feature/add-discount-logic

🧪 Running Tests

If tests exist:

python manage.py test

📁 Static & Media Files

Collect static files (for production):

python manage.py collectstatic


Add in settings.py:

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"

🛠 Production Deployment (Basic Outline)

Set DEBUG=False

Set proper ALLOWED_HOSTS

Use PostgreSQL

Use Gunicorn

Use Nginx

Set environment variables securely

Run:

gunicorn cafe_project.wsgi:application

📌 Database Schema Overview
App	Models
users	User, WorkingShift, Comment, Reply
payment	Order, Payment
servehub	Table, Category, Product, Discount
🤝 Contributing

Fork the repo

Create feature branch

Commit changes

Push branch

Open Pull Request

📜 License

MIT License

👨‍💻 Author
Parsa
Ebrahim
Maryam
Alireza



