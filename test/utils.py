import json

def load_fixture(name):
    with open(f'test/fixtures/{name}', encoding='utf-8') as fp:
        return json.load(fp)