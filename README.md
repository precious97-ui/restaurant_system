Foody Restaurant System 🍔

Description:
Foody is a restaurant management web application built with Django, Python, HTML, and CSS. It allows users to browse menu items, add items to a cart, place orders, and view order history. The About page displays the restaurant team with photos and roles. Images are stored using Cloudinary for reliable access.

Features:
	•	User signup/login (username, email, or phone)
	•	Dashboard with menu items, search, and category filter
	•	Add to Cart, Remove from Cart, Checkout
	•	Order history tracking
	•	About page showing team members

Tech Stack:
	•	Backend: Python, Django 6.0
	•	Frontend: HTML, CSS
	•	Database: SQLite (development)
	•	Image Storage: Cloudinary

Installation:
	1.	Clone the repo: git clone <repo-url>
	2.	Install dependencies: pip install -r requirements.txt
	3.	Set environment variables for secret keys and Cloudinary
	4.	Run migrations: python manage.py migrate
	5.	Start server: python manage.py runserver
