import os
import tempfile
from pathlib import Path
from flask import Flask, render_template, request, jsonify, abort, make_response

# Determine absolute templates path relative to this file (works on Vercel and locally)
TEMPLATES_DIR = str(Path(__file__).resolve().parent.parent.joinpath('templates'))

# Create the Flask app
app = Flask(__name__, template_folder=TEMPLATES_DIR)

# Directory to store saved files (local only)
# Try to create a `saved_files/` folder next to the project root. On
# serverless platforms that mount the deployment as read-only this will
# fail; in that case fall back to a writable temp folder (e.g. /tmp).
PROJECT_SAVED = Path(__file__).resolve().parent.parent.joinpath('saved_files')
try:
    PROJECT_SAVED.mkdir(parents=True, exist_ok=True)
    SAVED_DIR = PROJECT_SAVED
except Exception as _e:
    # Fall back to the system temp directory which is writable on serverless
    tmp = Path(tempfile.gettempdir()).joinpath('modern_text_editor_saved_files')
    try:
        tmp.mkdir(parents=True, exist_ok=True)
        SAVED_DIR = tmp
    except Exception:
        # As a last resort, use the project path (may raise later on write)
        SAVED_DIR = PROJECT_SAVED

# Limits
MAX_FILENAME_LEN = 200
MAX_FILE_BYTES = 1_000_000  # 1 MB


def sanitize_filename(name: str) -> str:
    """Sanitize a user-provided filename.

    Rules:
    - Strip any path components (use only the final name).
    - Replace unsafe characters with '_'.
    - Preserve a short alphanumeric extension when present (e.g. .txt, .md, .html).
    - Otherwise fall back to adding a .txt extension.
    """
    import re
    if not name:
        return 'untitled.txt'
    base = Path(name).name
    # separate name and extension
    stem = base
    ext = ''
    if base.count('.'):
        stem, ext = base.rsplit('.', 1)
        ext = '.' + ext

    # sanitize stem and ext
    safe_stem = re.sub(r'[^A-Za-z0-9_-]', '_', stem) or 'untitled'
    # allow short alphanumeric extensions, otherwise default to .txt
    if ext and re.match(r'^\.[A-Za-z0-9]{1,8}$', ext):
        safe = safe_stem + ext
    else:
        safe = safe_stem + '.txt'
    # final length guard
    if len(safe) > MAX_FILENAME_LEN:
        safe = safe[:MAX_FILENAME_LEN]
    return safe


@app.route('/api/list_files')
def list_files():
    files = []
    for p in SAVED_DIR.iterdir():
        if not p.is_file() or p.name.startswith('.'):
            continue
        try:
            st = p.stat()
            files.append({'name': p.name, 'mtime': int(st.st_mtime), 'size': st.st_size})
        except Exception:
            continue
    # sort by mtime desc
    files.sort(key=lambda x: x.get('mtime', 0), reverse=True)
    return jsonify(files=files)


@app.route('/api/load_file')
def load_file():
    name = request.args.get('name', '')
    if not name:
        return jsonify(error='name parameter required'), 400
    safe = sanitize_filename(name)
    path = SAVED_DIR.joinpath(safe)
    # extra safety: ensure path is inside SAVED_DIR
    try:
        path.resolve().relative_to(SAVED_DIR.resolve())
    except Exception:
        return jsonify(error='invalid filename'), 400
    if not path.exists():
        return jsonify(error='file not found'), 404
    try:
        text = path.read_text(encoding='utf-8')
    except Exception as e:
        return jsonify(error='could not read file', detail=str(e)), 500
    return jsonify(name=safe, content=text)


@app.route('/api/save_file', methods=['POST'])
def save_file():
    data = request.get_json(silent=True) or {}
    name = data.get('name', '')
    content = data.get('content', '')
    if not name:
        return jsonify(error='name required'), 400
    safe = sanitize_filename(name)
    path = SAVED_DIR.joinpath(safe)
    # enforce filename length
    if len(safe) > MAX_FILENAME_LEN:
        return jsonify(error='filename too long'), 400
    # enforce size limit
    if not isinstance(content, str):
        # convert non-string content to string safely
        try:
            content = str(content)
        except Exception:
            return jsonify(error='invalid content'), 400
    if len(content.encode('utf-8')) > MAX_FILE_BYTES:
        return jsonify(error='file too large'), 413
    try:
        # ensure parent safety
        path.resolve().relative_to(SAVED_DIR.resolve())
        path.write_text(content or '', encoding='utf-8')
    except Exception as e:
        # log the error to stdout for easy debugging in server logs
        print('save_file error:', e)
        return jsonify(error='could not save file', detail=str(e)), 500
    return jsonify(ok=True, name=safe)


@app.route('/api/delete_file', methods=['POST'])
def delete_file():
    data = request.get_json(force=True)
    name = (data or {}).get('name', '')
    if not name:
        return jsonify(error='name required'), 400
    safe = sanitize_filename(name)
    path = SAVED_DIR.joinpath(safe)
    try:
        if not path.exists():
            return jsonify(error='file not found'), 404
        path.resolve().relative_to(SAVED_DIR.resolve())
        path.unlink()
    except Exception as e:
        print('delete_file error:', e)
        return jsonify(error='could not delete file', detail=str(e)), 500
    return jsonify(ok=True)



@app.route('/')
def index():
    # Render a simple Jinja template
    return render_template('index.html', title='Modern Text Editor', message='Hello from Jhashank!')


if __name__ == '__main__':
    # Local development server
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
