# NiezbednikUcznia

**Final Python Project** – Developed by Ewa Grochola, Urszula Kępka
**Technologies used:** Python, SQLite, SQLAlchemy

## Project Overview

**NiezbednikUcznia** is a final-year Python project developed in collaboration by two PJATK students. The application serves as a comprehensive toolkit for students, providing features such as a weekly schedule, grade statistics, and subject-specific performance tracking.

The application supports **multiple user roles**, each with distinct functionalities:
- **Student** – View timetable, check grades, analyze statistics
- **Teacher** – Manage grades,  view timetable
- **Admin** – Full access to all data and user management

## Key Features

- **User Authentication** with hashed password encryption
- **Role-based Access Control** – Different permissions for students, teachers, and admins
- **Timetable Management** – Weekly schedule overview
- **Grade Tracking & Statistics** – View and analyze performance across subjects
- **Multi-table Structure** using **SQLite** and **SQLAlchemy ORM** – Efficient data handling with relationships between tables
- **PDF Export** – Generate reports for schedules or grades
- **Data Encryption** – Secure password storage using hashing techniques

## Technologies

- Python
- SQLite (lightweight relational database)
- SQLAlchemy (ORM for database operations)
- FPDF (for PDF exports)
- bcrypt (for password hashing)

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/NiezbednikUcznia.git
   cd NiezbednikUcznia
