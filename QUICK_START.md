# 🚀 Quick Start Guide - Sugandhit Space

Get the Sugandhit Space gardening app up and running in minutes!

## 📋 Prerequisites

- **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
- **Git** (optional) - For cloning repository
- **Razorpay Account** (optional) - For payment testing

## ⚡ Quick Start (5 minutes)

### 1. **Setup Python Environment**

```bash
# Navigate to project directory
cd sugandhit-app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 3. **Configure Environment**

Create `.env` file from example:
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your settings (optional for local development)
# At minimum, keep the default values for testing
```

### 4. **Initialize Database**

```bash
python init_db.py
```

This will:
- Create database tables
- Add sample services and plants
- Create admin account

**Default Admin Credentials:**
- Email: `admin@sugandhit.com`
- Password: `admin@123`

### 5. **Run Application**

```bash
python app.py
```

Application will start at: **http://localhost:5000**

## 🎯 First Steps After Setup

### 1. **Access Admin Panel**
- Go to http://localhost:5000/auth/login
- Login with admin credentials
- Access admin dashboard at `/admin/dashboard`

### 2. **Create Customer Account**
- Go to http://localhost:5000/auth/register
- Register as customer
- Browse plants and services

### 3. **Test Features**
- ✅ Browse plants catalog
- ✅ Add items to cart
- ✅ Book expert services
- ✅ Checkout (use test payment details)
- ✅ View admin dashboard

## 💳 Payment Testing (Razorpay)

For local testing without real payments:

1. Use test credentials from `.env.example`
2. Use Razorpay test keys: https://dashboard.razorpay.com/
3. Test card: `4111111111111111` (any future date, any CVV)

## 🗂️ Project File Structure

```
sugandhit-app/
├── app.py              # Main application
├── models.py           # Database models
├── config.py           # Configuration
├── init_db.py          # Database setup script
├── requirements.txt    # Python packages
├── .env.example        # Environment variables template
├── Dockerfile          # Docker setup
├── docker-compose.yml  # Docker Compose
├── README.md           # Full documentation
├── routes/             # API routes
│   ├── auth.py
│   ├── catalog.py
│   ├── booking.py
│   ├── order.py
│   ├── payment.py
│   ├── admin.py
│   └── ...
└── templates/          # HTML templates
    ├── base.html
    ├── home.html
    ├── auth/
    ├── catalog/
    ├── booking/
    └── ...
```

## 🔧 Common Issues & Solutions

### Issue: "Python not found"
**Solution:** Install Python from https://www.python.org/downloads/

### Issue: "Module not found" error
**Solution:** Make sure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
**Solution:** Either close the application using that port or change Flask port:
```bash
python app.py --port 5001
```

### Issue: Database locked
**Solution:** Delete `sugandhit.db` and reinitialize:
```bash
rm sugandhit.db
python init_db.py
```

## 📱 Access Points

| Page | URL | Access |
|------|-----|--------|
| Home | http://localhost:5000 | Everyone |
| Login | http://localhost:5000/auth/login | Everyone |
| Register | http://localhost:5000/auth/register | Everyone |
| Catalog | http://localhost:5000/catalog | Everyone |
| Dashboard | http://localhost:5000/dashboard | Logged in |
| Admin | http://localhost:5000/admin/dashboard | Admin only |

## 🎨 Customize the App

### Change App Name
Edit `base.html` - Update "Sugandhit Space" text

### Change Colors
Edit `templates/base.html` - Modify CSS variables in `<style>` tag:
```css
--primary-color: #2ecc71;
--secondary-color: #27ae60;
```

### Add More Plants
- Use admin panel: `/admin/plants`
- Or edit `init_db.py` and reinitialize

### Modify Services
- Use admin panel: `/admin/services`
- Or edit `init_db.py` and reinitialize

## 🚀 Next Steps

1. **Customize** - Add your branding and content
2. **Add Data** - Add more plants and services via admin panel
3. **Deploy** - Use Docker or deploy to cloud (Heroku, AWS, DigitalOcean)
4. **Scale** - Switch to PostgreSQL for production
5. **Integrate** - Add email notifications, SMS, etc.

## 📞 Support

- 📧 Email: info@sugandhit.com
- 📱 Phone: +91-9999-999-999

## 🤝 Contributing

Found a bug or have a feature request? Create an issue or submit a pull request!

## 📄 License

MIT License - Feel free to use and modify

---

**Happy Gardening! 🌱**

For more details, see [README.md](README.md)
