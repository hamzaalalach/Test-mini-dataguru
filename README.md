# Test mini dataguru
## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment . This keeps your dependencies for each project separate and organaized.

```bash
pip install virtualenv
cd YOUR_PROJECT_DIRECTORY_PATH/
virtualenv env
source env/bin/activate
```
More instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [unittest](https://docs.python.org/3.8/library/unittest.html) Python testing framework.

#### Running the server

From within the `src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python app.py
```

The application by default runs in debug mode, on port 5000.

## API REFERENCE

### Endpoints

- GET '/images?page={number}'
- POST '/images'
- GET '/tags'
- POST '/tags'
- GET '/images/{image_id}/tags'
- POST '/images/{image_id}/tags'
- GET '/tags/{tag_id}/images?page={number}'


##### GET '/images?page={number}'
- Fetches the available images paginated by 10, given a page number which is by default 1
- Request Arguments: None
- Response sample: 

```json
{
    "images": [
        {
            "id": 6,
            "name": "Untitled.jpg",
            "type": "jpg",
            "url": "/home/ooo/Workshop/monk/src/uploads/Untitled.jpg"
        }
    ],
    "success": true,
    "total_images": 1
}

```
##### POST '/images'
- Uploads and creates a new image.
- Request Arguments: Required
    - file: Form-Data file key
- Response sample: 

```json
{
    "image": {
        "id": 7,
        "name": "clownfish.jpg",
        "type": "jpg",
        "url": "/home/ooo/Workshop/monk/src/uploads/clownfish.jpg"
    },
    "success": true
}
```

##### GET '/tags'
- Fetches the available tags
- Request Arguments: None
- Response sample: 

```json
{
    "success": true,
    "tags": [
        {
            "id": 3,
            "name": "Cat"
        }
    ],
    "total_tags": 1
}
```

##### POST '/tags'
- Uploads and creates a new image.
- Request Arguments: Required
    - name: String
- Response sample: 

```json
{
    "success": true,
    "tag": {
        "id": 4,
        "name": "Dog"
    }
}
```

##### GET '/images/{image_id}/tags'
- Fetches all the tags on a certain image identified by `image_id`
- Request Arguments: None
- Response sample: 

```json
{
    "success": true,
    "tags": [
        {
            "id": 3,
            "name": "Cat"
        }
    ]
}

```
##### POST '/images/{image_id}/tags'
- Add a new tag to a given image identified by `image_id`.
- Request Arguments: Required
    - id: Int
- Response sample: 

```json
{
    "message": "Added tag 4 to image 3.",
    "success": true
}

```

##### GET '/tags/{tag_id}/images?page={number}'
- Fetches all images with a given tag identified by `tag_id` paginated by 10
- Request Arguments: None
- Response sample: 

```json
{
    "images": [
        {
            "id": 3,
            "name": "Untitled5.jpg",
            "type": "jpg",
            "url": "/home/ooo/Workshop/monk/src/uploads/Untitled5.jpg"
        }
    ],
    "success": true
}
```

## API ERROR CODES:

 - 400: bad request
 - 422: unprocessable
 - 404: resource not found
 - 405: method not allowed
 - 401: unauthorized
 - 500: internal server error
 - 200: ok

## Testing
To run the tests, execute:

```
createdb monk_test
python test_app.py
```

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE) file for details.

## Author

Created by [Hamza Alalach](https://twitter.com/Hamzaalalach) for Monk.