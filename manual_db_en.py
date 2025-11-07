import sqlite3

def manual_entry():
    """Manually insert a user entry into the users table."""
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        # Prompt user for input
        print("Enter user details for manual entry:")
        email = input("Email: ")
        password_hash = input("Password Hash: ")
        avatar = input("Avatar (URL or file path): ")
        avatar_name = input("Avatar Name: ")
        name = input("Name: ")
        college_name = input("College Name (optional, press Enter to skip): ") or None
        cgpa = input("CGPA (e.g., 8.5, optional, press Enter to skip): ")
        cgpa = float(cgpa) if cgpa else None
        branch = input("Branch (e.g., Computer Science, optional, press Enter to skip): ") or None
        interest = input("Interest (e.g., Machine Learning, optional, press Enter to skip): ") or None
        desired_role = input("Desired Role (e.g., Software Engineer, optional, press Enter to skip): ") or None
        location = input("Location (e.g., New York, optional, press Enter to skip): ") or None
        resume = input("Resume (text or file path, optional, press Enter to skip): ") or None
        github_link = input("GitHub Link (optional, press Enter to skip): ") or None
        linkedin_link = input("LinkedIn Link (optional, press Enter to skip): ") or None
        experience = input("Experience (e.g., Internship at XYZ, optional, press Enter to skip): ") or None
        career_path = input("Career Path (JSON or text, optional, press Enter to skip): ") or None

        # Insert data into the users table
        cursor.execute('''
            INSERT INTO users (
                email, password_hash, avatar, avatar_name, name, college_name, cgpa, branch, interest, desired_role, location,
                resume, github_link, linkedin_link, experience, career_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            email, password_hash, avatar, avatar_name, name, college_name, cgpa, branch, interest, desired_role, location,
            resume, github_link, linkedin_link, experience, career_path
        ))

        # Commit the transaction
        conn.commit()
        print(f"✅ Successfully inserted user '{name}' into the database.")

    except sqlite3.Error as e:
        print(f"❌ Error inserting data: {e}")
    except ValueError as e:
        print(f"❌ Invalid input (e.g., CGPA must be a number): {e}")
    finally:
        # Close the connection
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    manual_entry()