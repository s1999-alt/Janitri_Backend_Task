# Janitri Backend Assignment

## 📌 Overview
This project is a **Django REST Framework (DRF)** backend assignment for managing:
- **Users (Admins, Doctors, Nurses)**
- **Patients**
- **Heart Rate Data**

It implements **JWT authentication**, **role-based access control**, **pagination**, **filtering**, **unit tests**, and follows clean and extendible design practices.

---

## 🚀 Features
- **Custom User model** with roles: `admin`, `doctor`, `nurse`
- **Authentication & Authorization** using JWT (via SimpleJWT)
- **Role-based access**:
  - Admin → create doctors/nurses, manage everything
  - Doctor → manage patients & heart rates
  - Nurse → view-only (patients & heart rates)
- **Patients**: CRUD APIs (restricted create permissions)
- **Heart Rate Records**: record & retrieve with filtering (by patient, date range)
- **Pagination & filtering** for large datasets
- **Unit tests** for all major functionality
- **Clean, professional structure** (apps: `users`, `patients`, `heartbeats`)

---

## 🛠️ Tech Stack
- Python 3.10+  
- Django 5+  
- Django REST Framework  
- SimpleJWT (for authentication)  
- django-filter (for filtering)  
- SQLite (default, easy setup) / PostgreSQL (production ready)  

---

## ⚙️ Setup Instructions

### 1. Clone repo
```bash
git clone https://github.com/your-username/janitri-backend.git
cd janitri-backend
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate  # Windows
```

### 3. Install dependencies   
```bash
pip install -r requirements.txt
``` 

```bash
```   
### 4. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate  
```   

### 5. Create a superuser (Admin)
```bash
python manage.py createsuperuser 
```  
This super-user credentials is used for creating the doctors. Login with this superuser crendetials(username, password). After login, you get the access token and refresh token, copy the access token and create a doctor with that token as bearer token.


### 6. Run server
```bash
python manage.py runserver
```   

### Server runs at:
👉 http://127.0.0.1:8000/


## Environment
- SECRET_KEY
- DEBUG
- DB settings (if using Postgres) otherwise use the default sqlite3


## 🔑 Authentication
JWT-based authentication using SimpleJWT


### Obtain token:
POST /api/users/login/
{
  "username": "admin",
  "password": "yourpassword"
}


### Response:
{
  "refresh": "refresh_token_here",
  "access": "access_token_here"
}


### Use in headers:
Authorization: Bearer <access_token>


## 📡 API Documentation
### Users
#### Endpoint	Method	Role	Description
/api/users/login/	POST	All	Login & get JWT tokens
/api/users/token/refresh/	POST	All	Refresh JWT
/api/users/create/	POST	Admin	Create doctor/nurse
/api/users/	GET	Admin	List all users

### Patients
#### Endpoint	Method	Role	Description
/api/patients/	GET	All roles	List patients (pagination, filtering, search)
/api/patients/	POST	Admin/Doctor	Create new patient
/api/patients/{id}/	GET	All roles	Get patient details

### Heartbeats
#### Endpoint	Method	Role	Description
/api/heartbeats/	POST	Admin/Doctor	Record heart rate for a patient
/api/heartbeats/list/	GET	All roles	List heart rates (filter by patient, date range)

### Example Heart Rate Record
{
  "patient": 1,
  "bpm": 86,
  "recorded_at": "2025-09-18 10:30:00"
}

## 🔍 Filtering & Pagination

### Patients API supports:
Search by name, medical_id

Filter by gender

### Heartbeats API supports:

patient ID

from_date and to_date

### Pagination:

Default: 10 items per page

Use ?page=2 for next page

### Example:

GET /api/heartbeats/list/?patient=1&from_date=2025-09-01T00:00:00&to_date=2025-09-10T23:59:59

## 🧪 Running Tests

Unit tests cover all major functionality.

### Run:
```bash
python manage.py test
```   

### Tests included:

Users: Admin can create doctors/nurses, non-admins cannot

Patients: Doctors can create patients, nurses cannot, all can view

Heartbeats: Doctors can record, nurses cannot, all can view

### 📂 Project Structure

janitri_backend/
├── users/         # custom User model + auth
├── patients/      # patient management
├── heartbeats/    # heart rate management
├── janitri_backend/ # settings, urls, wsgi
└── manage.py