# Auction Project

This is an auction web application built with Django. Users can create listings, place bids, and comment on listings. The application also supports user authentication and category-based listing organization.


## Features

- User authentication (login, logout, register)
- Create, edit, and delete auction listings
- Place bids on listings
- Comment on listings
- View listings by category
- Watchlist functionality

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/shuklatul1021/Auctions.git
    cd commerce
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Apply migrations:
    ```sh
    python manage.py migrate
    ```

4. Run the development server:
    ```sh
    python manage.py runserver
    ```

## Deployment

This project is configured to be deployed on Vercel.
https://auctions-one.vercel.app/
