# 🎓 EduBot — AI College Enquiry Chatbot

A full-stack AI-powered chatbot web application that helps students get instant answers about college admissions, fees, courses, placements, scholarships, hostel, transport, and more.

---

## 🚀 Features

- **AI Chatbot** — NLP-based intent detection + TF-IDF FAQ matching
- **Voice Input/Output** — Web Speech API for hands-free interaction
- **User Auth** — JWT-based registration, login, profile management
- **Admin Panel** — Dashboard, FAQ CRUD, user management, chat logs, analytics
- **Dark/Light Mode** — Persistent theme toggle
- **Responsive UI** — Bootstrap 5, mobile-friendly
- **Notifications** — College announcements system
- **Chat History** — Per-user conversation history

---

## 🛠️ Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Frontend   | HTML5, CSS3, Bootstrap 5, JavaScript |
| Backend    | Python 3.10+, Flask 3.x             |
| AI/NLP     | NLTK, scikit-learn (TF-IDF)         |
| Database   | MySQL (via SQLAlchemy + PyMySQL)     |
| Auth       | JWT (Flask-JWT-Extended)            |
| Email      | Flask-Mail (SMTP)                   |
| Voice      | Web Speech API, SpeechRecognition   |

---

## 📁 Project Structure

```
college-chatbot/
├── app.py              # Flask application factory & routes
├── chatbot.py          # AI chatbot engine (NLP + TF-IDF)
├── config.py           # Configuration classes
├── database.py         # DB init, extensions, seed data
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
│
├── models/             # SQLAlchemy models
│   ├── user.py
│   ├── chat.py
│   ├── faq.py
│   ├── admin.py
│   └── notification.py
│
├── routes/             # Flask blueprints
│   ├── auth.py         # /api/auth/*
│   ├── chat.py         # /api/chat/*
│   ├── faq.py          # /api/faqs/*
│   └── admin.py        # /api/admin/*
│
├── services/
│   └── email_service.py
│
├── utils/
│   └── helpers.py
│
├── static/
│   ├── css/style.css
│   └── js/
│       ├── app.js      # Global JS (theme, auth, toasts)
│       ├── chatbot.js  # Chatbot UI logic
│       └── admin.js    # Admin panel logic
│
└── templates/
    ├── base.html
    ├── index.html
    ├── chatbot.html
    ├── login.html
    ├── register.html
    ├── admin.html
    ├── faq.html
    ├── profile.html
    ├── history.html
    ├── about.html
    ├── courses.html
    └── contact.html
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- MySQL 8.0+
- pip

### 1. Clone & Install

```bash
cd college-chatbot
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your MySQL credentials and secret keys
```

### 3. Create MySQL Database

```sql
CREATE DATABASE college_chatbot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Run the Application

```bash
python app.py
```

The app will:
- Auto-create all database tables
- Seed default FAQs and admin account
- Train the chatbot on startup
- Start on http://localhost:5000

---

## 🔑 Default Credentials

| Role  | Email                | Password   |
|-------|----------------------|------------|
| Admin | admin@college.edu    | Admin@123  |

---

## 📡 API Endpoints

| Method | Endpoint                    | Description              |
|--------|-----------------------------|--------------------------|
| POST   | /api/auth/register          | Register new user        |
| POST   | /api/auth/login             | Login (user or admin)    |
| GET    | /api/auth/profile           | Get user profile         |
| PUT    | /api/auth/profile           | Update profile           |
| POST   | /api/chat/message           | Send chat message        |
| GET    | /api/chat/history           | Get chat history         |
| GET    | /api/chat/suggestions       | Autocomplete suggestions |
| GET    | /api/faqs/                  | Get FAQs (public)        |
| POST   | /api/faqs/                  | Add FAQ (admin)          |
| PUT    | /api/faqs/:id               | Update FAQ (admin)       |
| DELETE | /api/faqs/:id               | Delete FAQ (admin)       |
| GET    | /api/admin/dashboard        | Dashboard stats (admin)  |
| GET    | /api/admin/users            | List users (admin)       |
| GET    | /api/admin/chats            | Chat logs (admin)        |
| POST   | /api/admin/notifications    | Add notification (admin) |

---

## 🌐 Pages

| URL        | Description              |
|------------|--------------------------|
| /          | Home page                |
| /chatbot   | AI Chatbot interface     |
| /login     | Login page               |
| /register  | Registration page        |
| /profile   | User profile             |
| /history   | Chat history             |
| /faq       | FAQ browser              |
| /about     | About college            |
| /courses   | Courses offered          |
| /contact   | Contact page             |
| /admin     | Admin dashboard          |

---

## 🚀 Production Deployment

```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# With environment variables
FLASK_ENV=production gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📝 License

MIT License — Free to use and modify.
