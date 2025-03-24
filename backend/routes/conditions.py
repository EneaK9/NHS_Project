from flask import Blueprint, jsonify
from database.db_connection import get_db_connection

conditions_bp = Blueprint("conditions", __name__)

@conditions_bp.route("/conditions", methods=["GET"])
def get_conditions():
    """Fetch all conditions from the database."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM conditions_albanian")
    conditions = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return jsonify(conditions)

@conditions_bp.route("/translated-conditions", methods=["GET"])
def get_translated_conditions():
    """Fetch all translated conditions from the database."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM condition_sections_albanian")
    sections = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return jsonify(sections)
