# Main code
"""
app.py

Parts of this code adapted from CS50 Finance.
See https://cs50.harvard.edu/x/2023/psets/9/finance/

Part of the code was completed with the help of copilot and AI tools.
"""

# Import necessary libraries
import os
from flask import Flask, flash, redirect, render_template, request, session, g, url_for, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, generate_qr_code
from flask_sqlalchemy import SQLAlchemy

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies), more security
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Code made with the help of AI to obtain correctly the database in SQL
# Railway configuration

DATABASE_URL = os.environ.get("DATABASE_URL")

# Configure database connection
# Ajuste opcional: SQLAlchemy espera "postgresql://" en vez de "postgres://"
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------------------
# Ejemplo de modelo
# ---------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(200), nullable=False)

# ---------------------------
# End of DB setup
# ---------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# After request
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# R O U T E S

# Index
@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html")




# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    # Clean the session
    session.clear()
    # If for form submission
    if request.method == "POST":
        # Validate username 
        if not request.form.get("username"):
            return apology("Ingresa un nombre de usuario", 400)
        # Validate password 
        if not request.form.get("password"):
            return apology("Ingresa una contraseña", 400)
        # Connect to the database
        db = get_db()
        # SQL Query
        user = db.execute("SELECT * FROM admins WHERE username = ?", (request.form.get("username"),)).fetchone()
        # Validate user
        if user is None or not check_password_hash(user["hash"], request.form.get("password")):
            return apology("Usuario o contraseña incorrectos", 400)
        # Store user ID in session
        session["user_id"] = user["admin_id"]

        # Redirect to index
        return redirect("/")
    else:
        # Render login template
        return render_template("login.html")



# Logout
@app.route("/logout")
def logout():
    """Log user out"""
    # Clear session
    session.clear()
    # Redirect to login
    return redirect("/login")
    


# Add a fan
@app.route("/fan", methods=["GET", "POST"])
def fan():
    """Register a fan"""
    if request.method == "POST":
        # Variables
        fan_name = request.form.get("fan_name")
        phone_number = request.form.get("phone_number")
        age = request.form.get("age")
        email = request.form.get("email")
        
        # Get fan name
        if not fan_name:
            return apology("Ingresa el nombre del fan", 400)
        # Get phone_number
        elif not phone_number:
            return apology("¡Agrega el número de teléfono!", 400)
        # Get age
        elif not age:
            return apology("¿Cuántos años tiene tu fan?", 400)
        
        # Connect to the database
        db = get_db()
        # Check if fan already exists
        rows = db.execute("SELECT * FROM fans WHERE fan_name = ?", (fan_name,)).fetchall()
        if len(rows) > 0:
            return apology("¡Ese fan ya existe!", 400)
        # Register fan in database
        db.execute("INSERT INTO fans (fan_name, phone_number, email, age) VALUES(?,?,?,?)", (fan_name, phone_number, email, age))
        db.commit()

        # Add a flash message to confirm fan registration
        flash("¡Fan registrado exitosamente!", "success")
        # Redirect
        return redirect("/fan")
    else:
        # Render page
        return render_template("fan.html")



# Add a concert
@app.route("/concert", methods=["GET", "POST"])
def concert():
    """Register a concert"""
    if request.method == "POST":
        # Variables
        venue = request.form.get("venue")
        date = request.form.get("date")
        address = request.form.get("address")
        contact_name = request.form.get("contact_name")
        contact_email = request.form.get("contact_email")
        contact_phone = request.form.get("contact_phone")
        
        # Get venue name
        if not venue:
            return apology("Ingresa el nombre del venue", 400)
        # Get date
        elif not date:
            return apology("¡Agrega la fecha!", 400)
        # Get contact_name
        elif not contact_name:
            return apology("Ingresa el nombre del contacto", 400)
        # Get contact_phone
        elif not contact_phone:
            return apology("Ingresa el teléfono del contacto", 400)
        
        # Connect to the database
        db = get_db()
        # Register fan in database
        db.execute("INSERT INTO concerts (venue, date, address, contact_name, contact_email, contact_phone) VALUES(?,?,?,?,?,?)", (venue, date, address, contact_name, contact_email, contact_phone))
        db.commit()

        # Redirect
        return redirect("/concert")
    else:
        # Render page
        return render_template("concert.html")



