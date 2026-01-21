import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='nazila',
    database='timetable_db4'
)

cur = conn.cursor()

try:
    # Insert staff
    cur.execute("""
        INSERT INTO staff (name) VALUES
        ('Dr. Ravi'),
        ('Ms. Anita'),
        ('Mr. Kumar'),
        ('Dr. Suresh'),
        ('Ms. Priya')
    """)
    print("✓ Staff inserted")
    
    # Insert classrooms
    cur.execute("""
        INSERT INTO classrooms (room_no) VALUES
        ('C101'),
        ('C102'),
        ('C103'),
        ('LAB1'),
        ('LAB2')
    """)
    print("✓ Classrooms inserted")
    
    # Insert subjects
    cur.execute("""
        INSERT INTO subjects (code, name, weekly_hours, year, course) VALUES
        ('MATH1', 'Engineering Mathematics I', 4, 'I', 'CSE'),
        ('PHY', 'Engineering Physics', 3, 'I', 'CSE'),
        ('C_PROG', 'C Programming', 4, 'I', 'CSE'),
        ('DS', 'Data Structures', 4, 'II', 'CSE'),
        ('OOPS', 'Object Oriented Programming', 3, 'II', 'CSE'),
        ('DBMS', 'Database Management Systems', 3, 'II', 'CSE'),
        ('AI', 'Artificial Intelligence', 4, 'III', 'AIDS'),
        ('ML', 'Machine Learning', 3, 'III', 'AIDS'),
        ('BD', 'Big Data Analytics', 3, 'III', 'AIDS'),
        ('VLSI', 'VLSI Design', 4, 'IV', 'ECE'),
        ('ES', 'Embedded Systems', 3, 'IV', 'ECE'),
        ('CN', 'Computer Networks', 3, 'IV', 'ECE')
    """)
    print("✓ Subjects inserted")
    
    # Insert users
    cur.execute("""
        INSERT INTO users (username, password, role) VALUES
        ('admin', 'admin123', 'admin'),
        ('faculty1', 'faculty123', 'faculty'),
        ('student1', 'student123', 'student')
    """)
    print("✓ Users inserted")
    
    # Create timetable
    cur.execute("""
        CREATE TABLE IF NOT EXISTS timetable (
            id INT AUTO_INCREMENT PRIMARY KEY,
            day ENUM('Monday','Tuesday','Wednesday','Thursday','Friday') NOT NULL,
            period INT NOT NULL CHECK (period BETWEEN 1 AND 7),
            subject_id INT NOT NULL,
            staff_id INT NOT NULL,
            classroom_id INT NOT NULL,
            year VARCHAR(10) NOT NULL,
            course VARCHAR(20) NOT NULL,
            FOREIGN KEY (subject_id) REFERENCES subjects(id),
            FOREIGN KEY (staff_id) REFERENCES staff(id),
            FOREIGN KEY (classroom_id) REFERENCES classrooms(id),
            UNIQUE (day, period, staff_id),
            UNIQUE (day, period, classroom_id)
        )
    """)
    print("✓ Timetable created")
    
    # Insert staff-subject assignments
    cur.execute("""
        INSERT INTO staff_subjects (staff_id, subject_id) VALUES
        (1, 1), (1, 4), (1, 7),
        (2, 2), (2, 5), (2, 8),
        (3, 3), (3, 6), (3, 9),
        (4, 10), (4, 11),
        (5, 12)
    """)
    print("✓ Staff-subject assignments inserted")

    conn.commit()
    print("\n✅ Database setup complete!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()

finally:
    cur.close()
    conn.close()
