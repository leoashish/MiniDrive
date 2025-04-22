from flask import Flask, render_template, request, redirect, url_for, send_file
from io import BytesIO
from file_manager import save_file_to_db, get_all_files, get_file_by_id, delete_file
import math

app = Flask(__name__)
PER_PAGE = 5

@app.route('/')
def index():
    page = int(request.args.get('page', 1))
    files = get_all_files()
    total = len(files)
    paginated = files[(page-1)*PER_PAGE: page*PER_PAGE]
    return render_template("index.html", files=paginated, page=page, total_pages=math.ceil(total/PER_PAGE))

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        save_file_to_db(file)
    return redirect(url_for('index'))

@app.route('/download/<int:file_id>')
def download(file_id):
    record = get_file_by_id(file_id)
    if record:
        filename, file_data = record
        return send_file(BytesIO(file_data), download_name=filename, as_attachment=True)
    return "File not found", 404

@app.route('/delete/<int:file_id>', methods=['POST'])
def delete(file_id):
    delete_file(file_id)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
