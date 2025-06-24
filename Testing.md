# Manual Testing

This document outlines the manual testing performed on the Eevee Emporium website to ensure all features are working as intended and the user experience is seamless, responsive, and bug-free.

---

## Testing Strategy

Testing was conducted across multiple modern web browsers (Google Chrome, Mozilla Firefox, Microsoft Edge) and on various device sizes (desktop, tablet, and mobile) to ensure cross-browser compatibility and a fully responsive design. The tests cover all key user stories and functionalities, from a guest visitor's perspective to a registered user and a site administrator.

---

## Test Cases

### 1. General Site & Navigation

| Test ID | Feature             | Test Description                                                              | Expected Result                                                              | Status |
|---------|---------------------|-------------------------------------------------------------------------------|------------------------------------------------------------------------------|--------|
| GEN-01  | Homepage            | Open the website's root URL.                                                  | The homepage loads correctly with all elements, including the navbar, footer, and featured products. | Pass   |
| GEN-02  | Navigation Links    | Click on every link in the main navigation bar (e.g., Cards, Accessories, All Products). | Each link directs the user to the correct page without errors.               | Pass   |
| GEN-03  | Footer Links        | Click on all links in the site footer.                                        | Each link directs the user to the correct page or external site.             | Pass   |
| GEN-04  | Image Loading       | Browse through various pages (home, product lists, product details).          | All images (logo, product images, banners) load correctly and are not broken. | Pass   |
| GEN-05  | Responsiveness      | Resize the browser window to simulate desktop, tablet, and mobile views.      | The layout adjusts gracefully to each screen size. Navigation collapses into a hamburger menu on smaller screens. | Pass   |
| GEN-06  | 404 Error Page      | Navigate to a non-existent URL.                                               | A user-friendly 404 "Page Not Found" error page is displayed.                | Pass   |

### 2. Guest & Shopping Functionality

| Test ID | Feature             | Test Description                                                              | Expected Result                                                              | Status |
|---------|---------------------|-------------------------------------------------------------------------------|------------------------------------------------------------------------------|--------|
| GUEST-01| Product Browsing    | Navigate to a product category page.                                          | All products within that category are displayed in a grid.                   | Pass   |
| GUEST-02| Product Details     | Click on a product from the list page.                                        | The user is taken to the product detail page, showing the product image, description, price, and "Add to Bag" button. | Pass   |
| GUEST-03| Search              | Use the search bar to search for an existing product by name or description.  | The search results page displays all relevant products.                      | Pass   |
| GUEST-04| Search (No Results) | Use the search bar to search for a non-existent product.                      | A message indicating "No results found" is displayed.                        | Pass   |
| GUEST-05| Add to Bag          | On a product detail page, select a quantity and click "Add to Bag".           | The item is added to the shopping bag, and a success message (toast) appears. The bag total in the navbar updates. | Pass   |
| GUEST-06| View Bag            | Click on the shopping bag icon.                                               | The shopping bag page is displayed, showing all items, quantities, subtotal, and total. | Pass   |
| GUEST-07| Update Quantity     | In the shopping bag, update the quantity of an item.                          | The item's subtotal and the grand total update automatically. A confirmation message is shown. | Pass   |
| GUEST-08| Remove from Bag     | In the shopping bag, click the remove icon for an item.                       | The item is removed from the bag, and the grand total is updated.            | Pass   |

### 3. User Authentication

| Test ID | Feature             | Test Description                                                              | Expected Result                                                              | Status |
|---------|---------------------|-------------------------------------------------------------------------------|------------------------------------------------------------------------------|--------|
| AUTH-01 | Registration (Success) | Navigate to the register page and sign up with a unique email and matching passwords. | The user is successfully registered, logged in, and redirected to their profile or the homepage. A success message is shown. | Pass   |
| AUTH-02 | Registration (Fail) | Attempt to register with an email that already exists or with mismatched passwords. | An appropriate error message is displayed to the user, and registration is prevented. | Pass   |
| AUTH-03 | Login (Success)     | Navigate to the login page and enter correct credentials.                     | The user is successfully logged in and redirected. The navbar updates to show "Profile" and "Logout" links. | Pass   |
| AUTH-04 | Login (Fail)        | Attempt to log in with an incorrect password or non-existent email.           | An error message is displayed, and the user remains on the login page.       | Pass   |
| AUTH-05 | Logout              | While logged in, click the "Logout" link.                                     | The user is logged out and redirected to the homepage. The navbar reverts to the guest view. | Pass   |

### 4. Registered User Functionality

| Test ID | Feature             | Test Description                                                              | Expected Result                                                              | Status |
|---------|---------------------|-------------------------------------------------------------------------------|------------------------------------------------------------------------------|--------|
| USER-01 | Profile Access      | While logged in, navigate to the user profile page.                           | The profile page displays the user's default delivery information and order history. | Pass   |
| USER-02 | Update Profile      | Update the default delivery information on the profile page and save.         | The information is successfully updated, and a confirmation message is shown. The updated info is pre-filled at checkout. | Pass   |
| USER-03 | View Order History  | On the profile page, view the list of past orders. Click on a past order.     | A list of past orders is visible. Clicking an order shows a detailed confirmation of that specific order. | Pass   |
| USER-04 | Checkout Process    | With items in the bag, proceed to the secure checkout.                        | The checkout page loads, pre-filling user info if available. The order summary and payment form are displayed. | Pass   |
| USER-05 | Form Validation     | Attempt to submit the checkout form with invalid or missing information.      | The form submission is blocked, and error messages are displayed next to the invalid fields. | Pass   |
| USER-06 | Payment (Stripe)    | Fill in the checkout form and valid Stripe test card details, then submit payment. | The payment is processed successfully. The user is redirected to an order confirmation page. | Pass   |

### 5. Site Administrator (Superuser) Functionality

| Test ID | Feature             | Test Description                                                              | Expected Result                                                              | Status |
|---------|---------------------|-------------------------------------------------------------------------------|------------------------------------------------------------------------------|--------|
| ADMIN-01| Access Controls     | Attempt to access an admin-only URL (e.g., product management) as a guest or regular user. | Access is denied, and the user is redirected (e.g., to the login page or homepage). | Pass   |
| ADMIN-02| Add Product         | As an admin, navigate to the "Add Product" page and fill out the form with valid data. | The new product is created and appears on the storefront and in the product management list. | Pass   |
| ADMIN-03| Edit Product        | As an admin, select a product to edit and update its details (e.g., price, description). | The product's details are successfully updated on the storefront.            | Pass   |
| ADMIN-04| Delete Product      | As an admin, delete a product from the management interface.                  | The product is removed from the database and no longer appears on the storefront. | Pass   |
| ADMIN-05| Category Management | As an admin, add, edit, and delete product categories.                        | All CRUD operations for categories work as expected, and changes are reflected in the site's navigation and product filtering. | Pass   |
| ADMIN-06| Order Management    | As an admin, view the list of all customer orders.                            | A comprehensive list of all orders is displayed in the admin panel.