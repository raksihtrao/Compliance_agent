import sqlite3
from datetime import datetime

class PromptDB:
    def __init__(self, db_path='Prompy.db'):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                protocol_name TEXT,
                protocol_description TEXT,
                what_to_flag TEXT,
                severity_threshold TEXT,
                output_format TEXT,
                citation_required INTEGER,
                language TEXT,
                created_at TEXT
            )
        ''')
        self.conn.commit()

    def save_prompt(self, protocol_name, protocol_description, what_to_flag, severity_threshold, output_format, citation_required, language):
        self.conn.execute('''
            INSERT INTO prompts (protocol_name, protocol_description, what_to_flag, severity_threshold, output_format, citation_required, language, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            protocol_name,
            protocol_description,
            what_to_flag,
            severity_threshold,
            output_format,
            int(citation_required),
            language,
            datetime.now().isoformat()
        ))
        self.conn.commit()

    def get_all_prompts(self):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM prompts ORDER BY created_at DESC')
        return cur.fetchall()

    def get_prompt_by_id(self, prompt_id):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM prompts WHERE id=?', (prompt_id,))
        return cur.fetchone() 