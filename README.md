# Eevee Emporium

install virtual environment:
```python -m venv virt```

Run Virtual Environment:
```./virt/Scripts/activate```

Install requirements:
```pip install -r requirements.txt```

Create superuser:
```python manage.py createsuperuser```

Follow prompts to add username, email and password.

Launch development server:
```python manage.py reunserver```


Template:
https://themewagon.com/themes/kaira/

Favicon:
https://commons.wikimedia.org/wiki/File:Pok%C3%A9_Ball_icon.svg

Favicon Generator
https://realfavicongenerator.net/

Wallpaper:
https://wall.alphacoders.com/big.php?i=613932

image optimiser:
https://squoosh.app

## Using Default Account Functionality over AllAuth

I opted not to use AllAuth in this project as Django comes with a robust and secure built-in authentication system (django.contrib.auth) that provides the fundamental building blocks for user management. For a project that requires standard user registration, login, logout, password reset, and profile updates, Django's default capabilities are often more than enough.

1 - Core User Model: Django provides a User model out of the box, which includes essential fields like username, password (hashed for security), email, first name, last name, is_active, is_staff, and is_superuser. This covers the basic identity and administrative roles.

2 - Authentication Views and URLs: Django includes pre-built views and URL patterns for common authentication actions:

- login/
- logout/
- password_change/
- password_change/done/
- password_reset/
- password_reset/done/
- reset/<uidb64>/<token>/
- reset/done/

By simply including django.contrib.auth.urls in our urls.py and creating custom templates for these views, we can get a fully functional authentication system with minimal effort.

3 - Extending the User Model (User Profile): For any additional user-specific information (e.g., a bio, profile picture, phone number), Django strongly recommends creating a separate "profile" model that has a OneToOneField relationship with the User model. This keeps authentication concerns separate from user data and allows for flexible extension without modifying Django's core User model directly. We can then easily create and update this profile information when users register or update their details. Signals (like post_save) can be used to automatically create a UserProfile whenever a new User is created.

4 - Forms for Registration and Updates: Django's UserCreationForm and UserChangeForm are excellent starting points for handling user registration and updates. These forms are based on the User model and can be easily customized or extended to include fields from our custom UserProfile model. This allows us to build our registration and profile update forms with Django's powerful form handling.

5 - Security: Django's built-in authentication system is designed with security in mind, handling password hashing, session management, and common vulnerabilities. By sticking to the default, we benefit from the continuous security improvements and best practices maintained by the Django community.

6 - Simplicity and Control: For projects with straightforward authentication requirements, using Django's defaults offers greater control and a simpler setup. We avoid introducing an external dependency, reducing potential complexity and the learning curve associated with a new library. We have direct control over the templates, views, and forms, allowing for precise customization.

## Why AllAuth is Unnecessary (for this project)

Django AllAuth is a fantastic and comprehensive package that offers a wide array of features, particularly for more complex authentication needs. However, for our project, these advanced features are currently not required, making AllAuth an unnecessary addition:

- Social Authentication (Google, Facebook, etc.): AllAuth excels at integrating with various social login providers. If our project required users to sign up or log in via Google, Facebook, Twitter, etc., AllAuth would be a strong contender. However, our current scope only requires traditional username/email and password authentication.
    
- Email Verification Workflows: While Django's default system can be extended for email verification, AllAuth provides robust, ready-to-use email verification workflows (mandatory, optional, none). Our current needs for email verification are basic and can be handled with simpler custom logic.
    
- Account Management Beyond Basic Updates: AllAuth includes more advanced account management features like linking/unlinking multiple email addresses, managing social account connections, etc. These features are not part of our initial requirements.
    
- Pre-built Templates and Views (Opinionated): AllAuth provides a set of pre-built templates and views that can accelerate development. However, these are often more opinionated in their structure and styling, and customizing them to fit a unique design can sometimes be more involved than building custom templates from scratch with Django's default views.
    
- Increased Dependency: Every third-party library adds a dependency to the project, which can introduce overhead in terms of maintenance, updates, and potential conflicts. By using Django's default, we keep our dependency footprint smaller.

In summary, for our Django project's user authentication and profile functionality, the built-in features of Django are perfectly capable and provide a secure, flexible, and maintainable solution without the added complexity of a larger third-party library like Django AllAuth. We can achieve all our requirements by extending and customizing Django's powerful default authentication system.