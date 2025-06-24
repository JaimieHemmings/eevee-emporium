# Eevee Emporium

Eevee Emporium is my submission for the Code Institute Milestone 4 project. It is a full-stack e-commerce platform built using the Django framework, designed for Pokémon enthusiasts. The store allows users to browse, purchase, and manage orders for a variety of Pokémon-related items, including trading cards, accessories, and merchandise. The project leverages Django's robust back-end capabilities to handle product management, user authentication, and a secure checkout process. A key architectural decision was to utilize Django's built-in authentication system to provide a secure and streamlined user experience, focusing on core functionalities without the need for external packages.

![image](documentation/screenshot.png)

View the Website [Here.](https://eeveeemporium-a0b363641244.herokuapp.com/)

## UX Developments

### Strategy

#### Project Goals

    Develop a full-stack e-commerce website with full CRUD functionality.
    Guests can browse products, view details, and add items to the cart.
    Users can create an account, log in, and manage their personal profile and order history.
    Registered users can complete a secure checkout process to purchase items.
    Admins have full CRUD functionality for products, categories, and can manage all user orders.
    The website will be fully responsive, providing a seamless experience on all device sizes.
    Implement robust error handling and user feedback to ensure a smooth user journey.
    Ensure a clear and intuitive user interface for easy navigation and product discovery.

#### User Demographic

    Pokémon fans and collectors of all ages.
    Individuals looking to purchase Pokémon trading cards, merchandise, and accessories.
    Gift shoppers looking for Pokémon-related items.
    Potential employers evaluating full-stack development skills.

### User Stories

#### First-Time Visitor / Guest Goals

As a first-time visitor, I want to be able to:

    Immediately understand the site is an e-commerce store for Pokémon products.
    Easily navigate the site and browse through different product categories.
    Search for specific products.
    View detailed information and images for each product.
    Add products to my shopping bag.
    Easily register for a new account.

#### Registered User Goals

As a registered user, I want to be able to:

    Securely log in and out of my account.
    View and update my personal information and shipping details.
    View my past order history.
    Proceed through a secure and simple checkout process to buy items in my bag.
    Receive an order confirmation after purchase.

#### Site Admin Goals

As a site admin, I want to be able to:

    Add new products to the store, including details like name, description, price, and image.
    Edit existing product information.
    Delete products from the store.
    View and manage all customer orders.
    Manage product categories to organize the storefront.

### Scope

#### Functionality Planning

When planning the scope of the project I created a Viability Analysis of the features I wished to add. This would allow me to prioritise the most critical features and defer the development of lesser functionality to a later date. Below is that table:

| #   | Feature                                | Importance | Viability |
| --- | -------------------------------------- | ---------- | --------- |
| 1   | Product CRUD Functionality (Admin)     | 5          | 5         |
| 2   | User Registration & Login              | 5          | 5         |
| 3   | Shopping Cart Functionality            | 5          | 5         |
| 4   | Secure Checkout with Stripe            | 5          | 5         |
| 5   | User Profile & Order History           | 4          | 5         |
| 6   | Product Search & Filtering             | 4          | 4         |
| 7   | Product Category Management (Admin)    | 4          | 5         |
| 8   | Responsive Design                      | 5          | 5         |
| 9   | User Action Validation & Feedback      | 5          | 5         |
| 10  | Product Reviews & Ratings              | 3          | 4         |
| 11  | Stock/Inventory Management             | 4          | 4         |
| 12  | Wishlist Functionality                 | 2          | 3         |
| 13  | Admin Dashboard for Order Management   | 5          | 5         |

Based on the premise of creating a minimally viable product I have decided to focus on implementing only the core functionality for the application to meet the minimum required specifications for functionality. This means on the initial development sprint I will be implementing features 1, 2, 3, 4, 7 and 13.

#### Functionality Requirements

- Clean and thematically cohesive design
- Functional and aesthetic presentation of Products
- Comprehensive inventory management to add, edit and delete items
- Login/logout functionality
- Manage profile
- Full CRUD functionality
- Defensive programming usage to safeguard the database from malicious or erroneous input
- Appropriate handling of error messages

# Structure

## Topology Diagrams

Below are diagrams illustrating the pages that are accessible for users based on their session state (guest/logged in guest/admin), any page not listed in a diagram is designed not to be accessible by a user.

# Deployment and Local Development

## Deployment to Heroku

The project is deployed to Heroku from this repository, therefore the deployed version of the site is always up to date with this repository and the deployed code is the exact code as in this repository.

In order to clone this project follow the steps below (May vary depending on your development environment):

- Create a local Clone of this repository from GitHub
- Run `pip install -r requirements.txt`
- Log in to Heroku and create a new app and name it as required
- Choose your closest region for deployment
- Still in Heroku, navigate to deploy and select GithHub, then select your cloned repository and click "connect".
- Navigate to the Settings tab and set up your environment variables using the [env.py.example](env.py.example) for reference
- Then return to the Deploy section of the App in Heroku and enable automatic deploys.
- Click on the "Deploy Branch" option.
- It will take a few minutes to deploy, then you can click on "Open App" once it is complete.

## Cloning the Repo

In order to fork the repo, follow these steps:

- Locate the repository
- Click the button labelled "Code" to the top right of the screen
- Click HTTPS and copy the link provided
- In your local environment navigate to the desired directory
- Open a terminal and type "git clone repository-url"
- Press enter to begin the cloning process

## Forking the Repo

- Locate the repository on GitHub
- Click Fork in the top right corner
- If necassary, select the owner for the forked code under the Owner dropdown menu.
- Optionally, edit the Repository Name field to rename your forked repository
- Optionally, use the Description field to input a description of your fork
- Select "Copy the DEFAULT branch only"
  - This is another optional step, many scenarios only require a fork of the default branch. If you do not select this you will copy all branches into your fork
- Click Create Fork

## Create Virtual Environment

To create a virtual environment for the project open gitbash or CLI of your choice within the project directory. To do this follow the instructions below:

- Open the CLI in the project directory
- install virtual environment:
```python -m venv virt```

Then to run the virtual environment type:

- ```./virt/Scripts/activate```

Following this it is wise to install the dependencies:

- ```pip install -r requirements.txt```

Create superuser:
- ```python manage.py createsuperuser```

Follow prompts to add username, email and password.

Launch development server:
- ```python manage.py reunserver```

This process varies depending on your local development environment and operating system. If the above doesn't work you may need to search for instructions specific to your development environment. Please ensure you have Python installed.

## Create and migrate Database

Before launching the project you will also need to run the database migrations:

This assumed you have updated the local project ENV values based on the example provided.

- within the vvirtual environment run: ```python manage.py migrate```

# Credits

## Content

Various pokemon related Imagery was sourced from [Pokemon](https://www.pokemon.com/us)

For the design of the website I modified a publicly available Bootstrap Template: [Kaira](https://themewagon.com/themes/kaira/)

The Favicon was sourced from [Wikimedia](https://commons.wikimedia.org/wiki/File:Pok%C3%A9_Ball_icon.svg)

I then generated the appropriate icons using [Favicon Generator](https://realfavicongenerator.net/)

I aslo used this image available from [Alphacoders](https://wall.alphacoders.com/big.php?i=613932)

For image optimisation and conversions between file types I used [Squoosh](https://squoosh.app)

## Acknowledgements

Thanks again to my Mentor, Brian Macharia, for provided continuous feedback on my ideas and progress as well as the teams at Code Institute and East Kent College for their ongoing support.