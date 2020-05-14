import requests
from bs4 import BeautifulSoup

url = 'https://www.drugbank.ca/covid-19'
resp = requests.get(url,stream=True)
if not resp.status_code == 200:
    print(resp.return_code)
    exit()

soup = BeautifulSoup(resp.content, 'html.parser')
tables = soup.find_all('table')
print(len(tables))
with open('trials.txt','w') as outf:
    outf.write('source\tpredicate\tobject\tcount\n')
    for t in tables:
        thead = t.contents[0]
        th = thead.contents[0]
        if not th.text == 'Drug':
            continue
        th = thead.contents[1]
        if not th.text == 'Count':
            continue
        lines = t.contents[1].contents
        for tr in lines:
            tds = tr.contents
            a = tds[0].strong.a
            #print(a['href'], a.text)
            drug=f'DRUGBANK:{a["href"].split("/")[-1]}'
            c = tds[1].text
            outf.write(f'{drug}\tin_clinical_trial_for\tMONDO:0100096\t{c}\n')
            #print(c)
