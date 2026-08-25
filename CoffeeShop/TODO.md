# TODO: Implement Admin Functionality

## Models
- [x] Add Order model to models.py (user, items JSONField, total, status, created_at)
- [x] Add Contact model to models.py (name, email, message, created_at)
- [x] Register Order and Contact in admin.py

## Views
- [x] Modify checkout view to save orders to database
- [x] Modify contact view to save contact submissions to database
- [x] Add admin_dashboard view
- [x] Add manage_coffee view (increase/decrease quantity and price)
- [x] Add confirm_order view
- [x] Add view_orders view
- [x] Add view_contacts view
- [x] Restrict add_to_cart and payment views for staff users (admins)

## URLs
- [x] Add admin URL patterns to coffee/urls.py

## Templates
- [x] Create admin_dashboard.html
- [x] Create manage_coffee.html
- [x] Create view_orders.html
- [x] Create view_contacts.html

## Database
- [x] Run migrations for new models

## Testing
- [ ] Test admin login
- [ ] Test coffee management (quantity/price)
- [ ] Test order confirmation
- [ ] Test viewing orders and contacts
- [ ] Ensure admins cannot add to cart or make payments
