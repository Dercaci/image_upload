from importlib.resources import path
import os
import PIL.Image

from flask import jsonify, request
from werkzeug.utils import secure_filename
from utils import allowed_file, current_time
from http.client import OK, CREATED, BAD_REQUEST, NOT_FOUND, METHOD_NOT_ALLOWED

from base import app
from app import db, Image
from constant import SMALL_IMAGE_WIDTH, SMALL_IMAGE_HEIGHT, LARGE_IMAGE_WIDTH, LARGE_IMAGE_HEIGHT


@app.route('/', methods = ['POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"status code":400, "msg": "bad request, add an image!"})
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            img_s = PIL.Image.open(f'images/standart_images/{filename}') 
            img_s.thumbnail((SMALL_IMAGE_WIDTH, SMALL_IMAGE_HEIGHT))
            img_s.save(f'images/small_images/{current_time}small{filename}')
            path_small = (f'images/small_images/{current_time}small{filename}')

            img_b = PIL.Image.open(f'images/standart_images/{filename}') 
            img_b.thumbnail((LARGE_IMAGE_WIDTH, LARGE_IMAGE_HEIGHT))
            img_b.save(f'images/large_images/{current_time}large{filename}')
            path_large = (f'images/large_images/{current_time}large{filename}')

            image = Image(big_image = path_large, small_image = path_small)
            db.session.add(image)
            db.session.commit()
           
            return jsonify(CREATED, {"msg":"created"})
        else:
            return jsonify(BAD_REQUEST, {"msg": "bad request, your image's format is wrong"})
    else:
        return jsonify(METHOD_NOT_ALLOWED, {"msg": "use POST method!"})
    

@app.route('/get_img', methods = ['GET'])
def show_image():
    id = request.args.get('id')
    if id is not None:
        path_img = Image.query.filter_by(id = id).first()
        if path_img is not None:
            return jsonify(OK, {"path_small":path_img.small_image, "path_large":path_img.big_image})
        else:
            return jsonify(NOT_FOUND, {"msg":"like image's id doesn't exist"})
    else:
        return jsonify (BAD_REQUEST, {"msg":"introduce the id"})   
    