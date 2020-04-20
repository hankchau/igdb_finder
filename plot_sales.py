import re
import string
import pandas as pd
import requests
import numpy as np
import unidecode
import matplotlib.pyplot as plt


def sanitize_name(name):
    name = (unidecode.unidecode(name)).lower()

    return name.translate(table)

df = pd.read_csv('vgsales.csv')
sales = df['Global_Sales'][:5000].tolist()
ranks = df['Rank'][:5000].tolist()

"""
plt.plot(ranks, sales)
xticks = np.arange(0, 100, 10)
plt.xlabel('Rank of Game')
plt.ylabel('Globally Shipped (Millions)')
plt.title('Distribution of Top 100 Selling Games')
plt.savefig('vgsales_plot.png')
"""
# top 3000 games
names = df['Name'][:3000].tolist()
url = 'https://api-v3.igdb.com/games'
keyword_url = 'https://api-v3.igdb.com/keywords'

headers = {
    'Accept': 'application/json',
    'user-key': '56d1bc79a1da0e6bb3a3b3aef6d481a9'
}

table = str.maketrans('', '', string.punctuation)

name2keys = {}
keywords = {}
unavail = []

for i in range(len(names)):
    name = sanitize_name(names[i])
    slug = '-'.join(name.split())

    name2keys[name] = []

    fields = 'limit 1; fields keywords,slug; where slug="' + slug + '";'
    req = requests.get(url, headers=headers, data=fields)

    # no result
    if len(req.json()) == 0:
        unavail.append(i)
        continue
    data = req.json()[0]

    if 'keywords' not in data:
        if 'id' not in data:
            # save and exit
            df = pd.DataFrame.from_dict(name2keys, orient='index')
            df.transpose()
            df.to_csv('igdb_keywords.csv')
            print('limit reached')

            errors = pd.DataFrame(unavail)
            errors.to_csv('igdb_notfound.csv')
            print('errors recorded')

            keywords_saved = pd.DataFrame(keywords)
            keywords_saved.to_csv('igdb_keywords_dict.csv')

            print('stopped at ' + str(i) + 'th game')
            exit(0)
        else:
            unavail.append(name)
            continue

    keyword_ids = data['keywords']
    for id in keyword_ids:
        if id in keywords:
            continue

        fields = 'fields name,slug; where id= ' + str(id) + '; '
        req = requests.get(keyword_url, headers=headers, data=fields)
        data = req.json()[0]

        name2keys[name].append(data['name'])
        keywords[id] = (data['name'])

df = pd.DataFrame.from_dict(name2keys, orient='index')
df.transpose()
df.to_csv('igdb_keywords.csv')
print('limit reached')

errors = pd.DataFrame(unavail)
errors.to_csv('igdb_notfound.csv')
print('errors recorded')

keywords_saved = pd.DataFrame(keywords)
keywords_saved.to_csv('igdb_keywords_dict.csv')

print('stopped at ' + str(i) + 'th game')
"""
sorted_args = np.argsort(np.array(keyword_count))[::-1][:50]
print('Top 50 Most Popular Tags')
print('Tag Word   :   Count')
top30Tags = []
for arg in sorted_args:
    tag = keywords[arg]
    top30Tags.append(tag)
    count = keyword_count[arg]
    print(tag + ' : ' + str(count))

print('Top Games Scoring w.r.t Tags')
print('Game   :   Score')
for name in names:
    name = sanitize_name(name)
    score = 0
    for word in name2keys[name]:
        if word in top30Tags:
            score += 1
    print(name + ' : ' + str(score))
"""
