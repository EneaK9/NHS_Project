from flask import Blueprint, jsonify
from database.db_connection import get_db_connection
import psycopg2.extras

conditions_bp = Blueprint("conditions", __name__)

@conditions_bp.route("/api/conditions")
def get_conditions():
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM conditions_albanian")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(data)

@conditions_bp.route("/api/translated-conditions")
def get_translated_conditions():
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM condition_sections_albanian")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(data)
