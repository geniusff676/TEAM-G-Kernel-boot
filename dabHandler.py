import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import logging
import os

# ✅ Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# ✅ Allow CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# ✅ Handle preflight requests (CORS OPTIONS method)
@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, GET, PUT, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, ngrok-skip-browser-warning')
        return response

# ✅ Initialize Firebase Admin SDK
cred = credentials.Certificate("popuauth.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# ✅ SQLite Database Configuration
DATABASE = 'user_data.db'

def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row  # ✅ Allows dict-like access to rows
        logging.info("✅ Database connected successfully!")
        return conn
    except Exception as e:
        logging.error(f"❌ Database connection failed: {e}")
        return None

# ✅ Initialize Database Schema
def init_db():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
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
        logging.info("✅ Database initialized successfully!")

# ✅ Initialize database on startup
init_db()


# **Signup Route**
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()

    try:
        # ✅ Create user in Firebase Authentication
        user = auth.create_user(
            email=data.get("email"),
            password=data.get("password"),
            display_name=data.get("name")
        )
        uid = user.uid

        # ✅ Store user data in SQLite
        cursor.execute(
            """
            INSERT INTO users (email, password_hash, avatar, avatar_name, name, 
                               college_name, cgpa, branch, interest, desired_role, 
                               location, resume, github_link, linkedin_link, 
                               experience, career_path) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.get("email"),
                data.get("password"),  # ⚠️ Store hashed password in production
                data.get("avatar", ""),
                data.get("avatarName", ""),
                data.get("name"),
                data.get("collegeName"),
                data.get("cgpa"),
                data.get("branch"),
                data.get("interest"),
                data.get("desiredRole"),
                data.get("location"),
                data.get("resume"),
                data.get("githubLink"),
                data.get("linkedinLink"),
                data.get("experience"),
                data.get("careerPath")
            )
        )

        user_id = cursor.lastrowid
        logging.info(f"✅ User inserted with ID: {user_id}")

        conn.commit()
        return jsonify({"message": "User registered successfully!", "uid": uid, "user_id": user_id}), 201

    except Exception as e:
        conn.rollback()
        logging.error(f"❌ Signup error: {e}")
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()


# **Login Route**
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if not user:
            logging.error("❌ No user found with this email")
            return jsonify({"error": "Invalid credentials"}), 401

        stored_password = user['password_hash']

        if stored_password != password:
            logging.error("❌ Incorrect password")
            return jsonify({"error": "Invalid credentials"}), 401

        user_record = auth.get_user_by_email(email)
        token = auth.create_custom_token(user_record.uid).decode("utf-8")

        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": {
                "email": email,
                "name": user['name'],
                "uid": user_record.uid,
                "avatar": user['avatar'] or "default.png",
                "avatarName": user['avatar_name']
            }
        }), 200

    except Exception as e:
        logging.error(f"❌ Login error: {e}")
        return jsonify({"error": str(e)}), 401

    finally:
        cursor.close()
        conn.close()


# ✅ Token Verification Function
def verify_token(token):
    try:
        return auth.verify_id_token(token)
    except auth.InvalidIdTokenError:
        return None, "Invalid token"
    except auth.ExpiredIdTokenError:
        return None, "Token expired"
    except Exception as e:
        logging.error(f"❌ Token verification error: {e}")
        return None, "Unknown error"


# **Fetch User Profile (Complete Profile)**
@app.route('/profile', methods=['GET'])
def get_user_profile():
    email = request.args.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user:
            return jsonify({
                "user_id": user['user_id'],
                "email": user['email'],
                "name": user['name'],
                "avatar": user['avatar'] or "default.png",
                "avatarName": user['avatar_name'],
                "collegeName": user['college_name'],
                "cgpa": user['cgpa'],
                "branch": user['branch'],
                "interest": user['interest'],
                "desiredRole": user['desired_role'],
                "location": user['location'],
                "resume": user['resume'],
                "githubLink": user['github_link'],
                "linkedinLink": user['linkedin_link'],
                "experience": user['experience'],
                "careerPath": user['career_path']
            }), 200

        return jsonify({"error": "User not found"}), 404

    except Exception as e:
        logging.error(f"❌ Profile fetch error: {e}")
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()


# **Update User Profile**
@app.route('/profile', methods=['PUT'])
def update_user_profile():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()

    try:
        # Build dynamic update query
        update_fields = []
        values = []

        for field in ['name', 'avatar', 'avatar_name', 'college_name', 'cgpa', 
                      'branch', 'interest', 'desired_role', 'location', 'resume', 
                      'github_link', 'linkedin_link', 'experience', 'career_path']:
            
            # Convert camelCase to snake_case for database
            db_field = field
            json_field = ''.join(['_' + c.lower() if c.isupper() else c for c in field]).lstrip('_')
            
            # Check both snake_case and camelCase versions
            if field in data or json_field in data:
                update_fields.append(f"{field} = ?")
                values.append(data.get(field) or data.get(json_field))

        if not update_fields:
            return jsonify({"error": "No fields to update"}), 400

        values.append(email)
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE email = ?"
        
        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "Profile updated successfully"}), 200

    except Exception as e:
        conn.rollback()
        logging.error(f"❌ Profile update error: {e}")
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()


# **Run Flask App on Port 5002**
if __name__ == "__main__":
    app.run(debug=True, port=5002)