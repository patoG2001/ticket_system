import sqlite3
from werkzeug.security import generate_password_hash

# Conexión a la base de datos
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Datos del usuario
username = "DiegoVelzer"
password = "Silencio21"

# Hashear la contraseña
hashed = generate_password_hash(password)

# Insertar en la tabla users
cursor.execute("INSERT INTO admins (username, hash) VALUES (?, ?)", (username, hashed))

# Guardar y cerrar
conn.commit()
conn.close()
print("Usuario creado correctamente.")