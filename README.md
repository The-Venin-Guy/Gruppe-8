# Gruppe-8 Portfolio Tracker

A personal finance and portfolio tracking web application built with Python and Django. Users can log and monitor their assets, stocks, and cash accounts in one place, with live market data and an AI-powered news feed.


## Project Structure

```
Gruppe-8/
├── core/                   # Project-level settings and master URL routing
├── users/                  # Authentication — login, signup, logout
├── portfolio/              # Assets, stocks, cash — models, views, forms
├── dashboard/              # Portfolio summary and net worth overview
├── templates/              # All HTML templates
│   ├── users/
│   ├── portfolio/
│   └── dashboard/
├── manage.py
├── db.sqlite3
├── .env                    # Secret keys — never commit this
└── requirements.txt
```

---

## Features Built So Far

### Authentication
- User signup and login
- Session-based login persistence
- Logout with session destruction
- Brute force protection via django-axes — account locks after 5 failed attempts for 1 hour
- Passwords validated against Django's built-in validators

### Asset Management
- Add physical assets — real estate, vehicles, land, other
- Edit asset details and current value
- Multi-currency support — USD, NGN, EUR, GBP
- Appreciation and appreciation percentage calculated automatically
- Mark asset as sold — records sale price and sale date
- Sold assets move to a collapsible history section

### Stock Tracking
- Add stocks by ticker symbol with autocomplete search
- Company name auto-filled when ticker is selected
- Live stock prices fetched from Yahoo Finance via yfinance
- Gain/loss and percentage return calculated in real time
- Edit stock details
- Sell stocks — optionally convert proceeds directly to a cash account
- Sold stocks move to a collapsible history section with profit/loss display

### Cash Accounts
- Add and edit bank account balances
- Multiple currencies supported per account
- Last updated timestamp tracked automatically

### Dashboard
- Total asset value pulled from database
- Total stock value calculated from live market prices
- Total cash balance
- Overall net worth = assets + stocks + cash
- All values update in real time on every page load

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.14 | Primary language |
| Django 6.x | Web framework |
| SQLite | Database |
| yfinance | Live stock prices from Yahoo Finance |
| django-axes | Brute force login protection |
| python-dotenv | Environment variable management |
| Bootstrap 5 | Frontend styling |

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd Gruppe-8
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create your `.env` file
Create a file called `.env` in the root of the project with the following:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create a superuser
```bash
python manage.py createsuperuser
```

### 7. Run the server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/users/login/` to get started.

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key — keep this private |
| `DEBUG` | Set to `True` in development, `False` in production |

---

## Pages and URLs

| URL | Page |
|-----|------|
| `/users/login/` | Login page |
| `/users/signup/` | Signup page |
| `/users/logout/` | Logout |
| `/dashboard/` | Portfolio dashboard and net worth |
| `/portfolio/assets/` | Asset list |
| `/portfolio/assets/add/` | Add new asset |
| `/portfolio/assets/edit/<id>/` | Edit asset |
| `/portfolio/assets/sell/<id>/` | Sell asset |
| `/portfolio/stocks/` | Stock list with live prices |
| `/portfolio/stocks/add/` | Add new stock |
| `/portfolio/stocks/edit/<id>/` | Edit stock |
| `/portfolio/stocks/sell/<id>/` | Sell stock |
| `/portfolio/cash/` | Cash accounts |
| `/portfolio/cash/add/` | Add cash account |
| `/portfolio/cash/edit/<id>/` | Edit cash account |
| `/admin/` | Django admin panel |

---

## What's Coming Next

- Currency conversion for accurate net worth across mixed currencies
- Interactive Plotly graphs for portfolio value over time
- Daily financial news feed via NewsAPI
- AI-powered investment recommendations via OpenAI API
- Deployment to Railway or Render

---

## Security Notes

- Never commit your `.env` file to version control
- Add `.env` to your `.gitignore` before pushing to GitHub
- Set `DEBUG=False` before deploying to production
- Change `ALLOWED_HOSTS` in `settings.py` to your actual domain before deployment

---

## Developer Notes

- The project uses Django's MVT pattern — Models, Views, Templates
- Each feature area is organised into its own Django app
- All portfolio data is user-scoped — users can only see and edit their own data
- Stock prices are fetched live on every page load — no caching yet
- Currency conversion for mixed-currency net worth is planned for the next sprint




