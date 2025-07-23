-- Drop existing tables
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS fans;
DROP TABLE IF EXISTS concerts;
DROP TABLE IF EXISTS tickets;

-- Table for admins
CREATE TABLE admins(
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    hash TEXT NOT NULL
);

-- Table for fans
CREATE TABLE fans(
    fan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fan_name TEXT NOT NULL,
    phone_number TEXT,
    email TEXT,
    age INTEGER
);

-- Table for concerts
CREATE TABLE concerts(
    concert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    venue TEXT NOT NULL,
    date TEXT NOT NULL,
    address TEXT,
    contact_name TEXT NOT NULL,
    contact_email TEXT,
    contact_phone TEXT NOT NULL,
    attendees INTEGER DEFAULT 0
);

-- Table for tickets, QR codes
CREATE TABLE tickets(
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    concert_id INTEGER NOT NULL,
    fan_id INTEGER NOT NULL,
    admin_id INTEGER,
    ticket_used INTEGER DEFAULT 0,
    qr_code_path TEXT,
    payment TEXT,
    FOREIGN KEY (concert_id) REFERENCES concerts(concert_id),
    FOREIGN KEY (fan_id) REFERENCES fans(fan_id),
    FOREIGN KEY (admin_id) REFERENCES admins(admin_id)
);