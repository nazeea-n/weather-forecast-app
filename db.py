"""MySQL storage for search history. If MySQL is unavailable, the app keeps working."""
import pymysql
import config

_ready = False


def _connect(with_db=True):
    return pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME if with_db else None,
        connect_timeout=3,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def ensure_db():
    """Create the database and table the first time. Returns True if MySQL is usable."""
    global _ready
    if _ready:
        return True
    try:
        conn = _connect(with_db=False)
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{config.DB_NAME}`")
        conn.close()

        conn = _connect()
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS searches (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    city VARCHAR(100) NOT NULL,
                    country VARCHAR(100),
                    temperature FLOAT,
                    description VARCHAR(100),
                    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        conn.close()
        _ready = True
        return True
    except Exception as e:
        print("MySQL not available:", e)
        return False


def save_search(city, country, temperature, description):
    if not ensure_db():
        return False
    try:
        conn = _connect()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO searches (city, country, temperature, description) VALUES (%s, %s, %s, %s)",
                (city, country, temperature, description),
            )
        conn.close()
        return True
    except Exception as e:
        print("Could not save search:", e)
        return False


def get_history(limit=10):
    """Return the latest searches, or None if MySQL is not available."""
    if not ensure_db():
        return None
    try:
        conn = _connect()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT city, country, temperature, description, searched_at "
                "FROM searches ORDER BY id DESC LIMIT %s", (limit,))
            rows = cur.fetchall()
        conn.close()
        for r in rows:
            r["searched_at"] = str(r["searched_at"])
        return rows
    except Exception as e:
        print("Could not read history:", e)
        return None
