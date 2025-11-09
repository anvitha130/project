# api.py
from flask import Flask, request, jsonify
import sqlite3
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

app = Flask(__name__)

# ✅ Configure JWT secret key AFTER app is created
app.config["JWT_SECRET_KEY"] = "supersecretkey"  # later move to .env file
jwt = JWTManager(app)

# --- Database helper ---
def get_db_connection():
    conn = sqlite3.connect("career_counselor.db")
    conn.row_factory = sqlite3.Row
    return conn


# --- 1. Health check endpoint ---
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is working successfully!"})


# --- 2. Add a new user query ---
@app.route("/add_query", methods=["POST"])
@jwt_required()  # ✅ protect this endpoint
def add_query():
    data = request.get_json()
    user = get_jwt_identity()  # user from token
    question = data.get("question")
    response = data.get("response")

    if not all([question, response]):
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_queries (username, user_input, ai_response, response_type)
        VALUES (?, ?, ?, ?)
    """, (user, question, response, "text"))
    conn.commit()
    conn.close()

    return jsonify({"message": "Query added successfully!"})


# --- 3. Fetch all user queries ---
@app.route("/get_queries", methods=["GET"])
@jwt_required()
def get_queries():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_queries")
    rows = cursor.fetchall()
    conn.close()

    results = [dict(row) for row in rows]
    return jsonify(results)


# --- 4. Login route (generates JWT token) ---
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # simple dummy login for testing
    if username == "admin" and password == "1234":
        token = create_access_token(identity=username)
        return jsonify({"access_token": token})
    else:
        return jsonify({"error": "Invalid credentials"}), 401


# --- 5. Protected test route ---
@app.route("/secure_data", methods=["GET"])
@jwt_required()
def secure_data():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Welcome {current_user}, this is a protected route!"})


if __name__ == "__main__":
    app.run(debug=True)
