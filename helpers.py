# Helper file for functions on the web app
# Inspired by CS50 finance helpers.py

# Important Libraries
from flask import redirect, render_template, session
from functools import wraps
import qrcode
from PIL import Image, ImageDraw, ImageFont

# Login required function
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function




# Apology for errors, adapted from Finance CS50 
def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", top=code, bottom=message), code




# Generate QR code function, first draft made with the help of AI
# I personalized QR code with ticket details. Appropiate sizes and fonts to fit the honor the brand.
def generate_qr_code(ticket_id, venue, address, date, path):
    # Select QR cpde and size
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,)
    qr.add_data(ticket_id)
    qr.make(fit=True)

    # Make the QR code image
    img = qr.make_image(fill_color="black", back_color="#FFFFED").convert("RGB")
    
    # Load logo
    logo = Image.open("static/images/logo.png")
    logo.thumbnail((130, 130))
    
    # Select Image size
    width, height = img.size
    total_height = height + 300
    total_width = width + 100
    
    # Font sizes
    title_font = ImageFont.truetype("static/CoveredByYourGrace-Regular.ttf", 50)
    text_font = ImageFont.truetype("static/CoveredByYourGrace-Regular.ttf", 25)
    
    # Create background image
    new_img = Image.new("RGB", (total_width, total_height), "black")
    
    # Paste QR code
    new_img.paste(img, (50, 195))
    
    # Set draw for text
    draw = ImageDraw.Draw(new_img)

    # Set title and text
    title= f"ANOMALÍA"
    title_width = draw.textlength(title, font=title_font)
    text = f"\nLugar: {venue}\nDirección: {address}\nFecha: {date}"

    # Draw title and text
    draw.text((((total_width-title_width)//2), 30), title, fill="#F4D03F", font=title_font)
    draw.text((25, 70), text, fill="#F4D03F", font=text_font)
    
    # Paste logo at center bottom
    new_img.paste(logo, (((total_width - logo.width)//2), 425), logo)
    
    # Save the new image with the QR code and details
    new_img.save(path)