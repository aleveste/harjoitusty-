import sqlite3
import bcrypt

class AuthManager:
    """
    AuthManager huolehtii käyttäjien rekisteröinnistä, 
    kirjautumisesta ja pelitulosten tallentamisesta tietokantaan.

    Attributes:
        db_file (str): Polku SQLite-tietokantatiedostoon.
    """
    def __init__(self, db_file="game_data.db"):
        """
        Luo uuden AuthManager-olion.

        Args:
            db_file (str): Tietokantatiedoston nimi.
        """
        self.db_file = db_file

    def create_user_table(self):
        """
        Luo taulun users jos sitä ei vielä ole.
        """
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                );
            """)

    def register_user(self, username, password):
        """
        Uuden käyttäjän rekisteröinti.

        Args:
            username (str): Käyttäjätunnus.
            password (str): Salasana.

        Returns:
            bool: True, jos rekisteröinti onnistui,
            False, jos käyttäjätunnus on jo olemassa tai syöte on virheellinen.
        """
        if not username.strip() or not password:
            return False
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                             (username, password_hash))
            return True
        except sqlite3.IntegrityError:
            return False

    def login_user(self, username, password):
        """
        Kirjaa käyttäjän sisään.

        Args:
            username (str): Käyttäjätunnus.
            password (str): Salasana.

        Returns:
            bool: True, jos kirjautuminen onnistui; muuten False.
        """
        if not username.strip() or not password:
            return False
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
            row = cur.fetchone()
            if row and bcrypt.checkpw(password.encode(), row[0].encode('utf-8')):
                return True
            return False

    def create_score_table(self):
        """
        Luo tulostaulun scores tietokantaan jos sitä ei vielä ole olemassa.
        """
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    grid_size INTEGER,
                    time_seconds INTEGER,
                    won BOOLEAN,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
            """)

    def get_user_id(self, username):
        """
        Hakee käyttäjän tietokanta-ID:n käyttäjätunnuksen perusteella.

        Args:
            username (str): Käyttäjätunnus.

        Returns:
            int | None: Käyttäjän ID, tai None jos käyttäjää ei löydy.
        """
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.execute("SELECT id FROM users WHERE username = ?", (username,))
            row = cur.fetchone()
            return row[0] if row else None

    def save_score(self, username, grid_size, time_seconds, won):
        """
        Tallentaa pelin tuloksen tietokantaan.

        Args:
            username (str): Käyttäjätunnus.
            grid_size (int): Peliruudukon koko.
            time_seconds (int): Pelin kesto sekunteina.
            won (bool): True jos peli voitettiin, False jos hävittiin.
        """
        user_id = self.get_user_id(username)
        if user_id is not None:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute("""
                    INSERT INTO scores (user_id, grid_size, time_seconds, won)
                    VALUES (?, ?, ?, ?)
                """, (user_id, grid_size, time_seconds, won))

    def get_user_scores(self, username):
        """
        Palauttaa käyttäjän viimeisimmät 5 pelitulosta.

        Args:
            username (str): Käyttäjätunnus.

        Returns:
            list: Lista pisteistä tupleina muodossa (grid_size, time_seconds, won, timestamp).
        """
        user_id = self.get_user_id(username)
        if user_id is not None:
            with sqlite3.connect(self.db_file) as conn:
                cur = conn.execute("""
                    SELECT grid_size, time_seconds, won, timestamp
                    FROM scores
                    WHERE user_id = ?
                    ORDER BY timestamp DESC
                    LIMIT 5
                """, (user_id,))
                return cur.fetchall()
        return []
