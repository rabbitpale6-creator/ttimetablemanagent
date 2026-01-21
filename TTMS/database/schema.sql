CREATE DATABASE IF NOT EXISTS timetable_db4;
USE timetable_db4;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    role ENUM('admin', 'faculty', 'student')
);

CREATE TABLE staff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    weekly_hours INT NOT NULL,
    year VARCHAR(10) NOT NULL,
    course VARCHAR(20) NOT NULL,
    UNIQUE (code, year, course)
);

CREATE TABLE staff_subjects (
    staff_id INT NOT NULL,
    subject_id INT NOT NULL,
    PRIMARY KEY (staff_id, subject_id),
    FOREIGN KEY (staff_id) REFERENCES staff(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

CREATE TABLE classrooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_no VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE timetable (
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
);
INSERT INTO staff (name) VALUES
('Dr. Ravi'),
('Ms. Anita'),
('Mr. Kumar'),
('Dr. Suresh'),
('Ms. Priya');
INSERT INTO classrooms (room_no) VALUES
('C101'),
('C102'),
('C103'),
('LAB1'),
('LAB2');
INSERT INTO subjects (code, name, weekly_hours, year, course) VALUES
('MATH1', 'Engineering Mathematics I', 4, 'I', 'CSE'),
('PHY', 'Engineering Physics', 3, 'I', 'CSE'),
('C_PROG', 'C Programming', 4, 'I', 'CSE');
INSERT INTO subjects (code, name, weekly_hours, year, course) VALUES
('DS', 'Data Structures', 4, 'II', 'CSE'),
('OOPS', 'Object Oriented Programming', 3, 'II', 'CSE'),
('DBMS', 'Database Management Systems', 3, 'II', 'CSE');
INSERT INTO subjects (code, name, weekly_hours, year, course) VALUES
('AI', 'Artificial Intelligence', 4, 'III', 'AIDS'),
('ML', 'Machine Learning', 3, 'III', 'AIDS'),
('BD', 'Big Data Analytics', 3, 'III', 'AIDS');
INSERT INTO subjects (code, name, weekly_hours, year, course) VALUES
('VLSI', 'VLSI Design', 4, 'IV', 'ECE'),
('ES', 'Embedded Systems', 3, 'IV', 'ECE'),
('CN', 'Computer Networks', 3, 'IV', 'ECE');
INSERT INTO users (username, password, role) VALUES
('admin', 'admin123', 'admin'),
('faculty1', 'faculty123', 'faculty'),
('student1', 'student123', 'student');
INSERT INTO staff_subjects (staff_id, subject_id) VALUES
-- Dr. Ravi
(1, 1), (1, 4), (1, 7),

-- Ms. Anita
(2, 2), (2, 5), (2, 8),

-- Mr. Kumar
(3, 3), (3, 6), (3, 9),

-- Dr. Suresh
(4, 10), (4, 11),

-- Ms. Priya
(5, 12);
SELECT * FROM staff;
SELECT code, name, year, course FROM subjects ORDER BY year, course;
SELECT st.name, sb.code
FROM staff_subjects ss
JOIN staff st ON ss.staff_id = st.id
JOIN subjects sb ON ss.subject_id = sb.id;