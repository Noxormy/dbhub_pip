import requests


url = 'https://dbhub.herokuapp.com/'


def get_database(api_key):
    return DbHub(api_key)


class DbHub:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_collection(self, collection_name):
        return Collection(self.api_key, collection_name)


class Collection:
    def __init__(self, api_key, collection_name):
        self.api_key = api_key
        self.collection_name = collection_name

    def create(self, doc):
        data = {
            'secret': self.api_key,
            'collectionName': self.collection_name,
            'doc': doc
        }
        response = requests.post(url, json=data)
        return response.text

    def read(self, id):
        params = {
            'secret': self.api_key,
            'collectionName': self.collection_name,
            'id': id
        }
        response = requests.get(url, params=params)
        return response.text

    def list(self):
        params = {
            'secret': self.api_key,
            'collectionName': self.collection_name
        }
        response = requests.get(url + '/list', params=params)
        return response.text

    def update(self, id, doc):
        data = {
            'secret': self.api_key,
            'collectionName': self.collection_name,
            'id': id,
            'doc': doc
        }
        response = requests.patch(url, json= data)
        return response.text

    def delete(self, id):
        data = {
            'secret': self.api_key,
            'collectionName': self.collection_name,
            'id': id
        }
        response = requests.delete(url, params=data)
        return response.text
