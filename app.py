# app.py (part of the code)

import ast
import datetime
import json
import sqlite3

from datetime import datetime as dt

# Ensure the database has the necessary column

DB_Path = './machine_learning/database/auth.db'

def init_db():
    conn = sqlite3.connect(DB_Path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT NOT NULL,        -- Adding first name
        last_name TEXT NOT NULL,         -- Adding last name
        gender TEXT NOT NULL,            -- Adding gender
        mobile_number TEXT NOT NULL,     -- Adding mobile number
        role TEXT NOT NULL,              -- Adding role Doctor or patient
        dob DATE NOT NULL                -- Adding Date of Birth for future analysis
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS analysis_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,                               -- user id from recorded session of the user
        timestamp DATETIME NOT NULL,                   -- Adding date time to identify date and time of test performed
        response TEXT NOT NULL,                        -- Adding results
        pred_age INTEGER,                              -- Adding predicted age
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    conn.commit()
    conn.close()

init_db()


# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from pydub.generators import Sine
from pydub import AudioSegment
import pygame
import os
import time


from utils.age_calculator import calculate_age
from utils.array_shape import transform_list, plot_and_save_responses_by_age
from utils.machine_learning import predict_age


app = Flask(__name__)
app.secret_key = 'your_secret_key'
pygame.mixer.init()

frequencies = list(range(20, 51, 10)) + list(range(12000, 18001, 500))  # made changes just for app testing
decibels = list(range(-45, -34, 5))                                     # Decibels from -45dB to -35dB, step 5dB

# To store user responses
user_responses = []

def get_db_connection():
    conn = sqlite3.connect(DB_Path)
    conn.row_factory = sqlite3.Row
    return conn

def is_file_in_use():
    file_path = "static/sound.wav"
    """Check if the file is currently in use by another process."""
    try:
        # Try opening the file in exclusive mode
        with open(file_path, 'a') as file:
            file.close()
            # If the file opens successfully, it is not being used by another process
            return False
    except IOError:
        # If an IOError occurs, it means the file is in use
        return True

# Function to generate sound
def generate_sound(freq, db):
    sine_wave = Sine(freq).to_audio_segment(duration=2000)  # 2-second sound
    sine_wave = sine_wave - abs(db)  # Adjust volume (in dB)

    # Ensure the directory exists
    if not os.path.exists("static"):
        os.makedirs("static")

    while True: # wait untill the resource is being free.
        if (is_file_in_use() == False):
            print("Continue with further exicution")
            break
        else:
            print(" Resource is utilised wait to get it free")

    # If the file already exists, remove it before creating a new one
    sound_file = "static/sound.wav"
    if os.path.exists(sound_file):
        try:
            os.remove(sound_file)
        except Exception as e:
            print(f"Error removing file: {e}")
            return

    # Export the sound to a file
    sine_wave.export(sound_file, format="wav")

# Function to play sound using pygame
def play_sound():
    # Initialize pygame for sound playback
    # time.sleep(0.15)
    pygame.mixer.init()
    while True: # wait untill the resource is being free.
        if (is_file_in_use() == False):
            # print("Continue with further exicution")
            break
        else:
            print(" Resource is utilised wait to get it free")

    if os.path.exists("static/sound.wav"):
        try:
            pygame.mixer.music.load("static/sound.wav")
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)  # Wait until the sound is done playing
            
            # Stop the mixer after playing the sound to free the file
            pygame.mixer.music.stop()
            pygame.mixer.quit()  # Quits pygame and frees resources

        except Exception as e:
            print(f"Error playing sound: {e}")
    else:
        print("Sound file not found!")

# Route to handle response submission
@app.route('/submit_response', methods=['POST'])
def submit_response():
    data = request.get_json()
    dob = data.get('dob')
    responses = data.get('responses')
    status = data.get('status')

    # Calculate age
    birth_date = datetime.strptime(dob, '%Y-%m-%d')
    age = (datetime.now() - birth_date).days // 365

    # Store responses in database (or for now, just print them)
    print(f"User Age: {age}")
    print(f"Test Status: {status}")
    print("User Responses:", responses)

    # Here, you'd add code to store the responses in a database, including the timestamp

    # Example response
    return jsonify({"message": "Response recorded!", "status": status})

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to start sound tests
@app.route('/start_sound_test', methods=['POST'])
def start_sound_test():
    global freq_idx, db_idx
    freq_idx = 0
    db_idx = 0
    user_responses.clear()  # Clear previous responses

    # Play the first sound
    return play_next_sound()

# Function to handle playing the next sound
def play_next_sound():
    global freq_idx, db_idx

    if freq_idx < len(frequencies):
        # Get current frequency and decibel value
        current_freq = frequencies[freq_idx]
        current_db = decibels[db_idx]

        # Generate and play sound
        generate_sound(current_freq, current_db)
        play_sound()

        return jsonify({
            "message": "Playing sound",
            "frequency": current_freq,
            "decibel": current_db
        }), 200
    else:
        # Test completed
        print("Test Completed\n",user_responses)
        return jsonify({
            "message": "Test completed"
        }), 200

