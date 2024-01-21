from business_dev.crawler import web_crawler
from business_dev.crawler.frozen_json import FacadeJSON
from collections import defaultdict


def app_main(data) -> dict:
    feed = FacadeJSON(data)
    processed = defaultdict()
    processed["result"] = dict()

    try:
        if feed.errorMessage.status != 200:
            raise AttributeError
    except KeyError:
        if feed.status != 200:
            return {"status": "[Error] 데이터를 받아오지 못했습니다."}

    for arrival in feed.realtimeArrivalList:
        try:
            processed["result"][arrival.trainLineNm].append(arrival.arvlMsg2)

        except KeyError:
            processed["result"][arrival.trainLineNm] = [arrival.arvlMsg2]

    processed["result"] = {key: list(set(value)) for key, value in processed["result"].items()}
    processed.update({"status": "success"})
    return processed


if __name__ == "__main__":
    res = app_main(web_crawler.load_data())
