# PocketSmart.AI 💰

An AI-powered budget planning web application built with **FastAPI** and **Google Gemini AI**. PocketSmart AI helps users plan budgets across three major life categories — Home Interior, Party Events, and Jewelry — with smart product recommendations and direct shopping links.

---

## ✨ Features

- 🏠 **Home Interior Planner** — Get AI-curated furniture, lighting, and decor recommendations within your budget from Amazon, Flipkart, and IKEA
- 🎉 **Party Budget Planner** — Plan events with smart cost splits across catering, decoration, entertainment, venue, photography, and gifts
- 💍 **Jewelry Planner** — Get occasion-based jewelry recommendations; upload an outfit photo for AI color-matched suggestions
- 📜 **Recommendation History** — View, filter, and manage all past AI-generated plans
- 🔐 **User Authentication** — Secure login and registration with JWT tokens
- 📊 **Dashboard** — Central hub to access all planners

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| AI | Google Gemini 2.5 Flash |
| Frontend | Jinja2 Templates, HTML/CSS/JS |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Image Processing | Pillow |
| State | In-memory (Python list) |

---

## 📁 Project Structure

```
pocketsmart-ai/
│
├── app.py                  # Main FastAPI application
├── state.py                # Shared in-memory history store
├── .env                    # Environment variables (not committed)
├── requirements.txt        # Python dependencies
│
├── routers/                # API route handlers
│   ├── auth.py             # Login / Register
│   ├── home.py             # Home planner routes
│   ├── party.py            # Party planner routes
│   └── jewelry.py          # Jewelry planner routes
│
├── templates/              # Jinja2 HTML templates
│   ├── home.html           # Landing page
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── home_planner.html
│   ├── party_planner.html
│   ├── jewelry_planner.html
│   └── history.html
│
└── static/                 # Static assets (CSS, JS, images)
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/pocketsmart-ai.git
cd pocketsmart-ai
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_jwt_secret_key_here
```

> Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/)

### 5. Run the application

```bash
uvicorn app:app --reload
```

Visit `http://localhost:8000` in your browser.

---

## 🛒 Supported Shopping Platforms

| Category | Platforms |
|----------|-----------|
| Home & Decor | Amazon, Flipkart, IKEA, Meesho |
| Food & Catering | Swiggy, Zomato, Sulekha, JustDial |
| Venue | Google Maps, OYO, Booking.com, Sulekha |
| Photography / Entertainment | Sulekha, JustDial |
| Gifts & Decoration | Amazon, Flipkart, Meesho |

---

## 📦 Requirements

```
fastapi
uvicorn
google-genai
python-jose[cryptography]
passlib[bcrypt]
python-dotenv
Pillow
jinja2
python-multipart
```

---

## 🔒 Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Your Google Gemini API key |
| `SECRET_KEY` | Secret key for JWT token signing |

> ⚠️ Never commit your `.env` file. It is listed in `.gitignore`.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">
  Built with ❤️ using FastAPI & Google Gemini AI
</div>
