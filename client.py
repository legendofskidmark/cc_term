from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import boto3
import time

app = Flask(__name__)

# Set the upload folder for file storage
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
const_bucket_name = "cloud-computing-termproject-boon"

aws_access_key_id="ASIAXD6GXUNFIQMS2YP6"
aws_secret_access_key="iO5mjCq2Zsm+EcmpgrUws8RYRZ+p7QGBa9k0E/Ga"
aws_session_token="FwoGZXIvYXdzEKD//////////wEaDDFvk/lzO/8sW8W3PSLDAeLMEFLi8jyZfxVP58I7xYx4fJCUdtPH4at146d95TkZZKVp713acor6xJyka6Y4BBFoN5AHB9WdKvMEze8dYcd+PVQYvPSq7UiVcTRL3Y1yZDnQAVErmKZkdp2ORjd589ifq/B9zpbrnJ/mJklGqYfr/NNXoPqqgMUzGVPlCnJggfrzqy3BZvoCKITdcedVeNy2OJT1/AZJXvhpnAwr/3OltWdQmU+0XqBcd3elOytganbrBFnLNs7KoucXH0qzv+fcvSjt26CrBjIti7Wuab8FvST2oVNJ3z2gCi1ewQ0O16xNNFiSE/yZofXWqoYkkvEe5dtX3edf"

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/generate", methods=['POST'])
def generate():

    files = request.files.getlist('files[]')
    current_timestamp = str(int(time.time()))
    current_timestamp = current_timestamp + "/"
    
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            local_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(local_file_path)
            s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

            s3_client.upload_file(local_file_path, const_bucket_name, current_timestamp + filename)
            os.remove(local_file_path)


    return render_template('out.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
