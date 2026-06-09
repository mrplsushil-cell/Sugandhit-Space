# 🧪 Testing Checklist - Sugandhit Space

Complete testing checklist to verify all features are working correctly.

## 📋 Pre-Testing Setup

- [ ] Python installed (3.8+)
- [ ] Dependencies installed via `pip install -r requirements.txt`
- [ ] Database initialized via `python init_db.py`
- [ ] Application started with `python app.py`
- [ ] Browser open at http://localhost:5000

---

## ✅ Authentication Tests

### Registration
- [ ] Can access registration page at `/auth/register`
- [ ] Can register with valid data
- [ ] Email validation works (rejects invalid emails)
- [ ] Phone validation works (requires 10 digits)
- [ ] Password validation works (min 6 characters)
- [ ] Password confirmation validation works
- [ ] Cannot register with existing email
- [ ] Redirects to login after successful registration

### Login
- [ ] Can access login page at `/auth/login`
- [ ] Can login with correct credentials
- [ ] Login fails with incorrect password
- [ ] Login fails with non-existent email
- [ ] "Remember me" checkbox works
- [ ] Can logout successfully

### Profile
- [ ] Can access profile from dropdown menu
- [ ] Can update profile information
- [ ] Can change password with correct old password
- [ ] Password change fails with wrong old password
- [ ] Cannot set password < 6 characters

---

## 🌱 Plant Catalog Tests

### Browsing
- [ ] Can access catalog at `/catalog/`
- [ ] Displays all active plants
- [ ] Pagination works (if > 12 plants)
- [ ] Search functionality works
- [ ] Category filter works
- [ ] Sort by name works
- [ ] Sort by price (low-high) works
- [ ] Sort by price (high-low) works

### Plant Details
- [ ] Can click on plant to view details
- [ ] Plant details page displays all information
- [ ] Care tips are visible
- [ ] Price is displayed correctly
- [ ] Stock availability is shown
- [ ] Related plants are suggested
- [ ] Can add to cart from detail page

### Reviews
- [ ] Can leave a review (if authenticated)
- [ ] Reviews display with rating
- [ ] Average rating calculates correctly
- [ ] Cannot review if not authenticated

---

## 🛒 Shopping Cart Tests

### Add to Cart
- [ ] Can add items from catalog
- [ ] Can add items from plant detail page
- [ ] Cart count updates in navbar
- [ ] Success message displays
- [ ] Cannot add out-of-stock items (button disabled)

### View Cart
- [ ] Can access cart from navbar
- [ ] All items display correctly
- [ ] Quantities show correctly
- [ ] Prices display correctly
- [ ] Item totals calculate correctly

### Cart Management
- [ ] Can update quantity
- [ ] Can remove items
- [ ] Can clear entire cart
- [ ] Subtotal calculates correctly
- [ ] Tax (5%) calculates correctly
- [ ] Delivery charge applies (if < 1000)
- [ ] Final total displays correctly

### Empty Cart
- [ ] Shows appropriate message for empty cart
- [ ] Provides link to continue shopping

---

## 💳 Checkout & Payment Tests

### Checkout Process
- [ ] Can access checkout from cart
- [ ] Cannot checkout if not authenticated
- [ ] Must fill all required fields
- [ ] Can enter delivery address
- [ ] Can select city and pincode
- [ ] Phone number field works
- [ ] Order summary displays correctly

### Order Creation
- [ ] Order created successfully after checkout
- [ ] Order number generated correctly (ORD-XXXXXXXX)
- [ ] Order status is "pending"
- [ ] Items saved correctly to order
- [ ] Cart cleared after checkout

### Payment Gateway
- [ ] Razorpay payment page loads
- [ ] Test payment can be processed
- [ ] Payment verification works
- [ ] Order status updates to "confirmed" after payment
- [ ] Payment status updates to "completed"

### Payment Failure
- [ ] Failed payments handled gracefully
- [ ] Error messages display correctly
- [ ] Can retry payment

---

## 📅 Service Booking Tests

### Booking System
- [ ] Can access booking page at `/booking/`
- [ ] Services list displays
- [ ] Can view service details
- [ ] Cannot book if not authenticated
- [ ] Can select booking date
- [ ] Can select booking time
- [ ] Can add notes (optional)
- [ ] Can confirm booking

### Booking Management
- [ ] My bookings display in dashboard
- [ ] Booking details show correctly
- [ ] Can cancel booking (24 hours before)
- [ ] Cannot cancel within 24 hours
- [ ] Can reschedule booking
- [ ] Booking status updates correctly

---

## 📦 Order Management Tests

### Order History
- [ ] Can view all orders in dashboard
- [ ] Orders list displays with order number, date, amount, status
- [ ] Can filter by status
- [ ] Pagination works

### Order Tracking
- [ ] Can access order details page
- [ ] Order information displays correctly
- [ ] Delivery tracking shows status
- [ ] Estimated delivery date shows
- [ ] Delivery person info shows (if assigned)

### Order Actions
- [ ] Can cancel order (if status allows)
- [ ] Cannot cancel delivered orders
- [ ] Can view invoice/receipt
- [ ] Can request return

---

## 👤 User Dashboard Tests

### Dashboard Overview
- [ ] Can access dashboard at `/dashboard/`
- [ ] Shows correct statistics
- [ ] Displays recent orders
- [ ] Displays upcoming bookings
- [ ] Quick links work

