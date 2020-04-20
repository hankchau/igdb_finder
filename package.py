import argparse
import unidecode
import csv
import string
import requests
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('--key', dest='key', default='56d1bc79a1da0e6bb3a3b3aef6d481a9', help='API Access Key')
parser.add_argument('--infile', dest='infile', default='', help='Input CSV file of games')
parser.add_argument('--fields', dest='fields', default='gameinfo', help='A string indicating which type of data to retrieve from DB')
parser.add_argument('--limit', dest='limit', default='', help='The limit of entries retrieved')

args = parser.parse_args()


def read_csv():
    if args.infile != '':
        with open(args.infile) as f:
            reader = csv.reader(f)
            game_titles = list(reader)
        return game_titles

    print('please provide a list of games in a csv file')
    exit(0)


def sanitize_name(name):
    table = str.maketrans('', '', string.punctuation)
    name = (unidecode.unidecode(name)).lower()

    return name.translate(table)


def save(name2keys, unavail, keywords):
    df = pd.DataFrame.from_dict(name2keys, orient='index')
    df.transpose()
    df.to_csv('igdb_keywords.csv')
    print('limit reached')

    errors = pd.DataFrame(unavail)
    errors.to_csv('igdb_notfound.csv')
    print('errors recorded')

    keywords_saved = pd.DataFrame(keywords)
    keywords_saved.to_csv('igdb_keywords_dict.csv')


def main():
    url = 'https://api-v3.igdb.com/games'
    keyword_url = 'https://api-v3.igdb.com/keywords'
    headers = {
        'Accept': 'application/json',
        'user-key':args.key
    }

    game_titles = read_csv()

    name2keys = {}
    keywords = {}
    unavail = []

    for i in range(len(game_titles)):
        name = sanitize_name(game_titles[i])
        slug = '-'.join(name.split())

        name2keys[name] = []
        limit = 'limit ' + args.limit

        fields = ''
        if args.fields == 'gameinfo':
            fields = 'age_ratings,alternative_names,bundles,category,collection,created_at,dlcs,expansions,external_games,first_release_date,franchise,franchises,game_engines,game_modes,genres,involved_companies,keywords,multiplayer_modes,name,parent_game,platforms,player_perspectives,release_dates,,similar_games,slug,standalone_expansions,status,storyline,summary,tags,themes,time_to_beat'

        elif args.fields == 'gameart':
            fields = 'artworks,videos,cover,screenshots'

        elif args.fields == 'sideinfo':
            fields = 'aggregated_rating,aggregated_rating_count,follows,hypes,popularity,pulse_count,rating,rating_count,total_rating,total_rating_count,updated_at,url,version_parent,version_title,websites'

        query = limit + '; fields ' + fields + '; where slug="' + slug + '";'
        req = requests.get(url, headers=headers, data=query)

        # no result
        if len(req.json()) == 0:
            unavail.append(i)
            continue
        data = req.json()[0]

        if 'keywords' not in data:
            if 'id' not in data:
                # save and exit
                save(name2keys, unavail, keywords)
                print('game not found')
                exit(1)

            else:
                unavail.append(name)
                continue

        keyword_ids = data['keywords']
        for id in keyword_ids:
            if id in keywords:
                continue

            fields = 'fields name; where id= ' + str(id) + '; '
            req = requests.get(keyword_url, headers=headers, data=fields)
            data = req.json()[0]

            name2keys[name].append(data['name'])
            keywords[id] = (data['name'])

    save(name2keys, unavail, keywords)


if __name__ == '__main__':
    main()
