# Library Management API

This project is a **Library Management System API** developed using Django and Django REST Framework (DRF). It provides functionality for managing books, borrowing, and returning operations, with distinct permissions for administrators and general users. JWT authentication is implemented for secure access control.

## Features

- **JWT Authentication**: Secures API endpoints using JSON Web Tokens.
- **User Authentication**: Supports user login and authentication using Django's built-in `User` model.
- **Book Management**: CRUD operations for books with permissions.
  - Administrators can perform full CRUD operations.
  - General users have read-only access.
- **Borrow and Return Books**:
  - Users can borrow books if available and return them with fine calculation for overdue returns.
  - Borrowing is limited to 5 books per user.
- **Permissions**:
  - Admins: Full access.
  - General Users: Restricted access.
- **Custom Actions**:
  - Borrow a book.
  - Return a book with automatic fine calculation.
- **Pagination**: Custom pagination for managing API responses.

## Requirements

- Python
- Django
- Django REST Framework
- djangorestframework-simplejwt

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/raiyan12999/library-management-api.git
   cd library-management-api
   ```

2. Set up a virtual environment and activate it:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations to set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the API at:
   ```
   http://127.0.0.1:8000/
   ```

## Models

### Book
Represents books available in the library.

Fields:
- `title` (CharField): Title of the book.
- `availability` (BooleanField): Indicates if the book is available for borrowing.

### Borrowed
Records borrowed books and their associated details.

Fields:
- `user` (ForeignKey): The user who borrowed the book.
- `book` (ForeignKey): The book being borrowed.
- `borrowing_date` (DateField): Auto-set to the date of borrowing.
- `return_deadline` (DateField): Deadline for returning the book (default is 14 days from borrowing).
- `returned` (BooleanField): Indicates if the book has been returned.

Methods:
- `calculate_fine`: Calculates the fine for overdue books (BDT 5 per day).

## API Endpoints

### Authentication
- `/api/token/`: Obtain a JWT token.
- `/api/token/refresh/`: Refresh an existing JWT token.

### Books
- `GET /books/`: List all books.
- `POST /books/`: Create a new book (Admin only).
- `PUT /books/{id}/`: Update a book (Admin only).
- `DELETE /books/{id}/`: Delete a book (Admin only).

### Borrowed
- `GET /borrowed/`: List borrowed books for the logged-in user.
- `POST /borrowed/{id}/borrow/`: Borrow a book.
- `POST /borrowed/{id}/return_book/`: Return a book and calculate fines.

## Permissions

### Custom Permissions
- **IsAdminOrReadOnly**: Grants full access to admins; read-only access to general users.
- **IsMember**: Restricts actions to authenticated non-admin users.

### Default Permissions
- Admins: Full CRUD access.
- Users: Read-only for books and limited borrowing actions.

## Pagination

The API uses custom pagination:
- Default page size: 5 items.
- Maximum page size: 20 items.

### Customize page size:
Add `?page_size={size}` to your API request.

## Fine Calculation

Overdue fines are calculated at **BDT 5 per day** beyond the return deadline. The fine is displayed in the response when a user returns an overdue book.

## Example Usage

### Obtain JWT Token
```bash
POST /api/token/
Body:
{
  "username": "john_doe",
  "password": "password123"
}
Response:
{
  "access": "<your_access_token>",
  "refresh": "<your_refresh_token>"
}
```

### Borrow a Book
```bash
POST /borrowed/{book_id}/borrow/
Headers:
  Authorization: Bearer <your_access_token>
Response:
{
  "id": 1,
  "user": {
    "id": 2,
    "username": "john_doe",
    "is_staff": false
  },
  "book": {
    "id": 5,
    "title": "Learn Python",
    "availability": false
  },
  "borrowing_date": "2024-12-10",
  "return_deadline": "2024-12-24",
  "returned": false
}
```

### Return a Book
```bash
POST /borrowed/{book_id}/return_book/
Headers:
  Authorization: Bearer <your_access_token>
Response:
{
  "message": "Book \"Learn Python\" returned successfully.",
  "fine": 10
}
```

## Contact

For any queries, feel free to reach out to me at [raiyanbinatik.m29@gmail.com](mailto:raiyanbinatik.m29@gmail.com).
