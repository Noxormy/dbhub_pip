from dbhub.dbhub import DbHub


def get_database(api_key):
    return DbHub(api_key)
