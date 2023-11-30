from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Set the upload folder for file storage
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/generate", methods=['POST'])
def generate():

    files = request.files.getlist('files[]')

    for file in files:
        if file:
            print("boon")
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('out.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