# Endpoint to record user response and move to the next sound
@app.route('/user_response', methods=['POST'])
def user_response():
    global freq_idx, db_idx

    # Record the user's response
    response = request.json.get('response')
    try:
        user_responses.append({
            "frequency": frequencies[freq_idx],
            "decibel": decibels[db_idx],
            "response": response
        })
    except:
        flash("Your test has been completed.")

    # Move to the next decibel value
    db_idx += 1
    if db_idx >= len(decibels):
        db_idx = 0
        freq_idx += 1

    # Play the next sound or complete the test
    return play_next_sound()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob'] 
        mobile_number = request.form['mobile_number']
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        gender = request.form['gender']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password, first_name, last_name, gender, mobile_number, role, dob) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',(username, email, password, first_name, last_name, gender, mobile_number, role, dob))
            conn.commit()
        except sqlite3.IntegrityError:
            flash('Username or email already exists')
            return redirect(url_for('register'))
        finally:
            conn.close()

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')


# Route to perform analysis and return the image path
@app.route('/perform_analysis/<int:row_id>')
def perform_analysis(row_id):
    # Here you would implement the actual analysis logic based on row_id
    # This is a placeholder that returns a static image for all rows
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM analysis_results WHERE id =?', (row_id,)).fetchone()    # Fetch multiple entries
    conn.close()

    # print(data['response'])

    # Convert the string to a Python list safely
    try:
        responses = ast.literal_eval(data['response'])
        print(responses)
    except (ValueError, SyntaxError) as e:
        print(f"Error parsing data: {e}")

    # print(responses)
    plot_and_save_responses_by_age(int(data['pred_age']), responses)

    analysis_result_image = url_for('static', filename='./imgs/result_img.png')

    # Return the image path as a JSON response
    return jsonify({'image_path': analysis_result_image})

@app.route('/dashboard')
def dashboard():
    user_id = session['user_id']
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM analysis_results WHERE user_id =?', (user_id,)).fetchall()    # Fetch multiple entries
    conn.close()
    return render_template('dashboard.html', data=data)

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        # Fetch the logged-in user's data
        user_id = session['user_id']  # Assuming you store user_id in session after login
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()

        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('change_password'))
        
        # Verify the current password
        if not check_password_hash(user['password'], current_password):
            flash('Incorrect current password.', 'error')
            return redirect(url_for('change_password'))

        # Check if new password and confirm password match
        if new_password != confirm_password:
            flash('New password and confirm password do not match.', 'error')
            return redirect(url_for('change_password'))

        # Hash the new password and update it in the database
        hashed_password = generate_password_hash(new_password)
        conn = get_db_connection()
        conn.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, user_id))
        conn.commit()
        conn.close()

        flash('Password updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('change_password.html')

@app.route('/audiometric_test')
def audiometric_test():
    return render_template('audiometric_test.html')

@app.route('/recognition_test') # this needs to develop and second part
def recognition_test():
    return render_template('recognition_test.html')


@app.route('/analyze', methods=['POST']) # this will perform machine learning analysis
def analyze():
    if 'user_id' not in session:
        flash('You need to log in first.')
        return redirect(url_for('login'))
    else:
        # Current timestamp
        timestamp = dt.now().isoformat() 

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
        conn.close()

        gender = session['gender']
        if gender == "Male":
            sent_gen = 1
        else:
            sent_gen = 0

        current_age = calculate_age(user['dob'])
        array = transform_list(sent_gen, current_age, user_responses)
        pred_age = predict_age(array)

        Auditory_health = "None"

        results = pred_age - array[1]

        if results > 0:
            Auditory_health = "Consider Consultation with Doctor !"
        elif results < 0:
            Auditory_health = "Awesome, Your hearing age is younger than your actual age!"
        else:
            Auditory_health = "Your Audiometric Health is Awesome!"

        # print("Predicted Age:", pred_age)
        # Save the results in database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO analysis_results (user_id, timestamp, response, pred_age)
                VALUES (?, ?, ?, ?)
                ''',(session['user_id'], timestamp, str(user_responses), pred_age))
        conn.commit()
        conn.close()

        # need to add machine learning for showing results.
        analysis_result = "As per analysis your Hearing age is :"+ str(pred_age) 

    return render_template('analyze.html', result=analysis_result, health= Auditory_health)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['first_name'] = user['first_name'][0].upper()+user['first_name'][1:]
            session['last_name'] = user['last_name'][0].upper()+user['last_name'][1:]
            session['gender'] = user['gender']
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch user by email
        cursor.execute('SELECT * FROM users WHERE email = ? AND username = ?', (email, username))
        user = cursor.fetchone()

        if user:
            # If user exists, update their password to 'Sunday@123'
            default_password = 'Sunday@123'
            hashed_password = generate_password_hash(default_password)  # Hash the default password for security
            
            # Update the password in the database
            cursor.execute('UPDATE users SET password = ? WHERE email = ?', (hashed_password, email))
            conn.commit()

            # Notify the user about the reset
            flash(f'Password has been reset to "{default_password}". Please change it after logging in.')

            # Optionally, you can redirect the user to the login page
            return redirect(url_for('login'))
        else:
            # If email not found, flash an error message
            flash('Email not found.')

        conn.close()

    return render_template('forgot_password.html')

@app.route('/analysis')
def analysis():
    if 'user_id' not in session:
        flash('You need to log in first.')
        return redirect(url_for('login'))
    return render_template('analysis.html')

@app.route('/save_analysis', methods=['POST'])
def save_analysis():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    heard_sound = data.get('heard')
    frequency = data.get('frequency')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO analysis_results (user_id, heard_sound, frequency)
        VALUES (?, ?, ?)
    ''', (session['user_id'], heard_sound, frequency))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
