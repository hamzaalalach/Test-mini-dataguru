import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import secure_filename

# To be able to recognize relative imports
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from models import setup_db, create_all, Tag, Image
from utils import allowed_file, get_elements_paginated

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)
    app.config.from_object('config.Config')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Controll-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Controll-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')

        return response

    @app.route('/images', methods=['POST'])
    def create_image():
        if 'file' not in request.files:
            abort(400)

        file = request.files['file']

        if file.filename == '':
            abort(400)

        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                filetype = filename.split(".")[-1]
                file.save(filepath)

                image = Image(filepath, filename, filetype)
                image.insert()

                return jsonify({
                    'success': True,
                    'image': image.format()

                })
            except BaseException:
                abort(422)

    @app.route('/images')
    def get_images():
        all_images = Image.query.order_by('id').all()
        page = request.args.get('page', 1, int)
        selected_images = get_elements_paginated(all_images, page)

        if len(selected_images) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'images': selected_images,
            'total_images': len(selected_images)
        })

    @app.route('/tags', methods=['POST'])
    def create_tag():
        body = request.get_json()

        if not body or not body.get('name'):
            abort(400)
        
        try:
            tag = Tag(body.get('name'))
            tag.insert()

            return jsonify({
                'success': True,
                'tag': tag.format()
            })
        except BaseException:
            abort(422)

    @app.route('/tags')
    def get_tags():
        try:
            tags = Tag.query.order_by('id').all()

            return jsonify({
                'success': True,
                'tags': [tag.format() for tag in tags],
                'total_tags': len(tags)
            })
        except BaseException:
            abort(500)

    @app.route('/images/<image_id>/tags', methods=['POST'])
    def create_image_tag(image_id):
        body = request.get_json()

        if not body or not body.get('id'):
            abort(400)

        id = body.get('id')
        image = Image.query.filter_by(id=image_id).one_or_none()

        if not image:
            abort(404)
        
        tag = Tag.query.filter_by(id=id).one_or_none()

        if not tag:
            abort(404)
        
        try:
            image.addTag(tag)

            return jsonify({
                'success': True,
                'message': "Added tag {} to image {}.".format(id, image_id)
            })
        
        except BaseException:
            abort(422)

    @app.route('/images/<image_id>/tags')
    def get_image_tags(image_id):
        try:
            image = Image.query.filter_by(id=image_id).one_or_none()

            if not image:
                abort(404)
            
            return jsonify({
                'success': True,
                'tags': image.getTags()
            })
        except BaseException:
            abort(500)

    @app.route('/tags/<tag_id>/images')
    def get_tag_images(tag_id):
        tag = Tag.query.filter_by(id=tag_id).one_or_none()
        page = request.args.get('page', 1, int)

        if not tag:
            abort(404)
        
        all_images = tag.getImages()
        selected_images = get_elements_paginated(all_images, page)
        
        return jsonify({
            'success': True,
            'images': selected_images
        })

    # Handle errors used across the app
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
