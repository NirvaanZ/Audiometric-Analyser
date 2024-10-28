from flask import Flask, render_template, jsonify, url_for
import sqlite3
import os

from utils.array_shape import plot_and_save_responses_by_age

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('../database/auth.db')                       # Replace with your actual database
    conn.row_factory = sqlite3.Row                                     # To return rows as dictionaries
    return conn

# Route to perform analysis and return the image path
@app.route('/perform_analysis/<int:row_id>')
def perform_analysis(row_id):
    # Here you would implement the actual analysis logic based on row_id
    # This is a placeholder that returns a static image for all rows
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM analysis_results WHERE id =?', (row_id,)).fetchall()    # Fetch multiple entries
    conn.close()
    
    plot_and_save_responses_by_age(30, data['response'])

    analysis_result_image = url_for('static', filename='images/result_img.png')

    # Return the image path as a JSON response
    return jsonify({'image_path': analysis_result_image})

@app.route('/')
def index():
    user_id = 3 # to receive all the responses from past audiometric tests
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM analysis_results WHERE user_id =?', (user_id,)).fetchall()    # Fetch multiple entries
    conn.close()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
