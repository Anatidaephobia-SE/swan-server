import requests

def recieve_mail_list(url, email_uuid):
    params = {"email_id" : email_uuid}
    response = requests.get(url, params=params)
    if(response.status_code != 200):
        return None
    try:
        emails = response.json().get("recievers", None)
        emails = [e for e in emails.split(',') if '@' in e]
        return emails
    except Exception as e:
        return None

def test_mail_api(url):
    params = {"email_id" : "test"}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return False
    try:
        emails = response.json().get("recievers", None)
        emails = [e for e in emails.split(',') if '@' in e]
        return len(emails) > 0
    except Exception as e:
        print(e)
        return False