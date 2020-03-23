import requests, base64, schedule, time, dotenv
from methods.log import *
dotenv.load_dotenv()
sendSlackerAlerts = False


def generate_token():
    """

    :return: Bearer token generated from TokenGenerationEndpoint
    """
    try:
        client_id = os.getenv('client_id')
        client_secret = os.getenv('client_secret')
        grant_type = os.getenv('grant_type')
        scope = os.getenv('scope')
        url = os.getenv('TokenGenerationEndpoint')
        basic_authorization = base64.b64encode(('Basic' + client_id + ':' + client_secret).encode("utf-8"))

        payload = f'grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}&scope={scope}'
        headers = {
          'Authorization': basic_authorization,
          'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == requests.status_codes.codes.get('OK'):
            return response.json().get('access_token')
        else:
            error = f'Cannot read token, status_code: {response.status_code} reason: ' + str(response.json().get('error_description'))
            print(error)
            if sendSlackerAlerts:
                send_slack_alert(message=error)
    except Exception as e:
        error = f'generate_token thrown an exception: {str(e)}'
        if sendSlackerAlerts:
            send_slack_alert(message=error)
        print(error)

    return None


def get_documents(bearer_token, account_number=os.getenv('accountNumber'), currency=os.getenv('currency')):
    """

    :param bearer_token: token from TokenGenerationEndpoint
    :param account_number: bank account number
    :param currency: string value of currency (gel/usd)
    :return: json format response of DocumentsEndpoint (api/documents/todayactivities)
    """
    try:

        url = str.format(os.getenv('documentsEndpoint'),
                         accountNumber=account_number,
                         currency=currency)
        headers = {
            'Authorization': f'Bearer {bearer_token}'
        }

        response = requests.request("GET", url, headers=headers)

        if response.status_code == requests.status_codes.codes.get('OK'):

            return response.json()
        else:
            error = f'Cannot read documents, status_code: {response.status_code} Message: ' + str(response.json().get('Message'))
            print(error)
            if sendSlackerAlerts:
                send_slack_alert(message=error)
    except Exception as e:
        error = f'get_documents thrown an exception: {str(e)}'
        if sendSlackerAlerts:
            send_slack_alert(message=error)
        print(error)
    return None


def parse():
    print(f'Process Started! Time: {datetime.datetime.now()}')
    docs = get_documents(bearer_token=generate_token())
    if docs:
        print(f'{len(docs)} documents found.')
        for doc in (doc for doc in docs if doc.get('Credit') != 0):
            if doc:
                print(f'document found, id: {doc.get("Id")}')
                if not is_already_in_db(doc_id=doc.get('Id'), doc_key=doc.get('DocKey')):
                    object_id = log_to_mongo(document=doc)
                    if object_id:
                        print(f'document {doc.get("Id")} logged into database, ObjectId: ' + str(object_id))
                    else:
                        error = f'log failed! log_to_mongo returned : {str(object_id)}'
                        print(error)
                        if sendSlackerAlerts:
                            send_slack_alert(message=error)
                else:
                    print(f'document {doc.get("Id")} is already in db')
            else:
                error = 'document is None!'
                print(error)
                if sendSlackerAlerts:
                    send_slack_alert(message=error)
    else:
        error = 'get_documents returned Nonetype value (docs is None)'
        print(error)
    print(f'Done! Time: {datetime.datetime.now()}')


def has_environment_variables():
    requirements = ['client_id',
                    'client_secret',
                    'grant_type',
                    'scope',
                    'tokenGenerationEndpoint',
                    'documentsEndpoint',
                    'accountNumber',
                    'currency',
                    'dbConnStr',
                    'dbName',
                    'colName']
    ok = True
    for req in requirements:
        if os.getenv(req) is None:
            print(f'environment variable "{req}" is required!')
            ok = False
    return ok


def has_slacker_environment_variables():
    requirements = ['slackerToken',
                    'slackerChannel',
                    'slackerUsername']
    ok = True
    for req in requirements:
        if os.getenv(req) is None:
            print(f'environment variable "{req}" is required!')
            ok = False
    return ok


def start_scheduler(interval):
    """

    :param interval: Time interval in minutes
    :param slackerAlerts: True/False value
    :return:
    """
    print(f'Bot will start every {interval} minute(s).')
    schedule.every(int(interval)).minutes.do(parse)
    while True:
        schedule.run_pending()
        print(f'Sleeping for {interval} minute(s)...')
        time.sleep(int(interval) * 60)


if __name__ == '__main__':
    if has_environment_variables():
        print("Business Online API Today Activities Bot")
        while True:
            interval = input('Enter interval in minutes (eg. 5) : ').upper()
            if not interval.isdigit():
                print("Please enter digits only!")
                continue
            if interval.isdigit():
                slackerAlerts = input('Do you want to receive alerts in Slack? (y/n) : ').upper()
                if slackerAlerts == "Y":
                    sendSlackerAlerts = True
                    if has_slacker_environment_variables():
                        from methods.slacker import *
                        print("Bot will send alerts!")
                        start_scheduler(interval=interval)
                    else:
                        break
                elif slackerAlerts == "N":
                    sendSlackerAlerts = False
                    print("Bot will not send alerts!")
                    start_scheduler(interval=interval)
                else:
                    print('You entered incorrect value, try again!')
