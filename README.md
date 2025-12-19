# Student Attendance Tracker

A simple web-based student attendance tracking system built using **Flask** and **SQLite**.  
This project focuses on backend fundamentals such as routing, database design, and data consistency.

---

## Features

- Add students to the system
- Mark attendance for each student by date
- Update attendance automatically if already marked
- View attendance report with percentage calculation
- Clean and minimal user interface

---

## Tech Stack

- **Backend:** Python, Flask  
- **Database:** SQLite  
- **Frontend:** HTML, CSS (no JavaScript)  

---

## Project Structure

student-attendance-tracker/
├── app.py
├── templates/
│ ├── index.html
│ ├── add_student.html
│ ├── attendance.html
│ └── report.html
├── static/
│ └── style.css
├── .gitignore
└── README.md



---

## How It Works

- Students are stored in a `students` table
- Attendance records are stored in an `attendance` table
- Each student can have only one attendance record per date
- If attendance is submitted again for the same student and date, it updates the existing record instead of creating duplicates

---

## Setup Instructions

1. Clone the repository
   ```bash
   git clone https://github.com/<your-username>/student-attendance-tracker.git
   cd student-attendance-tracker


2. Create and activate a virtual environment (optional but recommended)

3. Install Flask

4. pip install flask


5. Run the application

    python app.py


6. Open your browser and visit

    http://127.0.0.1:5000/


The database is created automatically on first run.

## Learning Outcomes

- Understanding Flask routing and request handling

- Using SQLite with relational design and constraints

- Handling form submissions with GET and POST

- Preventing duplicate records using database constraints

- Rendering dynamic data using Jinja templates

## Notes

- This project is intended for learning and demonstration purposes

- No authentication or user roles are implemented

- Focus is on backend logic rather than advanced UI or frontend frameworks