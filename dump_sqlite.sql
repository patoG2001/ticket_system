--Checking for existing tables and dropping them if they exist
DROP TABLE IF EXISTS tickets CASCADE;
DROP TABLE IF EXISTS concerts CASCADE;
DROP TABLE IF EXISTS fans CASCADE;
DROP TABLE IF EXISTS admins CASCADE;





-- Tabla admins
CREATE TABLE admins (
    admin_id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    hash TEXT NOT NULL
);

INSERT INTO admins VALUES
(1,'anito','scrypt:32768:8:1$PmNnlvEORUAiZv7G$b9597ed1d1d5790f7dd9975b68775d3fd3746c1d3754829837aacedac585a899f1618861632bdd68146e7022183d7cea40b12320008220755ad9a313458ce276'),
(2,'patobatako','scrypt:32768:8:1$rQe7o3hruiz9yk5S$fef549e98ab617108c52482fceafc40eadd2409e5402187e60a794d052c13162c9ca6a55418baecb186ce875ca3cec8f06c4ee6a1ffa0f34c075a0c09eeedbcb'),
(3,'B4seck','scrypt:32768:8:1$KOqBRxZ07uYd4qYs$f04868e301269a7dabe84329d6e5d71add408eaa6b87a6b7f281da8b62fbe489d76de9af3d00620bc649deddd8190b4f0438415a7ab35dd5cd262db11f5d4c0e'),
(4,'jt6453671','scrypt:32768:8:1$WqR5MQ1skmJYjtcC$00bbc35b6a5f86dc962c9580f87befec4d2cab165aef1c97171733e8315d022d7e10f3e303c016bc84e4336b6122bcce19454ad0684e4dc7e76b068f5877be19'),
(5,'Abiriuux','scrypt:32768:8:1$oqZpBntdJvjEhDxr$4e0136c8ea793f0178939e7e1fbd0fe455034ce0519045f474eb8ca1e86b408b43cd4c4258f3cdd1f0e1875d4696798b852aceb9b6ee86e52131ab54e20727a3'),
(6,'Angelcruz25','scrypt:32768:8:1$TPuDFohOX39PihUY$0560cc88307ffe3773d2423c2763237ca1f468ef1794392b2bda146a4a7cc83f37bd9511b290b7b84e3cc953bd102721856e4283923d94081220dd40bc8d1b34'),
(7,'DiegoVelzer','scrypt:32768:8:1$m1d1Uotlmg5pEvtn$d95ae506aa90990f06aa7c430b427a647ee09c024eb2d4b82084eefe3131c8069eaab3bda8efe7b672331de063a10496b433c090b2eb2fe3d19037703cb1be4a');


-- Tabla fans
CREATE TABLE fans (
    fan_id SERIAL PRIMARY KEY,
    fan_name TEXT NOT NULL,
    phone_number TEXT,
    email TEXT,
    age INTEGER
);

-- Tabla concerts
CREATE TABLE concerts (
    concert_id SERIAL PRIMARY KEY,
    venue TEXT NOT NULL,
    date TEXT NOT NULL,
    address TEXT,
    contact_name TEXT NOT NULL,
    contact_email TEXT,
    contact_phone TEXT NOT NULL,
    attendees INTEGER DEFAULT 0
);

-- Tabla tickets
CREATE TABLE tickets (
    ticket_id SERIAL PRIMARY KEY,
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
