from flask import Flask, render_template, request, redirect, session
import pymysql
import random
import sys
import os

# Add parent directory to path to import utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.auth import login_required

# Get the parent directory (project root)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__, 
    template_folder=os.path.join(BASE_DIR, 'template'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.secret_key = "timetable_secret_key"

# ---------------- DB CONNECTION ----------------
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="nazila",
        database="timetable_db4",
        cursorclass=pymysql.cursors.DictCursor
    )

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT role FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            role = user["role"]
            session["role"] = role

            if role == "admin":
                return redirect("/admin")
            elif role == "faculty":
                return redirect("/faculty")
            else:
                return redirect("/student")

        return "Invalid Login"

    return render_template("login.html")

# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin")
@login_required(role="admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")

# ---------------- STUDENT DASHBOARD ----------------
@app.route("/student")
@login_required(role="student")
def student_dashboard():
    return render_template("student_dashboard.html")

# ---------------- FACULTY DASHBOARD ----------------
@app.route("/faculty", methods=["GET", "POST"])
@login_required(role="faculty")
def faculty_dashboard():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM staff")
    staff_list = cur.fetchall()

    schedule = None

    if request.method == "POST":
        staff_id = request.form["staff_id"]
        cur.execute("""
            SELECT t.day, t.period, s.code, s.name, t.year, t.course
            FROM timetable t
            JOIN subjects s ON t.subject_id = s.id
            WHERE t.staff_id = %s
            ORDER BY t.day, t.period
        """, (staff_id,))
        schedule = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "faculty_dashboard.html",
        staff_list=staff_list,
        schedule=schedule
    )

# ---------------- AI TIMETABLE GENERATION ----------------
@app.route("/generate", methods=["POST"])
@login_required(role="admin")
def generate_timetable():
    year = request.form["year"]
    course = request.form["course"]

    conn = get_db_connection()
    cur = conn.cursor()

    # Delete existing timetable
    cur.execute(
        "DELETE FROM timetable WHERE year=%s AND course=%s",
        (year, course)
    )

    # Get subjects for that year & course
    cur.execute("""
        SELECT ss.subject_id, ss.staff_id
        FROM staff_subjects ss
        JOIN subjects s ON ss.subject_id = s.id
        WHERE s.year=%s AND s.course=%s
    """, (year, course))
    assignments = cur.fetchall()

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    periods = [1, 2, 3, 4, 5, 6, 7, 8]

    staff_busy = {}
    room_busy = {}

    # Get available classrooms
    cur.execute("SELECT id FROM classrooms")
    rooms = [r["id"] for r in cur.fetchall()]
    if not rooms:
        rooms = [1]  # Default room ID

    random.shuffle(assignments)

    for assignment in assignments:
        subject_id = assignment["subject_id"]
        staff_id = assignment["staff_id"]
        placed = False
        random.shuffle(days)

        for day in days:
            random.shuffle(periods)
            for period in periods:
                if (staff_id, day, period) in staff_busy:
                    continue
                room = rooms[0] if rooms else 1
                if (room, day, period) in room_busy:
                    continue

                cur.execute("""
                    INSERT INTO timetable
                    (day, period, subject_id, staff_id, classroom_id, year, course)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                """, (day, period, subject_id, staff_id, room, year, course))

                staff_busy[(staff_id, day, period)] = True
                room_busy[(room, day, period)] = True
                placed = True
                break

            if placed:
                break

    conn.commit()
    cur.close()
    conn.close()

    return redirect(f"/view_timetable?year={year}&course={course}")

# ---------------- FETCH TIMETABLE ----------------
def get_timetable_dict(year, course):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            t.day,
            t.period,
            s.code,
            s.name,
            st.name as staff_name
        FROM timetable t
        JOIN subjects s ON t.subject_id = s.id
        JOIN staff st ON t.staff_id = st.id
        WHERE t.year=%s AND t.course=%s
        ORDER BY t.day, t.period
    """, (year, course))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    timetable = {
        "Monday": [""] * 8,
        "Tuesday": [""] * 8,
        "Wednesday": [""] * 8,
        "Thursday": [""] * 8,
        "Friday": [""] * 8
    }

    for row in rows:
        day = row["day"]
        period = row["period"]
        code = row["code"]
        name = row["name"]
        staff = row["staff_name"]
        timetable[day][period - 1] = (
            f"<b>{code}</b><br>"
            f"<small>{name}</small><br>"
            f"<small>{staff}</small>"
        )

    return timetable

# ---------------- VIEW TIMETABLE ----------------
@app.route("/view_timetable")
@login_required()
def view_timetable():
    year = request.args.get("year")
    course = request.args.get("course")

    timetable = get_timetable_dict(year, course)

    return render_template(
        "timetable_view.html",
        timetable=timetable,
        year=year,
        course=course
    )

# ---------------- PRINT ----------------
@app.route("/print")
@login_required()
def print_timetable():
    year = request.args.get("year")
    course = request.args.get("course")

    timetable = get_timetable_dict(year, course)

    return render_template(
        "timetable_print.html",
        timetable=timetable,
        year=year,
        course=course
    )

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)