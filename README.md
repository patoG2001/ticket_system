# Anomalia ticket system
### Video DEMO: 
### Description:

In the need of developing a better system for keeping metrics and tracking the people who attend concerts and important contacts for the musical scene, I have developed the ticket system for my band **Anomalia**. Fulfilling the needs and flexibility that we have as an independent band in Mexico City. You can check our material here: https://linktr.ee/anomalia_band

The project consists of a web app connected to a database in SQLite that saves information about our fans and the concerts that we give. Then a unique QR code is generated that connects the fan to a concert. This personalized ticket is sent to the fan. This code is scanned inside the web app when people are entering the concert; a flash message appears allowing the fan to enter the concert or deny access if the ticket has been used.

## Objectives and Results
- Real-time tracking of concert access.
- Database with fan profiles for segmentation and contact.
- Metrics that allowed an expected 20% increase in attendance between events.

## Data Analysis
Once the system has gathered enough data from concerts and fan registrations, I plan to conduct exploratory data analysis to better understand the audience and optimize marketing campaigns. This analysis will include visualizations and segmentations based on factors such as age and attendance frequency, providing insights to improve fan engagement and event planning.

# How to Run the Project
1- Clone the repo.

2- Create and activate a virtual environment.

3 - Install dependencies with pip install -r requirements.txt.

4 - Run python app.py.

5 - Access at localhost:5000.
*(optional: mount web app)*

## Technologies Used
- Backend: Python, Flask.
- Database: SQLite.
- Frontend: HTML, CSS, JavaScript.
- QR Code: Generation and scanning with Python and JS libraries.

## How It Works
- Registration of fans and concerts.
- Automatic generation of a personalized QR ticket.
- Scanning at the entrance to validate access.
- Queries and reports for marketing and organization.

*Files*

**SCHEMA:**  We have 4 tables:

- Admins will allow the admins of the band to enter the web app and interact with it. Only band members have access to the web app.

- Fans will save information about our fans, with name, phone, email, and age. This is for keeping metrics and developing better marketing strategies.

- Concerts will save information about the venue name, date of the concert, address, and contact information of the person who is in charge of the place. This is not only for metrics but for keeping a database of valuable information of the people we have worked with, whom we can later contact to work again.

- Tickets will connect a fan to a concert, then the path, unique ticket_id, and whether the ticket has been used.

**init_db** Sets the connection and creates the database.

**helpers.py** Has 3 available functions:

- Login_required will allow only admins to interact with the database.

- Apology will render an apology message when errors occur.

- Generate_qr_code will create a personalized QR ticket, with the correct brand colors, font, and logos. It also includes information about the concert: address, venue, and date.

**app.py** Main program that runs the app. All routes are connected here. First, we import all necessary files and set the web app.

- "/" Our index just renders our index.html with a simple message for the admin.

- "/login" Renders the login.html form. Checks if the user and password match. Finally, it stores the session id.

- "/logout" Allows the user to exit.

- "/fan" Renders the HTML form that allows the user to register a fan. We gather the name, phone, age, and email. Finally, a unique id is saved.

- "/concert" Renders the HTML that allows the user to register a concert. We assign a unique id and gather the venue name, date of the concert, address, contact name, phone, and email.

- "/ticket" Renders the HTML form that allows the user to generate a ticket. For this, we select a fan, a concert, and the payment method that was used. First, we create the ticket with the information given; a unique ticket_id is generated. We take from the concert table the concert information, so we can print it on the ticket. Then we select a path where the ticket is going to be saved. We use the generate_qr_code function and register the path in the database. After that, a flash message is sent indicating the success of the action. Finally, we redirect to a page where the user can download the ticket.

- "/ticket_generated" The ticket HTML for downloading it is rendered.

- "/scan" Uses JavaScript to validate the ticket. The web app requests access to the device's camera and scans the QR code, rendering a success message if the ticket is valid, then marking in the database that the code has been used. The QR code contains only the ticket_id. If the user tries to scan it again, an error message will indicate that the ticket has already been used.

- "/consult" Allows the user to see the schema of the database and make SQL queries. In order to keep the database integrity, only SELECT queries are valid. Therefore, we can check contact information or view who has been the most loyal fan.

**style.css** Defines our classes, buttons, fonts, and style. This was extracted from the original band's page, so the brand identity is consistent.


**layout.html** Defines our header with all the necessary links for the web app. Defines our titles and favicons in multiple formats. The footer redirects you to the band's social media.


**admin.py** Simple python script that creates usernames and hash passwords, only accessible in the backend.

