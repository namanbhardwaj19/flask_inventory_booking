# Flask Inventory Booking System

This is a Flask-based web application that allows users to upload CSV files, manage inventory, and handle bookings.

## Features
- **Upload CSV Files**: Import members and inventory data.
- **Book an Item**: Allow members to book an inventory item.
- **Cancel a Booking**: Members can cancel their bookings.
- **Database Management**: Uses SQLite and SQLAlchemy for handling database operations.

## Project Structure
```
flask_inventory_booking/
│── app/
│   │── __init__.py  # Flask app initialization
│   │── models.py    # Database models
│   │── routes.py    # API routes
│── migrations/      # Database migrations
│── instance/
│   │── config.py    # Application configuration
│── requirements.txt # Dependencies
│── run.py           # Run the Flask server
│── README.md        # Project documentation
```

## Installation
1. **Clone the Repository**
   ```sh
   git clone https://github.com/your-repo/flask-inventory-booking.git
   cd flask-inventory-booking
   ```

2. **Create a Virtual Environment (Optional but Recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up the Database**
   ```sh
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. **Run the Application**
   ```sh
   python run.py
   ```

## API Endpoints
### 1️⃣ Upload CSV
- **URL**: `POST /upload_csv`
- **Request**: Upload a CSV file with `multipart/form-data`

### 2️⃣ Book an Item
- **URL**: `POST /book`
- **Request JSON**:
  ```json
  {
      "member_id": 1,
      "inventory_id": 2
  }
  ```
- **Response JSON**:
  ```json
  {
      "success": "Booking confirmed"
  }
  ```

### 3️⃣ Cancel a Booking
- **URL**: `POST /cancel`
- **Request JSON**:
  ```json
  {
      "booking_id": 3
  }
  ```
- **Response JSON**:
  ```json
  {
      "success": "Booking cancelled"
  }
  ```

## Checking the Database
1. **Using SQLite CLI**:
   ```sh
   sqlite3 instance/database.db
   .tables
   SELECT * FROM member;
   .exit
   ```
2. **Using Flask Shell**:
   ```sh
   flask shell
   from app.models import Member, Inventory, Booking
   Member.query.all()
   ```

## License
This project is licensed under the MIT License.

