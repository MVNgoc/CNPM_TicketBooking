import json
from ticketbooking import app


def load_categories():
    with open('%s/data/categories.json' % app.root_path, encoding='utf-8') as f:
        return json.load(f)