import requests

USER = "harry.knighton18@students.bhasvic.ac.uk"
PW = "HarryKnighton01234!"

def get_metrics(myQuery):
    ENDPOINT = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
    data = myQuery.to_dict()
    print("Making Request")
    response = requests.post(ENDPOINT, json=data, auth=(USER, PW))
    return response

def get_details(rid):
    ENDPOINT = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
    data = {"rid": rid}
    response = requests.post(ENDPOINT, json=data, auth=(USER, PW))
    return response