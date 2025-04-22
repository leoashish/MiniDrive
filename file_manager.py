# file_manager.py

import psycopg2
from psycopg2.extras import RealDictCursor
import os

# Set your DB credentials here
DB_CONFIG = {
    'dbname': 'minidrive',
    'user': 'postgres',
    'password': 'singoo123#',
    'host': 'localhost',
    'port': 5431,
}

def connect_db():
    return psycopg2.connect(**DB_CONFIG)

def save_file_to_db(file_storage):
    file_data = file_storage.read()  # Read binary content once
    file_size = len(file_data)       # Get size in bytes
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO files (name, size, data) VALUES (%s, %s, %s)",
                (file_storage.filename, file_size, file_data)
            )

def get_all_files():
    with connect_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, name, size FROM files ORDER BY uploaded_at DESC")
            return cur.fetchall()

def get_file_by_id(file_id):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT name, data FROM files WHERE id = %s", (file_id,))
            return cur.fetchone()

def delete_file(file_id):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM files WHERE id = %s", (file_id,))
