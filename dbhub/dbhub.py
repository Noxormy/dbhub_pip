from easydict import EasyDict as edict

import requests
import json

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
        self.__dict = self.__list()

    def __create(self, doc_id, doc):
        doc_dict = doc if isinstance(doc, dict) else dict(doc.__dict__)
        data = {
            'secret': self.__api_key__,
            'collectionName': self.__collection_name__,
            'doc': doc_dict
        }
        if doc_id:
            data['id'] = doc_id

        response = requests.post(url, json=data)
        return json.loads(response.text)

    def __read(self, key):
        params = {
            'secret': self.__api_key__,
            'collectionName': self.__collection_name__,
            'id': key
        }
        response = requests.get(url, params=params)
        parsed_data = edict(json.loads(response.text))
        return parsed_data if not hasattr(parsed_data, 'Error') else None

    def __list(self):
        params = {
            'secret': self.__api_key__,
            'collectionName': self.__collection_name__
        }
        response = requests.get(url + 'list', params=params)
        array = json.loads(response.text)
        response_dict = {}
        for elem in array:
            key = elem[0]
            value = edict(elem[1])
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
        return json.loads(response.text)

    def __delete(self, key):
        data = {
            'secret': self.__api_key__,
            'collectionName': self.__collection_name__,
            'id': key
        }
        response = requests.delete(url, params=data)
        return json.loads(response.text)

    # dict imitation

    def __setitem__(self, key, item):
        self.__create(key, item)
        self.__dict = self.__list()

    def __getitem__(self, key):
        return self.__dict[key]

    def __repr__(self):
        return repr(self.__dict)

    def __len__(self):
        return len(self.__dict)

    def __delitem__(self, key):
        deleted = self.__delete(key)
        self.__dict = self.__list()
        return deleted

    def clear(self):
        for key in self.__dict.keys():
            self.__delete(key)
        self.__dict = self.__list()

    def copy(self):
        return self.__dict.copy()

    def has_key(self, k):
        return k in self.__dict

    def update(self, *args):
        self.__dict.update(*args)
        for key, value in self.__dict.items():
            self.__update(key, value)

        self.__dict = self.__list()

    def keys(self):
        return self.__dict.keys()

    def values(self):
        return self.__dict.values()

    def items(self):
        return self.__dict.items()

    def pop(self, key, default_key):
        true_key = key if key in self.__dict else default_key if default_key in self.__dict else None
        if true_key:
            item = self.__dict[true_key]
            self.__delete(true_key)
            return item
        else:
            raise KeyError(key)

    def __contains__(self, item):
        return str(item) in self.__dict

    def __iter__(self):
        return iter(self.__dict)

    def __str__(self):
        return str(repr(self.__dict))


class obj:
    def __init__(self, dict_data):
        self.__dict__.update(dict_data)
