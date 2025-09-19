# app.py
"""
Main code adapted from CS50 Finance.
"""

import os
from flask import Flask, flash, redirect, render_template, request, session, g, url_for, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, generate_qr_code
import psycopg2
import psycopg2.extras

# Configure application
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# DATABASE SETUP
DATABASE_URL = os.environ.get("DATABASE_URL")

# Fix for SQLAlchemy URL if needed (optional)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Connect to database with DictCursor
def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.DictCursor)
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# HELPER FUNCTIONS FOR QUERIES
def query_db(query, args=(), one=False):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchone() if one else cur.fetchall()
    cur.close()
    return rv

def execute_db(query, args=()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()

# AFTER REQUEST
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# ROUTES

# INDEX
@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Ingresa un nombre de usuario", 400)
        if not request.form.get("password"):
            return apology("Ingresa una contraseña", 400)

        user = query_db("SELECT * FROM admins WHERE username = %s", (request.form.get("username"),), one=True)

        if user is None or not check_password_hash(user["hash"], request.form.get("password")):
            return apology("Usuario o contraseña incorrectos", 400)

        session["user_id"] = user["admin_id"]
        return redirect("/")
    else:
        return render_template("login.html")

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ADD FAN
@app.route("/fan", methods=["GET", "POST"])
def fan():
    if request.method == "POST":
        fan_name = request.form.get("fan_name")
        phone_number = request.form.get("phone_number")
        age = request.form.get("age")
        email = request.form.get("email")

        if not fan_name:
            return apology("Ingresa el nombre del fan", 400)
        if not phone_number:
            return apology("¡Agrega el número de teléfono!", 400)
        if not age:
            return apology("¿Cuántos años tiene tu fan?", 400)

        rows = query_db("SELECT * FROM fans WHERE fan_name = %s", (fan_name,))
        if len(rows) > 0:
            return apology("¡Ese fan ya existe!", 400)

        execute_db("INSERT INTO fans (fan_name, phone_number, email, age) VALUES (%s,%s,%s,%s)",
                   (fan_name, phone_number, email, age))

        flash("¡Fan registrado exitosamente!", "success")
        return redirect("/fan")
    else:
        return render_template("fan.html")

# ADD CONCERT
@app.route("/concert", methods=["GET", "POST"])
def concert():
    if request.method == "POST":
        venue = request.form.get("venue")
        date = request.form.get("date")
        address = request.form.get("address")
        contact_name = request.form.get("contact_name")
        contact_email = request.form.get("contact_email")
        contact_phone = request.form.get("contact_phone")

        if not venue:
            return apology("Ingresa el nombre del venue", 400)
        if not date:
            return apology("¡Agrega la fecha!", 400)
        if not contact_name:
            return apology("Ingresa el nombre del contacto", 400)
        if not contact_phone:
            return apology("Ingresa el teléfono del contacto", 400)

        execute_db(
            "INSERT INTO concerts (venue, date, address, contact_name, contact_email, contact_phone) VALUES (%s,%s,%s,%s,%s,%s)",
            (venue, date, address, contact_name, contact_email, contact_phone)
        )

        return redirect("/concert")
    else:
        return render_template("concert.html")

# GENERATE TICKET
@app.route("/ticket", methods=["GET", "POST"])
@login_required
def ticket():
    if request.method == "POST":
        fan_id = request.form.get("fan_id")
        concert_id = request.form.get("concert_id")
        admin_id = session.get("user_id")
        payment = request.form.get("payment")

        if not fan_id:
            return apology("Selecciona un fan", 400)
        if not concert_id:
            return apology("Selecciona un concierto", 400)
        if not payment:
            return apology("Selecciona un metodo de pago", 400)

        execute_db("INSERT INTO tickets (fan_id, concert_id, admin_id, payment) VALUES (%s,%s,%s,%s)",
                   (fan_id, concert_id, admin_id, payment))

        ticket = query_db("SELECT ticket_id FROM tickets ORDER BY ticket_id DESC LIMIT 1", one=True)
        ticket_id = ticket["ticket_id"]

        concert = query_db("SELECT * FROM concerts WHERE concert_id = %s", (concert_id,), one=True)
        qr_path = f"static/qr_codes/ticket_{ticket_id}.png"
        generate_qr_code(str(ticket_id), concert["venue"], concert["address"], concert["date"], qr_path)
        execute_db("UPDATE tickets SET qr_code_path = %s WHERE ticket_id = %s", (qr_path, ticket_id))

        flash("¡Boleto generado exitosamente!")
        return redirect(url_for("ticket_generated", ticket_id=ticket_id))
    else:
        fans = query_db("SELECT * FROM fans")
        concerts = query_db("SELECT * FROM concerts")
        return render_template("ticket.html", fans=fans, concerts=concerts)

# TICKET GENERATED
@app.route("/ticket_generated")
@login_required
def ticket_generated():
    ticket_id = request.args.get("ticket_id")
    if not ticket_id:
        return apology("Boleto no encontrado", 404)

    ticket = query_db("SELECT * FROM tickets WHERE ticket_id = %s", (ticket_id,), one=True)
    if not ticket:
        return apology("Boleto no encontrado", 404)

    return render_template("ticket_generated.html", ticket=ticket)

# SCAN
@app.route("/scan", methods=["GET"])
@login_required
def scan():
    return render_template("scan.html")

# VALIDATE TICKET
@app.route("/validate_ticket")
def validate_ticket():
    ticket_id = request.args.get("ticket_id")
    if not ticket_id:
        return jsonify({"success": False, "message": "ID de boleto faltante"})

    ticket = query_db("SELECT * FROM tickets WHERE ticket_id = %s", (ticket_id,), one=True)

    if not ticket:
        return jsonify({"success": False, "message": "Boleto no encontrado"})
    if ticket["ticket_used"] != 0:
        return jsonify({"success": False, "message": "Este boleto ya fue usado"})

    execute_db("UPDATE tickets SET ticket_used = 1 WHERE ticket_id = %s", (ticket_id,))
    return jsonify({"success": True, "message": f"Boleto válido. Acceso permitido."})

# SQL CONSOLE
@app.route("/consult", methods=["GET", "POST"])
@login_required
def sql_console():
    """SQL Console to consult the database and see the schema"""
    db = get_db()
    results = None
    error = None
    query = ""

    # Get list of tables
    tables = db.cursor()
    tables.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables_list = [row[0] for row in tables.fetchall()]

    # Get schema for each table
    schema = {}
    for table_name in tables_list:
        cur = db.cursor()
        cur.execute(f"""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = %s
        """, (table_name,))
        schema[table_name] = cur.fetchall()

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if not query.lower().startswith("select"):
            error = "Solo se permiten consultas SELECT por seguridad."
        elif not query:
            error = "Por favor, ingresa una consulta SQL."
        else:
            try:
                cur = db.cursor()
                cur.execute(query)
                results = cur.fetchall()
            except Exception as e:
                error = str(e)

    return render_template("consult.html", results=results, error=error, query=query, schema=schema)

# MAIN
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
