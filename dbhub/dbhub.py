import requests
import json
from types import SimpleNamespace

from idna import unicode

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
        self.__api_key__ = api_key
        self.__collection_name__ = collection_name

    def create(self, doc_id, doc):
        data = {
            'secret': self.__api_key__,
            'collectionName': self.__collection_name__,
            'doc': doc,
            'id': doc_id
        }
        response = requests.post(url, json=data)
        return parse(response.text)

    def __read(self, key):
        params = {
            'secret': self.__api_key__,
            'collectionName': self.__collection_name__,
            'id': key
        }
        response = requests.get(url, params=params)
        return parse(response.text)

    def __list(self):
        params = {
            'secret': self.__api_key__,
            'collectionName': self.__collection_name__
        }
        response = requests.get(url + 'list', params=params)
        array = parse(response.text)
        response_dict = {}
        for elem in array:
            key = elem[0]
            value = elem[1]
            response_dict[key] = value
        return response_dict

    def __update(self, key, doc):
        data = {
            'secret': self.__api_key__,
            'collectionName': self.__collection_name__,
            'id': key,
            'doc': doc
        }
        response = requests.patch(url, json= data)
        return parse(response.text)

    def __delete(self, key):
        data = {
            'secret': self.__api_key__,
            'collectionName': self.__collection_name__,
            'id': key
        }
        response = requests.delete(url, params=data)
        return parse(response.text)

    # dict imitation

    def __setitem__(self, key, item):
        self.__create(key, item)

    def __getitem__(self, key):
        return self.__read(key)

    def __repr__(self):
        self.__dict__ = self.__list()
        return repr(self)

    def __len__(self):
        self.__dict__ = self.__list()
        return len(self.__dict__)

    def __delitem__(self, key):
        return self.__delete(key)

    def clear(self):
        self.__dict__ = self.__list()
        for key in self.__dict__.keys():
            self.__delete(key)

    def copy(self):
        self.__dict__ = self.__list()
        return self.__dict__.copy()

    def has_key(self, k):
        self.__dict__ = self.__list()
        return k in self.__dict__ or k in self

    def update(self, *args, **kwargs):
        self.__dict__ = self.__list()
        self.__dict__.update(*args, **kwargs)
        for key, value in self.__dict__.items():
            self.__update(key, value)

    def keys(self):
        self.__dict__ = self.__list()
        return self.__dict__.keys()

    def values(self):
        self.__dict__ = self.__list()
        return self.__dict__.values()

    def items(self):
        self.__dict__ = self.__list()
        return self.__dict__.items()

    def pop(self, key, default_key):
        self.__dict__ = self.__list()
        true_key = key if key in self.__dict__ else default_key if default_key in self.__dict__ else None
        if true_key:
            item = self.__dict__[true_key]
            self.__delete(true_key)
            return item
        else:
            raise KeyError(key)

    def __contains__(self, item):
        self.__dict__ = self.__list()
        return item in self.__dict__

    def __iter__(self):
        self.__dict__ = self.__list()
        return iter(self.__dict__)

    # def __str__(self):
    #     self.__dict__ = self.__list()
    #     return str(repr(self.__dict__))


def parse(json_data):
    return json.loads(json_data, object_hook=lambda d: SimpleNamespace(**d))
