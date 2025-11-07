import sqlite3

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    avatar TEXT NOT NULL,
    avatar_name TEXT NOT NULL,
    name TEXT NOT NULL,
    college_name TEXT,
    cgpa REAL,
    branch TEXT,
    interest TEXT,
    desired_role TEXT,
    location TEXT,
    resume TEXT,
    github_link TEXT,
    linkedin_link TEXT,
    experience TEXT,
    career_path TEXT
)
''')

conn.commit()
conn.close()
print("✅ Database and table created successfully with 'career_path' field.")
