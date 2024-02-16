import requests
from bs4 import BeautifulSoup

def run() -> dict:
    url = r'https://www.tukorea.ac.kr/tukorea/1096/subview.do'
    response = requests.get(url)
    result = {}
    dict1 = {}

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        board_table = soup.find('table', class_='board-table horizon1')

        if board_table:
            notice = board_table.find('tr', class_='notice')

            if notice:
                td_subject = notice.find('td', class_='td-subject')
                title = td_subject.get_text()
                dict1["title"] = title


            if notice:
                td_write = notice.find('td', class_='td-write')
                author = td_write.get_text()
                dict1["author"] = author

            if notice:
                td_date = notice.find('td', class_='td-date')
                date = td_date.get_text()
                dict1["date"] = date

            if notice:
                if td_subject:
                    link_base = td_subject.find('a', href=True)
                    link = link_base.get_text()
                    dict1["link"] = link
        else:
            pass
    else:
        pass

    result["informations"] = dict1

    return result