# Generate ticket
@app.route("/ticket", methods=["GET", "POST"])
@login_required
def ticket():
    """Generate a ticket"""
    db = get_db()
    if request.method == "POST":
        # Variables
        fan_id = request.form.get("fan_id")
        concert_id = request.form.get("concert_id")
        admin_id = session.get("user_id")
        payment = request.form.get("payment")

        # Validate fan ID
        if not fan_id:
            return apology("Selecciona un fan", 400)
        # Validate concert ID
        elif not concert_id:
            return apology("Selecciona un concierto", 400)
        # Validate payment    
        elif not payment:
            return apology("Selecciona un metodo de pago", 400)

        # Register variables in database to generate ticket_id
        db.execute("INSERT INTO tickets (fan_id, concert_id, admin_id, payment) VALUES(?,?,?,?)", (fan_id, concert_id, admin_id, payment))
        db.commit()

        # Get the last ticket_id Extracted with the help of AI
        ticket_id = db.execute("SELECT last_insert_rowid() AS ticket_id").fetchone()["ticket_id"]
        
        # Get concert details
        concert = db.execute("SELECT * FROM concerts WHERE concert_id = ?", (concert_id,)).fetchone()
        venue = concert["venue"]
        address = concert["address"]
        date = concert["date"]

        # Generate QR CODE 
        qr_path = f"static/qr_codes/ticket_{ticket_id}.png"
        generate_qr_code(str(ticket_id), venue, address, date, qr_path)

        # Register QR code path in database
        db.execute("UPDATE tickets SET qr_code_path = ? WHERE ticket_id = ?", (qr_path, ticket_id))
        db.commit()
        
        # Flash message
        flash("¡Boleto generado exitosamente!")


        # Redirect to ticket page
        return redirect(url_for("ticket_generated", ticket_id=ticket_id))
    else:

        # Get fans and concerts for dropdowns
        fans = db.execute("SELECT * FROM fans").fetchall()
        concerts = db.execute("SELECT * FROM concerts").fetchall()
        
        # Render ticket page
        return render_template("ticket.html", fans=fans, concerts=concerts)



# Ticket generated
@app.route("/ticket_generated")
@login_required
def ticket_generated():
    """Display generated ticket"""
    # Ticket ID obtained with the help of AI
    ticket_id = request.args.get("ticket_id")
    if not ticket_id:
        return apology("Boleto no encontrado", 404)
    # Connect to the database
    db = get_db()
    # Get ticket details
    ticket = db.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,)).fetchone()
    
    # If ticket does not exist
    if ticket is None:
        return apology("Boleto no encontrado", 404)

    # Render ticket generated page
    return render_template("ticket_generated.html", ticket=ticket)




# Read ticket
@app.route("/scan", methods=["GET"])
@login_required
def scan():
    """Scan a ticket"""
    return render_template("scan.html")


# Validate ticket JavaScript made with the help of AI
@app.route("/validate_ticket")
def validate_ticket():
    # Obtain ticket_id from the request
    ticket_id = request.args.get("ticket_id")
    if not ticket_id:
        return jsonify({"success": False, "message": "ID de boleto faltante"})

    # Connect to the database
    db = get_db()
    ticket = db.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,)).fetchone()

    # Verify ticket existence and status
    if not ticket:
        return jsonify({"success": False, "message": "Boleto no encontrado"})
    if ticket["ticket_used"] != 0:
        return jsonify({"success": False, "message": "Este boleto ya fue usado"})

    # Marcar como usado
    db.execute("UPDATE tickets SET ticket_used = 1 WHERE ticket_id = ?", (ticket_id,))
    db.commit()

    # Return success message
    return jsonify({"success": True, "message": f"Boleto válido. Acceso permitido."})


# Consult and Edit DB,
@app.route("/consult", methods=["GET", "POST"])
@login_required
def sql_console():
    """SQL Console to consult the database and see the schema"""
    db = get_db()
    results = None
    error = None
    query = ""

    # Get list of tables in the DB
    tables = db.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """).fetchall()

    # Get schema of each table
    schema = {}
    for table in tables:
        table_name = table['name']
        cols = db.execute(f"PRAGMA table_info({table_name})").fetchall()
        schema[table_name] = cols

    if request.method == "POST":
        query = request.form.get("query", "").strip()

        # Limit to SELECT queries for security
        if not query.lower().startswith("select"):
            error = "Solo se permiten consultas SELECT por seguridad."
        elif not query:
            error = "Por favor, ingresa una consulta SQL."

        # Execute the query made with the help of AI
        else:
            try:
                cursor = db.execute(query)
                results = cursor.fetchall()
            except Exception as e:
                error = str(e)

    # Render the template
    return render_template("consult.html", results=results, error=error, query=query, schema=schema)