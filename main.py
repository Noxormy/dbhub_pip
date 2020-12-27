from dbhub import get_database


def main():
    db = get_database('b54e8270-f851-679f-a2a1-ad56ab00f584')
    collection = db.get_collection('users')
    user = collection[192]
    print(list)


if __name__ == '__main__':
    main()
