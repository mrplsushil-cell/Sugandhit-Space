# Sugandhit Space - Gardening & Landscaping App

A full-stack web application for gardening and landscaping services with online plant catalog, expert booking, and real-time order tracking.

## 🚀 Features

### Customer Features
- ✅ User authentication (Register, Login)
- ✅ Browse and search plant catalog
- ✅ Shopping cart and checkout
- ✅ Service booking with calendar
- ✅ Real-time order tracking
- ✅ Payment gateway integration (Razorpay)
- ✅ Support tickets and FAQ
- ✅ Customer dashboard

### Admin Features
- ✅ Admin dashboard with analytics
- ✅ Order management
- ✅ Customer management
- ✅ Plant/Product inventory management
- ✅ Service management
- ✅ Support ticket management
- ✅ Revenue tracking

## 📋 Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Database**: SQLite (scalable to PostgreSQL)
- **Payment**: Razorpay
- **Authentication**: Flask-Login, JWT
- **ORM**: SQLAlchemy

## 🔧 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Local Setup

1. **Clone the repository**
```bash
cd sugandhit-app
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Set environment variables**

Create a `.env` file:
```
FLASK_APP=app.py
FLASK_ENV=development
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
JWT_SECRET_KEY=your-secret-key
```

6. **Run the application**
```bash
python app.py
```

The app will be available at `http://localhost:5000`

## 🐳 Docker Setup (Recommended for Production)

### Build Docker image
```bash
docker build -t sugandhit-app .
```

### Run Docker container
```bash
docker run -p 5000:5000 sugandhit-app
```

## 📱 Default Admin Credentials

To access the admin dashboard, you need to create an admin account. You can do this by:

1. Registering a new account
2. Manually updating the user role in the database to 'admin'

Or create an admin script and run it.

## 🗂️ Project Structure

```
sugandhit-app/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── models.py                 # Database models
├── requirements.txt          # Python dependencies
├── routes/
│   ├── auth.py              # Authentication routes
│   ├── main.py              # Main routes (home, about, etc.)
│   ├── catalog.py           # Plant catalog routes
│   ├── booking.py           # Service booking routes
│   ├── order.py             # Order management routes
│   ├── payment.py           # Payment routes
│   ├── support.py           # Support/ticket routes
│   ├── admin.py             # Admin panel routes
│   └── dashboard.py         # Customer dashboard routes
├── templates/
│   ├── base.html            # Base template
│   ├── home.html            # Home page
│   ├── auth/                # Auth templates
│   ├── catalog/             # Catalog templates
│   ├── booking/             # Booking templates
│   ├── order/               # Order templates
│   ├── payment/             # Payment templates
│   ├── support/             # Support templates
│   ├── dashboard/           # Dashboard templates
│   └── admin/               # Admin templates
├── static/
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript files
│   └── images/              # Images
└── README.md                # This file
```

## 🗄️ Database Models

### User
- Customer, Expert, Admin roles
- Authentication with password hashing
- Profile information

### Plant
- Product catalog
- Categories, pricing, quantity
- Care tips and descriptions

### Service
- Gardening services
- Bookable expert visits
- Monthly maintenance plans

### Booking
- Expert visit scheduling
- Status tracking
- Expert assignment

### Order
- Plant/product orders
- Cart management
- Payment status tracking

### Payment
- Razorpay integration
- Transaction history
- Payment verification

### DeliveryTracking
- Real-time order tracking
- Estimated delivery dates
- Delivery personnel info

### SupportTicket
- Customer support requests
- Ticket categorization
- Resolution tracking

## 🔐 Security Features

- Password hashing with Werkzeug
- CSRF protection
- SQL injection prevention with ORM
- JWT token-based authentication
- Session management
- HTTPS ready

## 💳 Payment Integration

### Razorpay Setup

1. Create account on [Razorpay](https://razorpay.com)
2. Get API keys from dashboard
3. Add to `.env`:
   ```
   RAZORPAY_KEY_ID=your_key_id
   RAZORPAY_KEY_SECRET=your_key_secret
   ```

## 📊 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/logout` - Logout user

### Products
- `GET /catalog/` - List plants
- `GET /catalog/<id>` - Plant details
- `POST /catalog/cart/add` - Add to cart
- `GET /catalog/cart` - View cart

### Booking
- `GET /booking/` - Browse services
- `POST /booking/book/<id>` - Book service
- `POST /booking/cancel/<id>` - Cancel booking

### Orders
- `GET /order/checkout` - Checkout page
- `POST /order/checkout` - Create order
- `GET /order/<id>` - Order details

### Admin
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/orders` - Manage orders
- `GET /admin/plants` - Manage plants

## 🧪 Testing

To test the application:

1. Create test data (plants, services)
2. Register test user accounts
3. Test booking flow
4. Test cart and checkout
5. Test admin functionalities

## 🚀 Deployment

### Heroku
```bash
heroku create sugandhit-app
git push heroku main
```

### AWS/DigitalOcean
- Use Gunicorn as WSGI server
- Set up Nginx as reverse proxy
- Configure PostgreSQL for production
- Set up SSL certificates

## 📞 Support

For support and queries:
- Email: info@sugandhit.com
- Phone: +91-9999-999-999

## 📄 License

This project is licensed under MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 Notes

- Update Razorpay keys for production
- Use PostgreSQL for production instead of SQLite
- Enable HTTPS
- Set up email notifications
- Configure backup strategy
- Monitor application performance

---

**Built with ❤️ for gardening enthusiasts**
