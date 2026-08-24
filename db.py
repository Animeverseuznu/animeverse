import sqlite3
from datetime import datetime, timedelta

DB = "anime.db"


def connect():
    return sqlite3.connect(DB)


def init_db():
    con = connect()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        vip_until TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS anime (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE,
        title TEXT,
        description TEXT,
        genre TEXT,
        poster TEXT,
        is_vip INTEGER DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS episodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        anime_id INTEGER,
        episode INTEGER,
        file_id TEXT,
        UNIQUE(anime_id, episode)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS favorites (
        user_id INTEGER,
        anime_id INTEGER,
        UNIQUE(user_id, anime_id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        user_id INTEGER,
        anime_id INTEGER,
        episode INTEGER,
        updated_at TEXT,
        UNIQUE(user_id, anime_id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        package TEXT,
        days INTEGER,
        amount INTEGER,
        status TEXT DEFAULT 'pending',
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS referrals (
        user_id INTEGER PRIMARY KEY,
        invited_by INTEGER
    )
    """)

    con.commit()
    con.close()


def create_user(user_id, username=None):
    con = connect()
    cur = con.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO users
    (user_id, username)
    VALUES (?, ?)
    """, (user_id, username))

    con.commit()
    con.close()


def get_user(user_id):
    con = connect()
    cur = con.cursor()

    cur.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )

    result = cur.fetchone()
    con.close()

    return result


def add_xp(user_id, amount):
    con = connect()
    cur = con.cursor()

    cur.execute("""
    UPDATE users
    SET xp = xp + ?
    WHERE user_id=?
    """, (amount, user_id))

    cur.execute(
        "SELECT xp FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cur.fetchone()

    if row:
        xp = row[0]
        level = xp // 100 + 1

        cur.execute("""
        UPDATE users
        SET level=?
        WHERE user_id=?
        """, (level, user_id))

    con.commit()
    con.close()


def is_vip(user_id):
    con = connect()
    cur = con.cursor()

    cur.execute(
        "SELECT vip_until FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cur.fetchone()
    con.close()

    if not row or not row[0]:
        return False

    try:
        return datetime.fromisoformat(row[0]) > datetime.now()
    except Exception:
        return False


def add_vip_days(user_id, days):
    con = connect()
    cur = con.cursor()

    cur.execute(
        "SELECT vip_until FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cur.fetchone()

    now = datetime.now()

    if row and row[0]:
        try:
            current = datetime.fromisoformat(row[0])
        except Exception:
            current = now
    else:
        current = now

    if current < now:
        current = now

    until = current + timedelta(days=days)

    cur.execute("""
    UPDATE users
    SET vip_until=?
    WHERE user_id=?
    """, (until.isoformat(), user_id))

    con.commit()
    con.close()

    return until


def add_anime(code, title, description="", genre="", poster="", is_vip=0):
    con = connect()
    cur = con.cursor()

    cur.execute("""
    INSERT INTO anime
    (code,title,description,genre,poster,is_vip)
    VALUES (?,?,?,?,?,?)
    """, (
        code,
        title,
        description,
        genre,
        poster,
        is_vip
    ))

    anime_id = cur.lastrowid

    con.commit()
    con.close()

    return anime_id


def get_anime(code):
    con = connect()
    cur = con.cursor()

    cur.execute("""
    SELECT id,code,title,description,genre,poster,is_vip
    FROM anime
    WHERE code=?
    """, (code,))

    row = cur.fetchone()
    con.close()

    return row


def add_episode(anime_id, episode, file_id):
    con = connect()
    cur = con.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO episodes
    (anime_id,episode,file_id)
    VALUES (?,?,?)
    """, (
        anime_id,
        episode,
        file_id
    ))

    con.commit()
    con.close()


def get_episode(anime_id, episode):
    con = connect()
    cur = con.cursor()

    cur.execute("""
    SELECT file_id
    FROM episodes
    WHERE anime_id=? AND episode=?
    """, (
        anime_id,
        episode
    ))

    row = cur.fetchone()
    con.close()

    return row[0] if row else None


def save_history(user_id, anime_id, episode):
    con = connect()
    cur = con.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO history
    (user_id,anime_id,episode,updated_at)
    VALUES (?,?,?,?)
    """, (
        user_id,
        anime_id,
        episode,
        datetime.now().isoformat()
    ))

    con.commit()
    con.close()


def create_payment(user_id, package, days, amount):
    con = connect()
    cur = con.cursor()

    cur.execute("""
    INSERT INTO payments
    (user_id,package,days,amount,status,created_at)
    VALUES (?,?,?,?,?,?)
    """, (
        user_id,
        package,
        days,
        amount,
        "pending",
        datetime.now().isoformat()
    ))

    payment_id = cur.lastrowid

    con.commit()
    con.close()

    return payment_id


def get_payment(payment_id):
    con = connect()
    cur = con.cursor()

    cur.execute("""
    SELECT id,user_id,package,days,amount,status
    FROM payments
    WHERE id=?
    """, (payment_id,))

    row = cur.fetchone()
    con.close()

    return row


def set_payment_status(payment_id, status):
    con = connect()
    cur = con.cursor()

    cur.execute("""
    UPDATE payments
    SET status=?
    WHERE id=?
    """, (status, payment_id))

    con.commit()
    con.close()


def get_pending_payment(user_id):
    con = connect()
    cur = con.cursor()

    cur.execute("""
    SELECT id,package,days,amount
    FROM payments
    WHERE user_id=? AND status='pending'
    ORDER BY id DESC
    LIMIT 1
    """, (user_id,))

    row = cur.fetchone()
    con.close()

    return row

def get_vip_until(user_id):
    con = connect()
    cur = con.cursor()

    cur.execute(
        "SELECT vip_until FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cur.fetchone()
    con.close()

    if row and row[0]:
        return row[0]

    return "Noma'lum"

