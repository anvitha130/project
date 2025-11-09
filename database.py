import sqlite3
import datetime

# ======================================
# 🧩 1️⃣ Create or connect to database
# ======================================
def create_database():
    conn = sqlite3.connect('career_counselor.db')   # Creates the DB file if not present
    cursor = conn.cursor()

    # Create a table for user queries if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            input_text TEXT,
            response_text TEXT,
            input_type TEXT,
            timestamp TEXT
        )
    ''')

    conn.commit()
    conn.close()

# ======================================
# 🧩 2️⃣ Insert a new query and response
# ======================================
def insert_query(username, input_text, response_text, input_type):
    conn = sqlite3.connect('career_counselor.db')
    cursor = conn.cursor()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        INSERT INTO user_queries (username, input_text, response_text, input_type, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, input_text, response_text, input_type, timestamp))

    conn.commit()
    conn.close()

# ======================================
# 🧩 3️⃣ Fetch all previous user queries
# ======================================
def get_all_queries(username=None):
    conn = sqlite3.connect('career_counselor.db')
    cursor = conn.cursor()

    if username:
        cursor.execute('SELECT * FROM user_queries WHERE username = ?', (username,))
    else:
        cursor.execute('SELECT * FROM user_queries')

    rows = cursor.fetchall()
    conn.close()
    return rows

# ======================================
# 🧩 4️⃣ Run once to create DB and test
# ======================================
if __name__ == "__main__":
    create_database()
    insert_query("guest", "Career in AI?", "Learn Python and ML.", "text")
    data = get_all_queries()
    for row in data:
        print(row)
