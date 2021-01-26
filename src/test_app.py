import unittest
import json
import os
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Tag, Image


def get_last_element_id(element):
    elements = element.query.order_by('id').all()

    return str(elements[-1].format()['id'])


class MonkTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "monk_test"
        self.database_path = "postgres://postgres:0000@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.new_tag = {
            'name': 'Cat'
        }

    def tearDown(self):
        pass

    def test_get_images_200(self):
        res = self.client().get('/images')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['images'])
        self.assertEqual(data['total_images'], 1)
        self.assertTrue(data['success'])

    def test_get_images_404(self):
        res = self.client().get('/images?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
    
    def test_create_tag_200(self):
        res = self.client().post('/tags', json=self.new_tag);
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['tag'])
        self.assertEqual(data['tag']['name'], self.new_tag['name'])
    
    def test_add_tag_image_200(self):
        latest_image = get_last_element_id(Image)
        latest_tag = get_last_element_id(Tag)
        res = self.client().post('/images/' + latest_image + '/tags', json={'id': latest_tag})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], "Added tag {} to image {}.".format(latest_tag, latest_image))

if __name__ == "__main__":
    unittest.main()
