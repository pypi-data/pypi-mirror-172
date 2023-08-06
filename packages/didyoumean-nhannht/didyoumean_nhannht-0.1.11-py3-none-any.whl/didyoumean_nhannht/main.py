#%%
from os.path import expanduser

import requests
import json

# Get key from json file
home = expanduser("~")
with open(f'{home}/org-one/api_key.json') as f:
    api_key = json.load(f)['apilayer_key']


#%%
payload = {}
headers= {
    "apikey": f"{api_key}"
}
#%% Do not run interactive
# parse args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("query", help="query to search")
args = parser.parse_args()
#%% scratch area
# q = "howw are you ?"
# url_didyoumean = f"https://api.apilayer.com/dymt/did_you_mean_this?q={q}"
# url_suggest = f"https://api.apilayer.com/spell/spellchecker?q={q}"
# suggest = requests.request("GET", url_suggest, headers=headers, data = payload)
# suggest.json()['corrections'][0]['candidates']

# didyoumean = requests.request("GET", url_didyoumean, headers=headers, data = payload)
# didyoumean.json()
#%%
def main():
    q = args.query
    url_didyoumean = f"https://api.apilayer.com/dymt/did_you_mean_this?q={q}"
    url_suggest = f"https://api.apilayer.com/spell/spellchecker?q={q}"
    didyoumean = requests.request("GET", url_didyoumean, headers=headers, data = payload)
    suggest = requests.request("GET", url_suggest, headers=headers, data = payload)
    didyoumean_ismodified = didyoumean.json()['is_modified']
    suggest_candidates = suggest.json()['corrections'][0]['candidates']
    if didyoumean_ismodified:
        print(f"<div><b>Did you mean</b> \"{didyoumean.json()['result']}\"?</div>")
    if suggest_candidates:
        print("<div><b>Other candidate</b></div>")
        print("<ul>")
        for candidate in suggest_candidates:
            print(f"<li>{candidate}</li>")
        print("</ul>")
    #%%
if __name__ == '__main__':
    main()