### Dashboard Pages
- [ ] My Orders page shows all orders
- [ ] My Bookings page shows all bookings
- [ ] Profile page displays user info
- [ ] Can update profile information
- [ ] Password change page works

---

## 💬 Support System Tests

### Support Center
- [ ] Can access support at `/support/`
- [ ] FAQ section displays all FAQs
- [ ] FAQ accordion expands/collapses
- [ ] Can access contact form
- [ ] Can create support ticket (if authenticated)

### Support Tickets
- [ ] Can create ticket with subject, message, category, priority
- [ ] Ticket created successfully
- [ ] Can view ticket details
- [ ] Can view all tickets
- [ ] Can filter by status

### Chat
- [ ] Chat interface loads
- [ ] Can send message
- [ ] Bot response works (mock)
- [ ] Chat history displays

---

## 🔐 Admin Tests

### Admin Authentication
- [ ] Admin can login with admin credentials
- [ ] Regular users cannot access admin panel
- [ ] Admin dashboard accessible at `/admin/dashboard`

### Admin Dashboard
- [ ] Dashboard loads successfully
- [ ] Statistics display correctly (orders, revenue, etc.)
- [ ] Recent orders list shows
- [ ] Charts render (if implemented)

### Admin Features
- [ ] Can view and manage orders
- [ ] Can view and manage customers
- [ ] Can view and manage plants
- [ ] Can create new plant
- [ ] Can edit plant
- [ ] Can delete plant
- [ ] Can view bookings
- [ ] Can view support tickets
- [ ] Can respond to tickets
- [ ] Can view analytics

---

## 🎨 UI/UX Tests

### Responsiveness
- [ ] Layout works on mobile (375px)
- [ ] Layout works on tablet (768px)
- [ ] Layout works on desktop (1024px+)
- [ ] Navigation responsive on mobile
- [ ] All buttons/forms accessible
- [ ] Images responsive

### Visual
- [ ] Navigation bar visible and styled
- [ ] Footer displays correctly
- [ ] Colors consistent throughout
- [ ] Fonts readable
- [ ] Icons display correctly
- [ ] No broken images
- [ ] Flash messages styled correctly

### Navigation
- [ ] Home link works from all pages
- [ ] Navigation menu accessible
- [ ] User dropdown works (if authenticated)
- [ ] Logout link works
- [ ] Links go to correct pages
- [ ] Breadcrumbs work (if implemented)

---

## 🐛 Error Handling Tests

### Page Errors
- [ ] 404 error page displays for non-existent routes
- [ ] 500 error page displays for server errors
- [ ] Error messages are user-friendly

### Form Validation
- [ ] Empty fields show error messages
- [ ] Invalid formats show error messages
- [ ] Success messages display on completion
- [ ] Errors prevent form submission

### Database Errors
- [ ] Handles database connection errors gracefully
- [ ] Shows appropriate error messages
- [ ] Application doesn't crash

---

## ⚡ Performance Tests

### Page Load
- [ ] Home page loads < 3 seconds
- [ ] Catalog page loads < 3 seconds
- [ ] Admin dashboard loads < 5 seconds
- [ ] No console errors in developer tools

### Functionality
- [ ] Search responds quickly
- [ ] Cart operations are instant
- [ ] Payment processing doesn't timeout
- [ ] No memory leaks in console

---

## 🔐 Security Tests

### Authentication
- [ ] Cannot access admin without authentication
- [ ] Cannot access dashboard without login
- [ ] Session expires after timeout
- [ ] Passwords hashed in database

### Data Protection
- [ ] Passwords are hidden in forms
- [ ] Sensitive data not exposed in URLs
- [ ] CSRF protection works
- [ ] SQL injection not possible

### Input Validation
- [ ] HTML special characters handled
- [ ] File uploads validated (if applicable)
- [ ] Email addresses validated
- [ ] Phone numbers validated

---

## 📊 Browser Compatibility

- [ ] Works in Chrome
- [ ] Works in Firefox
- [ ] Works in Safari
- [ ] Works in Edge
- [ ] Mobile Safari works
- [ ] Chrome Mobile works

---

## 🎁 Bonus Tests

### Additional Features
- [ ] Testimonials page works
- [ ] About page displays
- [ ] Contact form submits
- [ ] FAQ search works (if implemented)
- [ ] User preferences saved
- [ ] Dark mode toggle (if implemented)

---

## ✅ Final Verification

- [ ] No console errors in browser
- [ ] No Python errors in terminal
- [ ] Database operations complete
- [ ] All links functional
- [ ] All pages accessible
- [ ] Data persists after refresh
- [ ] Can complete full user journey (register → browse → purchase → track)

---

## 🎯 Sign-off Checklist

- [ ] All critical tests passed
- [ ] All important tests passed
- [ ] No critical bugs found
- [ ] All features working as expected
- [ ] Application ready for use
- [ ] Documentation complete

---

## 📝 Notes

Use this space to note any issues found during testing:

```
1. 
2. 
3. 
```

---

## 🚀 Ready for Deployment?

- [ ] All tests passed
- [ ] Database backed up
- [ ] Configuration updated for production
- [ ] Environment variables set
- [ ] SSL certificate ready (if needed)
- [ ] Deployment script ready

---

**Tested By**: ___________________
**Date**: ___________________
**Status**: ✅ PASSED / ❌ FAILED

For any issues found, please report in the Notes section above.
