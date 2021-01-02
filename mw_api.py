import json
import requests

try:
    api_key = open('mwapi.key','r').read().strip()
except:
    print("Could not read api key")
    quit()

syns_file = open('synonyms.csv','a')
ants_file = open('antonyms.csv','a')
rels_file = open('related_words.csv','a')
defs_file = open('short_defs.csv','a')

def make_api_request(word):
    url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"+word+"?key="+api_key
    response = requests.get(url)
    return response.json()[0]

def get_synonyms_from_json(json_obj):
    ls = json_obj['meta']['syns']
    syns = list(set([j for i in ls for j in i]))
    syns.sort()
    return syns


def get_antonyms_from_json(json_obj):
    try:
        ls = json_obj['meta']['ants']
    except KeyError:
        return []
    ants = list(set([j for i in ls for j in i]))
    ants.sort()
    return ants

def get_related_words_from_json(json_obj):
    rw = ''
    try:
        rw = json_obj["def"][0]["sseq"][0][0][1]["rel_list"]
    except KeyError:
        return []
    rw = [j for i in rw for j in i]
    r = []
    for w in rw:
        r.append(w["wd"])
    r = list(set(r))
    r.sort()
    return r

def get_short_defs_from_json(json_obj):
    defs = json_obj["shortdef"]
    defs.sort()
    return defs

def get_info(word):
    js = make_api_request(word)
    syns = get_synonyms_from_json(js)
    ants = get_antonyms_from_json(js)
    rels = get_related_words_from_json(js)
    defs = get_short_defs_from_json(js)
    return (word, syns, ants, rels, defs)

def create_csv_entries(info):
    (word, syns, ants, rels, defs) = info
    syns = [word] + syns
    ants = [word] + ants
    rels = [word] + rels
    defs = [word] + defs
    syns = ','.join(syns) + '\n'
    ants = ','.join(ants) + '\n'
    rels = ','.join(rels) + '\n'
    defs = ','.join(defs) + '\n'
    l = (syns, ants, rels, defs)
    return l

def write_csvs(csvs):
    (syns, ants, rels, defs) = csvs
    syns_file.write(syns)
    ants_file.write(ants)
    rels_file.write(rels)
    defs_file.write(defs)
    

def main():
    wordfile = open("words.txt")
    wordlist = wordfile.read().split()
    wordfile.close()
    for word in wordlist:
        print("Downloading:",word)
        i = get_info(word)
        csvs = create_csv_entries(i)
        write_csvs(csvs)


main()
