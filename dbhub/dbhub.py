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
        parsed_data = json.loads(response.text)
        return parsed_data if not hasattr(parsed_data, 'Error') else None

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
        if hasattr(array, 'Error'):
            return None

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
        response = requests.patch(url, json=data)
        parsed_data = json.loads(response.text)
        return parsed_data if not hasattr(parsed_data, 'Error') else None

    def __delete(self, key):
        data = {
            'secret': self.__api_key__,
            'collectionName': self.__collection_name__,
            'id': key
        }
        response = requests.delete(url, params=data)
        parsed_data = json.loads(response.text)
        return parsed_data if not hasattr(parsed_data, 'Error') else None

    # dict imitation

    def __setitem__(self, key, item):
        real_key = str(key)
        result = self.__create(real_key, item)
        if result:
            self.__dict[real_key] = item
        else:
            raise Exception('Element with key [%s] was not added into the collection' % real_key)

    def __getitem__(self, key):
        real_key = str(key)
        return edict(self.__dict[real_key])

    def __repr__(self):
        return repr(self.__dict)

    def __len__(self):
        return len(self.__dict)

    def __delitem__(self, key):
        real_key = str(key)
        deleted = self.__delete(real_key)
        if deleted:
            del self.__dict[real_key]
            return deleted
        else:
            raise Exception('Cannot delete element with key %s from the collection' % real_key)

    def clear(self):
        for key in self.__dict.keys():
            deleted = self.__delete(key)
            if not deleted:
                raise Exception('Cannot delete element with key [%s] from the collection' % key)

        self.__dict.clear()

    def copy(self):
        return self.__dict.copy()

    def has_key(self, k):
        real_key = str(k)
        return real_key in self.__dict

    def update(self, upd_dict):
        self.__dict.update(upd_dict)
        for key, value in upd_dict.items():
            real_key = str(key)
            updated = self.__update(real_key, value)
            if not updated:
                raise Exception('Cannot update element with key [%s]' % real_key)

    def keys(self):
        return self.__dict.keys()

    def values(self):
        return self.__dict.values()

    def items(self):
        return self.__dict.items()

    def pop(self, key, default_key):
        real_key = str(key)
        real_default_key = str(default_key)

        true_key = real_key if real_key in self.__dict else real_default_key if real_default_key in self.__dict else None
        if true_key:
            item = self.__dict[true_key]
            deleted = self.__delete(true_key)
            if not deleted:
                raise Exception('Cannot delete element with key [%s] from the collection' % true_key)
            return edict(item)
        else:
            raise KeyError(real_key)

    def __contains__(self, item):
        return str(item) in self.__dict

    def __iter__(self):
        return iter(self.__dict)

    def __str__(self):
        return str(repr(self.__dict))


class obj:
    def __init__(self, dict_data):
        self.__dict__.update(dict_data)
