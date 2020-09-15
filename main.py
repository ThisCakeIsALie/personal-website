import os
import sys
import image_processing
from io import BytesIO
from flask import Flask, render_template, send_file, abort
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from PIL import Image

DEBUG = True

app = Flask(__name__)

app.config['FLATPAGES_AUTO_RELOAD'] = DEBUG
app.config['FLATPAGES_EXTENSION'] = '.md'

pages = FlatPages(app)
freezer = Freezer(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects/')
def projects():
    return render_template('projects.html', items=pages)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/blog/')
def blog():
    return render_template('blog.html', items=pages)

@app.route('/blog/<string:name>/')
def article(name):
    page = pages.get_or_404(name)
    return render_template('article.html', article=page)

# https://stackoverflow.com/questions/35710361/python-flask-send-file-stringio-blank-files
def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/image/<name>/<preprocessor>')
@app.route('/image/<name>')
def image(name, preprocessor=None):
    stripped_name = os.path.basename(name)
    image_path = os.path.join('images/', stripped_name)

    if not os.path.exists(image_path):
        abort(404)

    original_image = Image.open(image_path)
    processed_image = image_processing.process(preprocessor, original_image)

    return serve_pil_image(processed_image)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(debug=DEBUG, host='0.0.0.0')
