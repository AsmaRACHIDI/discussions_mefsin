import json

import requests


# url = "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique/discussions"
from dataset import open_json, append_to_csv

url = "https://www.data.gouv.fr/api/1/datasets/rappelconso/#/discussions"

# with open("tmp.json2", "w") as file:
#     response = requests.get(url)
#     data = json.loads(response.text)
#     json.dump(data, file, indent=2, ensure_ascii=False)


data = open_json("tmp.json")
report = []
for d in data:
    discussion = {
        "id": d["id"],
        "created": d["created"],
        "dataset_id": d["subject"]["id"],
        "title": d["title"],
        "first_message": d["discussion"][0]["content"]
    }
    # for message in d["discussion"]:
    #     out = {
    #         **discussion,
    #         "message": message["content"]
    #     }
    report.append({**discussion})

append_to_csv("data/dataset.csv", report)
