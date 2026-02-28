import sqlite3
import os
from flask import Flask, render_template, request, jsonify, send_file
from gtts import gTTS
import io

app = Flask(__name__)

# Language code mapping for gTTS
LANG_MAP = {
    "ar-IQ": "ar",
    "en-US": "en",
}

def init_db():
    conn = sqlite3.connect('voice_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transcripts 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  content TEXT, 
                  language TEXT,
                  audio_blob BLOB,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_data():
    """Save VTT audio and transcript to database."""
    text_content = request.form.get('text')
    language = request.form.get('lang')
    audio_file = request.files.get('audio')

    if not audio_file or not text_content:
        return jsonify({"status": "error", "message": "Missing audio or text"}), 400

    audio_bytes = audio_file.read()

    conn = sqlite3.connect('voice_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO transcripts (content, language, audio_blob) VALUES (?, ?, ?)",
              (text_content, language, audio_bytes))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Saved audio inside DB!"})

@app.route('/tts', methods=['POST'])
def text_to_speech():
    """Convert text to speech using gTTS (Google TTS library)."""
    data = request.get_json()
    text = data.get('text', '').strip()
    lang = data.get('lang', 'en-US')

    if not text:
        return jsonify({"status": "error", "message": "No text provided"}), 400

    google_lang = LANG_MAP.get(lang, 'en')

    try:
        tts = gTTS(text=text, lang=google_lang, slow=False)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return send_file(mp3_fp, mimetype="audio/mpeg", download_name="tts.mp3")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/play/<int:id>')
def play_audio(id):
    conn = sqlite3.connect('voice_data.db')
    c = conn.cursor()
    c.execute("SELECT audio_blob FROM transcripts WHERE id=?", (id,))
    data = c.fetchone()
    conn.close()

    if data:
        return send_file(
            io.BytesIO(data[0]),
            mimetype="audio/webm",
            as_attachment=False,
            download_name=f"audio_{id}.webm"
        )
    return "Audio not found", 404

@app.route('/history')
def history():
    conn = sqlite3.connect('voice_data.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM transcripts ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return render_template('history.html', rows=rows)

@app.route('/audio/<int:id>')
def get_audio(id):
    conn = sqlite3.connect('voice_data.db')
    c = conn.cursor()
    c.execute("SELECT audio_blob FROM transcripts WHERE id=?", (id,))
    row = c.fetchone()
    conn.close()

    if row and row[0]:
        return send_file(
            io.BytesIO(row[0]),
            mimetype="audio/webm",
            as_attachment=False,
            download_name=f"recording_{id}.webm"
        )
    return "Audio not found", 404

if __name__ == '__main__':
    init_db()
    print("Running on http://127.0.0.1:5000")
    app.run(debug=True)