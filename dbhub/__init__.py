from dbhub.dbhub import DbHub


def get_database(token, db_name):
    return DbHub(token, db_name)
