# Bank Management System

A complete **Bank Management System** built using **Python**, **Object-Oriented Programming (OOP)**, **MySQL**, and **Streamlit**.

This project started as a simple terminal-based banking application using JSON file storage and was later upgraded into a modern interactive web application connected with a MySQL database.


# Features

## Terminal-Based Version

* Create Bank Account
* Deposit Money
* Withdraw Money
* Show Account Details
* Update Account Information
* Delete Account
* JSON-based local data storage


## Streamlit + MySQL Version

* Interactive Web Interface
* MySQL Database Integration
* Secure Environment Variables using `.env`
* Account Authentication using PIN
* Real-Time Balance Updates
* CRUD Operations
* Better Scalability compared to JSON storage


# Technologies Used

* Python
* Object-Oriented Programming (OOP)
* Streamlit
* MySQL
* dotenv
* JSON
* SQL


# Project Structure

```bash
Bank-Management-System/
│
├── app.py              # Streamlit Web Application
├── bank_raw.py         # Terminal-Based Banking System
├── db.sql              # MySQL Database Setup File
├── data.json           # JSON Database for Raw Version
├── .env                # Environment Variables
└── README.md
```


# Installation & Setup

## Clone Repository

```bash
git clone https://github.com/your-username/bank-management-system.git
cd bank-management-system
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt is not available:

```bash
pip install streamlit mysql-connector-python python-dotenv
```


# Setup MySQL Database

1. Open MySQL
2. Run the SQL file:

```sql
SOURCE db.sql;
```


# Configure Environment Variables

Create a `.env` file and add:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=bank_system
```


# Run Streamlit Application

```bash
streamlit run app.py
```


# Run Terminal Version

```bash
python bank.py
```


# Concepts Implemented

* Classes & Objects
* Encapsulation
* CRUD Operations
* Database Connectivity
* File Handling
* Environment Variables
* Input Validation
* Authentication System


# Learning Outcomes

Through this project, I learned:

* How real banking operations work internally
* Building scalable applications from scratch
* Transitioning from file storage to database systems
* Backend logic implementation using Python
* Developing interactive applications using Streamlit
* Managing sensitive credentials securely using `.env`


# Future Improvements

* Password Hashing
* Transaction History
* Money Transfer Between Accounts
* Admin Dashboard
* Email Notifications
* User Session Management
* Docker Deployment
