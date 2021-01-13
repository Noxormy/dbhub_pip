from easydict import EasyDict as edict
import requests
import json

from dbhub.exceptions import is_res_ok, get_error, NotFoundException, WrongDataException, CredentialsException, \
    ServiceException

url = 'https://dbhub-py.herokuapp.com/'


class DbHub:
    def __init__(self, token, db_name):
        self.token = token
        self.db_name = db_name
        self.collections = []

    def get_collection(self, collection_name):
        collection = Collection(self.token, self.db_name, collection_name)
        self.collections.append(collection)
        return collection


class Collection:
    def __init__(self, token, db_name, collection_name):
        self.__headers = {"Authorization": "Bearer %s" % token}
        self.__db_name = db_name
        self.__collection_name = collection_name

        try:
            self.__dict = self.__list()
        except CredentialsException as e:
            raise CredentialsException(e.msg) from e
        except NotFoundException:
            self.__dict = {}

    def __create(self, doc_id, doc):
        doc_dict = to_dict(doc)
        data = {
            'db_name': self.__db_name,
            'collection_name': self.__collection_name,
            'data': doc_dict
        }
        if doc_id:
            data['doc_id'] = doc_id

        response = requests.post(url, json=data, headers=self.__headers)
        if is_res_ok(response):
            return json.loads(response.text)
        else:
            raise get_error(response)

    # def __read(self, key):
    #     params = {
    #         'db_name': self.__db_name,
    #         'collection_name': self.__collection_name,
    #         'doc_id': key
    #     }
    #     response = requests.get(url, params=params, headers=self.__headers)
    #
    #     if is_res_ok(response):
    #         return edict(json.loads(response.text))
    #     else:
    #         raise get_error(response)

    def __list(self):
        params = {
            'db_name': self.__db_name,
            'collection_name': self.__collection_name
        }
        response = requests.get(url + 'list', params=params, headers=self.__headers)

        if is_res_ok(response):
            response_dict = json.loads(response.text)

            parsed_data = {}
            for key, value in response_dict.items():
                parsed_data[key] = edict(value)

            return response_dict
        else:
            raise get_error(response)

    def __update(self, key, doc):
        doc_dict = to_dict(doc)

        data = {
            'db_name': self.__db_name,
            'collection_name': self.__collection_name,
            'doc_id': key,
            'data': doc_dict
        }
        response = requests.patch(url, json=data, headers=self.__headers)

        if is_res_ok(response):
            return json.loads(response.text)
        else:
            raise get_error(response)

    def __delete(self, key):
        data = {
            'db_name': self.__db_name,
            'collection_name': self.__collection_name,
            'doc_id': key
        }
        response = requests.delete(url, params=data, headers=self.__headers)

        if is_res_ok(response):
            return json.loads(response.text)
        else:
            raise get_error(response)

    # dict imitation

    def __setitem__(self, key, item):
        real_key = str(key)

        try:
            result = self.__create(real_key, item)
            self.__dict[real_key] = item
            return result
        except WrongDataException:
            raise ValueError(item)  # Consider that None is not valid value
        except ServiceException as e:
            raise ServiceException(e.msg)

    def __getitem__(self, key):
        real_key = str(key)
        return edict(self.__dict[real_key])

    def __repr__(self):
        return repr(self.__dict)

    def __len__(self):
        return len(self.__dict)

    def __delitem__(self, key):
        real_key = str(key)

        try:
            self.__delete(real_key)
            del self.__dict[real_key]
        except NotFoundException as e:
            raise KeyError(key)

    def clear(self):
        for key in self.__dict.keys():
            self.__delitem__(key)

        self.__dict.clear()

    def copy(self):
        return self.__dict.copy()

    def has_key(self, k):
        real_key = str(k)
        return real_key in self.__dict

    def update(self, upd_dict):
        try:
            for key, value in upd_dict.items():
                real_key = str(key)
                self.__update(real_key, value)

            self.__dict.update(upd_dict)
        except WrongDataException as e:
            raise ValueError(upd_dict)  # Consider that None is invalid value, you can use {} or []
        except NotFoundException as e:
            raise KeyError(upd_dict)  # Probably you've tried to update the element that not exist
        except Exception as e:        # This method should only be used for existing elements
            raise e

    def keys(self):
        return self.__dict.keys()

    def values(self):
        return self.__dict.values()

    def items(self):
        return self.__dict.items()

    def pop(self, key, default=None):
        real_key = str(key)
        if not (real_key in self.__dict):
            if not default:
                raise KeyError(key)
            else:
                return default

        item = self.__dict[real_key]
        self.__delitem__(real_key)
        return edict(item)

    def __contains__(self, item):
        return str(item) in self.__dict

    def __iter__(self):
        return iter(self.__dict)

    def __str__(self):
        return str(repr(self.__dict))


def to_dict(obj, class_key=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = to_dict(v, class_key)
        return data
    elif hasattr(obj, "_ast"):
        return to_dict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [to_dict(v, class_key) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, to_dict(value, class_key))
                     for key, value in obj.__dict__.items()
                     if not callable(value) and not key.startswith('_')])
        if class_key is not None and hasattr(obj, "__class__"):
            data[class_key] = obj.__class__.__name__
        return data
    else:
        return obj
