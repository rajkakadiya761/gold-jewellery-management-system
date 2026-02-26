💎 Gold Jewellery Management System with Augmented Reality

A modern full-stack web application that allows users to browse, manage, purchase, and virtually try jewellery products using real-time Augmented Reality.

This platform provides a realistic online jewellery shopping experience where customers can preview rings and other jewellery items before purchasing.

🚀 Features

🔐 User Registration & Secure Login

🛒 Add to Cart & Order Management

💳 Razorpay Payment Integration

📦 Admin Product Management

📧 Email Verification System

⏰ Background Scheduler (Automated Tasks)

🎥 AR-Based Virtual Try-On (Ring / Jewellery)

📱 Fully Responsive UI

🛠️ Tech Stack
🔹 Backend

Flask

SQLAlchemy

APScheduler

🔹 Database

MySQL

XAMPP

🔹 AR & Computer Vision

OpenCV

MediaPipe

NumPy

🔹 Payment Gateway

Razorpay

🖥 Requirements

Python 3.10.0 or above (Recommended: 3.10 / 3.11)

MySQL Server (XAMPP recommended for local setup)

Webcam (for AR functionality)

Internet connection (for payment gateway)

⚙️ Installation Guide
1️⃣ Clone Repository
git clone https://github.com/rajkakadiya761/gold-jewellery-management-system.git
cd gold-jewellery-management-system
2️⃣ Create Virtual Environment
python -m venv venv

Activate:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run Application
python app.py

Open browser:

http://127.0.0.1:5000
📦 Production Requirements (requirements.txt)
Flask>=2.2.0
Flask-SQLAlchemy>=3.0.0
Flask-Mail>=0.9.1
SQLAlchemy>=2.0.0
itsdangerous>=2.1.0
APScheduler>=3.10.0
opencv-python-headless>=4.8.0
mediapipe>=0.10.0
numpy>=1.23.0
requests>=2.28.0
razorpay>=1.3.0
gunicorn>=21.2.0

✔ Removed Windows-only dependency (pywin32)
✔ Replaced opencv-python with opencv-python-headless
✔ Added gunicorn for production deployment

🚀 Deployment Guide
🔹 Render Deployment

Push project to GitHub

Go to https://render.com

Create New → Web Service

Connect your GitHub repository

Build Command

pip install -r requirements.txt

Start Command

gunicorn app:app

Add Environment Variables:

SECRET_KEY

MAIL_USERNAME

MAIL_PASSWORD

RAZORPAY_KEY_ID

RAZORPAY_SECRET

Use a cloud MySQL/PostgreSQL database.

🔹 Railway Deployment

Go to https://railway.app

Deploy from GitHub

Add MySQL plugin

Add environment variables

Start Command:

gunicorn app:app
⚠️ MediaPipe Troubleshooting
❌ Failed building wheel for mediapipe
pip install --upgrade pip setuptools wheel
pip install mediapipe
❌ Python Version Error

Use:

Python 3.10

Python 3.11

Avoid:

Python 3.12+

❌ Webcam Not Opening

Allow camera permissions

Close other apps using camera

Ensure correct:

cv2.VideoCapture(0)
📂 Project Modules

Authentication Module

Product Management

Shopping Cart

AR Try-On System

Payment System

Email Verification
