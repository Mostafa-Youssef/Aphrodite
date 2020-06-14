from flask import Flask, request, send_file
import os
from werkzeug.utils import secure_filename
from integrating import enhance

app = Flask(__name__)


PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['POST'])
def upload_image():

    if request.method == 'POST' and request.files['image']:

        image = request.files['image']
        img_name = secure_filename(image.filename)
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)

        image.save(saved_path)

        enhance(saved_path)

        return send_file('super.png', mimetype='image/png')
    else:
        return "Where is the image?"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
