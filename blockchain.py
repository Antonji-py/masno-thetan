import requests
from datetime import datetime
from bs4 import BeautifulSoup


def create_session():
    s = requests.Session()
    s.headers.update({
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    })

    return s


def get_sid(session):
    response = session.get(f"https://bscscan.com/token/0x98eb46cbf76b19824105dfbcfa80ea8ed020c6f4")
    soup = BeautifulSoup(response.text, "lxml")
    script = soup.find_all("script", {"type": "text/javascript"})
    sid = script[4].text.strip().replace("var sid = '", "").split("';")[0]

    return sid


def get_transactions(session, contract_address, sid, method):
    response = session.get(f"https://bscscan.com/token/generic-tokentxns2?m=normal&contractAddress={contract_address}&a=&sid={sid}&p=1")
    soup = BeautifulSoup(response.text, "lxml")
    txns_raw = soup.find_all("tr")[1:]
    txns = []

    for txn in txns_raw:
        tds = txn.find_all("td")
        # print(tds[6])
        if tds[1].find("span")["title"] == method:
            txn_data = list()
            txn_hash = txn_data.append(tds[0].text)
            method = txn_data.append(tds[1].find("span")["title"])
            timestamp = txn_data.append(int(datetime.timestamp(datetime.strptime(tds[2].text, "%Y-%m-%d %H:%M:%S"))))
            _from = txn_data.append(tds[4].text)
            to = txn_data.append(tds[6].text)
            print(txn_data)

        break

    # ts = soup.find_all("tr")[-10:]
    # t = soup.find_all("tr")
    # for x in ts:
    #     print(x)
    # print()
    # for x in t:
    #     print(x)
        

s = create_session()
sid = get_sid(s)
get_transactions(s, "0x98eb46cbf76b19824105dfbcfa80ea8ed020c6f4", sid, "Match Transaction")
