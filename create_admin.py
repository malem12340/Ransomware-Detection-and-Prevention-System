from db import Database
from werkzeug.security import generate_password_hash

db = Database()

fullname = "Administrator"

username = "admin"

email = "admin@gmail.com"

password = generate_password_hash("admin123")

query = """
INSERT INTO users
(fullname, username, email, password)
VALUES (%s,%s,%s,%s)
"""

values = (
    fullname,
    username,
    email,
    password
)

db.execute(query, values)

print("Admin user created successfully!")

db.close()