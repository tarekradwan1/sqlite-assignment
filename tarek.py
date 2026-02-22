import sqlite3

# Connect to SQLite (in memory for testing)
conn = sqlite3.connect(':memory:')

# this is important because foreign keys are OFF by default in SQLite
conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()

# Helper function to inspect table contents
def print_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print(f"\nTable: {table_name}")
    print(" | ".join(columns))
    print("-" * 30)

    for row in rows:
        print(" | ".join(str(value) for value in row))

# Create tables
cursor.execute("""
CREATE TABLE student (
    student_id INT PRIMARY KEY,
    name TEXT NOT NULL,
    age INT
)
""")

cursor.execute("""
CREATE TABLE registered_courses (
    student_id INT,
    course_id INT,
    primary key(student_id, course_id)
)
""")


cursor.execute("""
CREATE TABLE grades (
    student_id INT,
    course_id INT,
    grade INT,
    primary key(student_id, course_id)
)
""")



students = [
    (10, 'Tarek', 30),
    (11, 'Taline', 31),
    (12, 'Issa', 32),
    (13, 'Reina', 33),
    (14, 'Moe', 34)
]

courses = [
    (10, 340),
    (11, 350),
    (12, 380)
    ]

grade = [
    (10, 340, 95),
    (11, 350, 97),
    (12, 380, 90)
    ]


cursor.executemany("INSERT INTO student VALUES (?, ?, ?)", students)
cursor.executemany("INSERT INTO registered_courses VALUES (?, ?)", courses)
cursor.executemany("INSERT INTO grades VALUES (?, ?, ?)", grade)

conn.commit()

print_table(cursor, "student")

print("\nMax grade per student:")
cursor.execute("""
SELECT student_id, course_id, MAX(grade)
FROM grades
GROUP BY student_id
""")
for row in cursor.fetchall():
    print(row)
    
    
print("\nAverage grade per student:")
cursor.execute("""
SELECT student_id, AVG(grade)
FROM grades
GROUP BY student_id
""")

for row in cursor.fetchall():
    print(row)


# Example SELECT query
cursor.execute("SELECT * FROM student")
print("\nResult of: SELECT * FROM student")
for row in cursor.fetchall():
    print(row)

conn.close()