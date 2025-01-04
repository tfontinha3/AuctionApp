# Auction App

**Auction App** is a full-featured web application that allows users to participate in online auctions. The app includes user authentication, an admin panel, active listings, and a watchlist feature, providing a seamless auction experience.

## Features
- **User Authentication**: Secure login and registration for users to manage their accounts and bids.
- **Admin User Page**: Admin can manage users, listings, and view active auctions.
- **Active Listings**: View current active auction listings, place bids, and track auction status.
- **Watchlist**: Users can add items to their watchlist to keep track of auctions they’re interested in.

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: [Django/Flask/Other Backend Framework]
- **Database**: SQLite or PostgreSQL

## How to Use
1. Clone the repository:
   ```bash
   git clone https://github.com/tfontinha3/AuctionApp.git
   cd AuctionApp
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```
5. Open the app in your browser:
   `http://127.0.0.1:8000`

## Future Enhancements
- Implement payment processing for auction winners.
- Add real-time bidding updates with WebSockets.
- Support for auction item images.
