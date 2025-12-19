from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)

# ---------- DATABASE ----------
def get_db():
    con = sqlite3.connect("attendance.db")
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with get_db() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """)
        con.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT CHECK(status IN ('present','absent')) NOT NULL,
            UNIQUE(student_id, date),
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
        """)
        con.commit()


init_db()

# ---------- ROUTES ----------

@app.route("/")
def home():
    with get_db() as con:
        stats = con.execute("""
            SELECT
                COUNT(DISTINCT s.id) AS total_students,
                COUNT(DISTINCT a.date) AS total_days,
                SUM(a.status = 'present') AS total_present
            FROM students s
            LEFT JOIN attendance a ON s.id = a.student_id
        """).fetchone()

    return render_template("index.html", stats=stats)


@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            with get_db() as con:
                con.execute("INSERT INTO students (name) VALUES (?)", (name,))
                con.commit()
        return redirect("/add-student")

    return render_template("add_student.html")


@app.route("/attendance", methods=["GET", "POST"])
def mark_attendance():
    with get_db() as con:
        students = con.execute("SELECT * FROM students").fetchall()

    if request.method == "POST":
        attendance_date = request.form.get("date")

        with get_db() as con:
            for s in students:
                status = request.form.get(f"status_{s['id']}")
                if status:
                    con.execute("""
                        INSERT INTO attendance (student_id, date, status)
                        VALUES (?, ?, ?)
                        ON CONFLICT(student_id, date)
                        DO UPDATE SET status = excluded.status
                    """, (s["id"], attendance_date, status))
            con.commit()

        return redirect("/attendance")

    return render_template(
        "attendance.html",
        students=students,
        today=date.today().isoformat()
    )


@app.route("/report")
def report():
    with get_db() as con:
        report = con.execute("""
            SELECT s.name,
                   COUNT(a.id) AS total_days,
                   SUM(a.status = 'present') AS present_days
            FROM students s
            LEFT JOIN attendance a ON s.id = a.student_id
            GROUP BY s.id
        """).fetchall()

    return render_template("report.html", report=report)


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
