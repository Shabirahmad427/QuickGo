#use for retrieving QuicGo subcellular localization
#Uploading the Uniprot ID of the genes

import requests
import sys

def get_annotations(uniprot_id):
    quickgo_url = f"https://www.ebi.ac.uk/QuickGO/services/annotation/stats?geneProductId={uniprot_id}&aspect=cellular_component"
    teste = requests.get(quickgo_url).json()
    return teste

def choose_go_from_stats(go_json):
    found_go = []
    for key in go_json["results"]:
        if key["groupName"] == "annotation":
            for type in key["types"]:
                if type["type"] == "goId":
                    for value in type["values"]:
                        found_go.append(value)
    if not found_go:
        return ["N/A","N/A"]
    found_go = sorted(found_go, key=lambda x: x['percentage'], reverse=True)
    return [found_go[0]['key'],found_go[0]['name']]


with open(sys.argv[1], "r") as f:
    ids = []
    for line in f:
        ids.append(line.replace("\n", ""))

with open("cellular_component_results.txt", "w") as f:
    for id in ids:
        result = choose_go_from_stats(get_annotations(id))
        f.write(f"{id}\t{result[0]}\t{result[1]}\n")
