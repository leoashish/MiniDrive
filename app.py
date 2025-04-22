import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from file_manager import get_all_files, delete_file
from werkzeug.utils import secure_filename
import math

app = Flask(__name__)
UPLOAD_FOLDER = 'storage'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
PER_PAGE = 5

@app.route('/')
def index():
    page = int(request.args.get('page', 1))
    files = get_all_files()
    total = len(files)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    paginated_files = files[start:end]
    total_pages = math.ceil(total / PER_PAGE)
    return render_template('index.html', files=paginated_files, page=page, total_pages=total_pages)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    delete_file(filename)
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)