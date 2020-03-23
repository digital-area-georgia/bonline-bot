import pymongo, os, datetime, dotenv
#load environment
dotenv.load_dotenv()
#auth mongo client
client = pymongo.MongoClient(os.getenv('dbConnStr'))
db = client[os.getenv('dbName')]
col = db[os.getenv('colName')]
client.server_info()


def fix_dates(document):
    """

    :param document: Json formatted document
    :return: document object with fixed/converted date values
    """
    postDate = datetime.datetime.strptime(document.get('PostDate'), "%Y-%m-%dT%H:%M:%S")
    valueDate = datetime.datetime.strptime(document.get('ValueDate'), "%Y-%m-%dT%H:%M:%S")
    document['PostDate'] = postDate
    document['ValueDate'] = valueDate
    return document


def log_to_mongo(document):
    """

    :param document: Json formatted document
    :return: return objectId if data was inserted successfully, if not it will return None
    """
    document = fix_dates(document)
    document_object = {
        'createDate': datetime.datetime.utcnow(),
        'document': document,
        'isRead': False
    }

    result = col.insert_one(document_object)
    if result.acknowledged:
        return str(result.inserted_id)
    else:
        return None


def is_already_in_db(doc_id, doc_key):
    """

    :param doc_id: document Id from document object
    :param doc_key: Doc Key from document object
    :return: False if document(s) was not found in database
    """

    if col.find_one({'document.Id': doc_id, 'document.DocKey': doc_key}, no_cursor_timeout=True) is None:
        return False
    else:
        return True
