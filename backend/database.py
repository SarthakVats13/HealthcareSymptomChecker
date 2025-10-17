import sqlite3
from datetime import datetime
from typing import Optional, List
import json
import os

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), "symptom_checker.db")

def init_database():
    """Initialize the SQLite database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create queries table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptoms TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            conditions TEXT NOT NULL,
            recommendations TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def save_query(
    symptoms: str,
    age: Optional[int],
    gender: Optional[str],
    conditions: List[str],
    recommendations: List[str]
) -> int:
    """
    Save a symptom query to the database.
    
    Args:
        symptoms: User's symptom description
        age: Patient age
        gender: Patient gender
        conditions: List of possible conditions
        recommendations: List of recommendations
    
    Returns:
        int: The ID of the inserted query
    """
    try:
        # Initialize DB if it doesn't exist
        if not os.path.exists(DB_PATH):
            init_database()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Convert lists to JSON strings for storage
        conditions_json = json.dumps(conditions)
        recommendations_json = json.dumps(recommendations)
        
        cursor.execute("""
            INSERT INTO queries (symptoms, age, gender, conditions, recommendations)
            VALUES (?, ?, ?, ?, ?)
        """, (symptoms, age, gender, conditions_json, recommendations_json))
        
        query_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return query_id
    
    except Exception as e:
        print(f"Database save error: {e}")
        return None

def get_recent_queries(limit: int = 10) -> List[dict]:
    """
    Retrieve recent queries from the database.
    
    Args:
        limit: Maximum number of queries to retrieve
    
    Returns:
        List of query dictionaries
    """
    try:
        # Initialize DB if it doesn't exist
        if not os.path.exists(DB_PATH):
            init_database()
            return []
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, symptoms, age, gender, conditions, recommendations, timestamp
            FROM queries
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        queries = []
        for row in rows:
            queries.append({
                "id": row["id"],
                "symptoms": row["symptoms"],
                "age": row["age"],
                "gender": row["gender"],
                "conditions": json.loads(row["conditions"]),
                "recommendations": json.loads(row["recommendations"]),
                "timestamp": row["timestamp"]
            })
        
        return queries
    
    except Exception as e:
        print(f"Database retrieval error: {e}")
        return []

def get_query_by_id(query_id: int) -> Optional[dict]:
    """
    Retrieve a specific query by ID.
    
    Args:
        query_id: The query ID to retrieve
    
    Returns:
        Query dictionary or None if not found
    """
    try:
        if not os.path.exists(DB_PATH):
            return None
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, symptoms, age, gender, conditions, recommendations, timestamp
            FROM queries
            WHERE id = ?
        """, (query_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row["id"],
                "symptoms": row["symptoms"],
                "age": row["age"],
                "gender": row["gender"],
                "conditions": json.loads(row["conditions"]),
                "recommendations": json.loads(row["recommendations"]),
                "timestamp": row["timestamp"]
            }
        return None
    
    except Exception as e:
        print(f"Database retrieval error: {e}")
        return None

# Initialize database on module import
init_database()