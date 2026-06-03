import sqlite3
import os
class MetadataDB:
    def __init__(self):
        os.makedirs(r"f:\rag_system\data\metadata", exist_ok=True)
        self.connection = sqlite3.connect(r"f:\rag_system\data\metadata\metadata.db")
        self._create_table()
        
    def _create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS metadata(
            chunk_id TEXT,
            source TEXT,
            title TEXT,
            content TEXT
        )
        """)
        self.connection.commit()
        cursor.close()

    def insert(self, metadata):
        cursor = self.connection.cursor()
        cursor.execute("""
        INSERT INTO metadata VALUES (?, ?, ?, ?)
        """, (
            metadata["chunk_id"],
            metadata["source"],
            metadata["title"],
            metadata["content"]
        ))
        self.connection.commit()
        cursor.close()

    def fetch(self, chunk_id):
        cursor = self.connection.cursor()
        cursor.execute("""
        SELECT * FROM metadata WHERE chunk_id=?
        """, (chunk_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def close(self):
        self.connection.close()
        