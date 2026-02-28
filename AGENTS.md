# AGENTS.md - STT Voice-to-Text Application

## Project Overview

This is a Flask-based voice-to-text web application that records audio using the Web Speech API, transcribes it, and stores both audio and text in an SQLite database.

- **Main file**: `app.py` (Flask backend)
- **Templates**: `templates/index.html` (recorder), `templates/history.html` (history view)
- **Database**: SQLite (`voice_data.db`)
- **Run command**: `python app.py` (starts on http://127.0.0.1:5000)

---

## 1. Build / Lint / Test Commands

### Running the Application
```bash
cd D:/projects/STT/v2
python app.py
```

### Dependencies
Install required packages:
```bash
pip install flask
```
(No other dependencies - uses Python standard library for SQLite, io)

### Testing
- **No formal test suite exists** - this is a simple Flask app
- To test manually: run `python app.py` and open http://127.0.0.1:5000 in browser
- Single test: Create pytest tests in a `tests/` directory if needed

### Linting (Optional - Not Configured)
```bash
pip install ruff
ruff check app.py
```

---

## 2. Code Style Guidelines

### General
- Keep files simple and readable
- This is a small single-file Flask app - avoid over-engineering

### Python Conventions (app.py)

**Imports**
- Standard library first, then third-party
- Group: stdlib → flask → blank line
```python
import sqlite3
from flask import Flask, render_template, request, jsonify, send_file
import io
```

**Functions**
- Use descriptive names: `init_db()`, `save_data()`, `play_audio()`
- Add docstrings for route handlers
- Keep functions under 50 lines

**Database**
- Always close connections (use try/finally or context managers)
- Use parameterized queries to prevent SQL injection
```python
c.execute("INSERT INTO transcripts (content, language, audio_blob) VALUES (?, ?, ?)", 
          (text_content, language, audio_bytes))
```

**Error Handling**
- Return proper HTTP status codes (200, 400, 404)
- Return JSON errors for API endpoints
```python
return jsonify({"status": "error", "message": "Missing audio or text"}), 400
return "Audio not found", 404
```

**Routes**
- Use appropriate HTTP methods (GET for views, POST for mutations)
- Use route parameters for resource IDs: `/audio/<int:id>`

### HTML/Templates Conventions

**Structure**
- Use semantic HTML5 (`<html lang="en">`, `<head>`, `<body>`)
- Keep inline styles minimal - prefer `<style>` blocks for small projects
- Use consistent indentation (2 spaces)

**JavaScript**
- Use ES6+ syntax (const/let, arrow functions)
- Use `async/await` for async operations
- Add error handling for fetch calls
```javascript
.catch(err => console.error(err));
```

**CSS**
- Use flexbox for layout
- Use CSS custom properties for colors if needed
- Keep it simple - no frameworks required

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Python functions | snake_case | `save_data()`, `get_audio()` |
| Python variables | snake_case | `text_content`, `audio_bytes` |
| HTML IDs | camelCase | `resultText`, `recordBtn` |
| CSS classes | kebab-case | `.record-btn`, `.save-btn` |

### File Organization
```
v2/
├── app.py              # Main Flask application
├── templates/
│   ├── index.html      # Main recording page
│   └── history.html    # History view
├── voice_data.db       # SQLite database (auto-created)
└── AGENTS.md           # This file
```

---

## 3. Adding New Features

### Adding a New Route
```python
@app.route('/new-route', methods=['GET', 'POST'])
def new_route():
    # Your logic here
    return jsonify({"status": "success"})
```

### Adding a Database Table
```python
def init_db():
    conn = sqlite3.connect('voice_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS new_table 
                 (id INTEGER PRIMARY KEY, 
                  name TEXT)''')
    conn.commit()
    conn.close()
```

### Adding New Templates
- Create file in `templates/` directory
- Use Jinja2 syntax: `{% for item in items %}`
- Extend existing patterns for consistency

---

## 4. Important Notes

- Database file (`voice_data.db`) is created automatically on first run
- Audio is stored as BLOB in the database (webm format)
- Uses Web Speech API for speech recognition (browser-dependent)
- No authentication/authorization - local development only
