"""
Module: database/table_manager.py

This module provides a class `Table` that manages PostgreSQL database operations
for a task and notes manager application. It handles table creation and basic
CRUD operations for users, tasks, and notes.

Author: [Your Name]
Created: 2025-05-01
"""

import psycopg2
from datetime import datetime


class Table:
    """
    A class to manage PostgreSQL connections and operations related to users,
    tasks, and notes.

    Attributes:
        dbname (str): Name of the database.
        user (str): Username for the database.
        password (str): Password for the database.
        host (str): Host address of the database.
        port (str): Port number for the database.
    """

    def __init__(self, dbname="Users", user="postgres", password="postgres", host="localhost", port="5432"):
        """
        Initializes the Table class with database connection parameters.
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def create_table(self):
        """
        Creates 'users', 'tasks', and 'notes' tables in the database if they do not exist.
        """
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            cur = conn.cursor()

            # Users table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(120) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(120) NOT NULL UNIQUE
                );
            """)

            # Tasks table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    due_date DATE,
                    category VARCHAR(100),
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed BOOLEAN DEFAULT FALSE
                );
            """)

            # Notes table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    category VARCHAR(100),
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            conn.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def add_user(self, username: str, email: str, password: str) -> None:
        """
        Adds a new user to the users table.

        Args:
            username (str): The username of the new user.
            email (str): The email address of the user.
            password (str): The hashed password of the user.
        """
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            cur = conn.cursor()

            cur.execute("SELECT 1 FROM users WHERE username = %s;", (username,))
            if cur.fetchone():
                print(f"User with username {username} already exists.")
                return

            cur.execute("""
                INSERT INTO users (username, email, password)
                VALUES (%s, %s, %s);
            """, (username, email, password))

            conn.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def add_task(self, title: str, description: str, due_date: str, category: str, user_id: int) -> None:
        """
        Adds a task for a specific user.

        Args:
            title (str): Title of the task.
            description (str): Description of the task.
            due_date (str): Due date in YYYY-MM-DD format.
            category (str): Category of the task.
            user_id (int): ID of the user to assign the task to.
        """
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            cur = conn.cursor()
            current_time = datetime.now()

            cur.execute("""
                INSERT INTO tasks (title, description, due_date, category, user_id, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (title, description, due_date, category, user_id, current_time, current_time))

            conn.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def add_note(self, title: str, content: str, category: str, user_id: int) -> None:
        """
        Adds a note for a specific user.

        Args:
            title (str): Title of the note.
            content (str): Content of the note.
            category (str): Category of the note.
            user_id (int): ID of the user to assign the note to.
        """
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            cur = conn.cursor()
            current_time = datetime.now()

            cur.execute("""
                INSERT INTO notes (title, content, category, user_id, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (title, content, category, user_id, current_time, current_time))

            conn.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def update_task(self, task_id: int, title=None, description=None, due_date=None, category=None, completed=None) -> None:
        """
        Updates an existing task.

        Args:
            task_id (int): ID of the task to update.
            title (str, optional): New title.
            description (str, optional): New description.
            due_date (str, optional): New due date.
            category (str, optional): New category.
            completed (bool, optional): Completion status.
        """
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            cur = conn.cursor()
            current_time = datetime.now()

            cur.execute("""
                UPDATE tasks
                SET title = %s, description = %s, due_date = %s, category = %s, completed = %s, updated_at = %s
                WHERE id = %s;
            """, (title, description, due_date, category, completed, current_time, task_id))

            conn.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def update_note(self, note_id: int, title=None, content=None, category=None) -> None:
        """
        Updates an existing note.

        Args:
            note_id (int): ID of the note to update.
            title (str, optional): New title.
            content (str, optional): New content.
            category (str, optional): New category.
        """
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            cur = conn.cursor()
            current_time = datetime.now()

            cur.execute("""
                UPDATE notes
                SET title = %s, content = %s, category = %s, updated_at = %s
                WHERE id = %s;
            """, (title, content, category, current_time, note_id))

            conn.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
