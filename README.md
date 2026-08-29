# BlogPost

BlogPost is a Django-based blogging web application where users can create accounts, publish posts, interact with other users' posts, and manage their profiles.

## Repository

GitHub Repository: https://github.com/vrushang922/Blog-Post.git

## Features

### User Authentication
- Users can create a new account.
- Registered users can log in and log out.
- Only authenticated users can create and manage posts.

### Blog Posts
- Logged-in users can create new blog posts.
- Users can edit or delete their own posts.
- Published posts are visible to everyone on the home page.
- Visitors who are not logged in can read posts but cannot create, edit, like, or comment on posts.

### User Profiles
- Every registered user has a profile.
- Users can upload or set a profile avatar.
- Users can edit their profile information.
- Users can view posts published by other users.

### Likes
- Logged-in users can like and unlike posts.
- Like counts are displayed on posts.

### Comments
- Logged-in users can comment on individual blog posts.
- Comments are displayed on the corresponding post detail page.

## User Permissions

| Feature | Guest User | Logged-in User | Post Owner |
|---|---|---|---|
| View posts | Yes | Yes | Yes |
| Create posts | No | Yes | Yes |
| Edit own posts | No | No | Yes |
| Delete own posts | No | No | Yes |
| Like posts | No | Yes | Yes |
| Comment on posts | No | Yes | Yes |

## Tech Stack

- Python
- Django
- HTML
- CSS
- Bootstrap
- SQLite
- Django Templates
- Django Authentication System

## How It Works

1. A user creates an account.
2. The user logs in with their account.
3. The user can create a blog post.
4. The post appears on the main page and can be viewed by other users and visitors.
5. Logged-in users can like and comment on posts.
6. The author can edit or delete their own posts.
7. Users can create and update their profile and avatar.

## Installation

Clone the repository:

```bash
git clone https://github.com/vrushang922/Blog-Post.git
cd mysite
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run database migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

## Admin Panel

Create a superuser:

```bash
python manage.py createsuperuser
```

Then open:

```text
http://127.0.0.1:8000/admin/
```

## Project Purpose

This project was built to practice and demonstrate Django web development concepts such as:

- User authentication and authorization
- CRUD operations
- Django models and relationships
- User profiles
- File/image uploads
- Likes and comments
- Permissions
- Django templates
- Pagination
- Form handling
