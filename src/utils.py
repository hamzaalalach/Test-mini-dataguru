ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ELEMENTS_PER_PAGE = 10

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_elements_paginated(elements, page):
    start = (page - 1) * ELEMENTS_PER_PAGE
    end = start + ELEMENTS_PER_PAGE
    formatted_elements = [element.format() for element in elements]

    return formatted_elements[start:end]