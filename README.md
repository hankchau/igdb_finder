# IGDB
A simple script for retrieving game information from IGDB's API.

## package.py
```
python3 package.py --infile='vgsales.csv' --limit=500 --fields='gameinfo'
```

--infile:<br/>
    \t A required argument that specifies a csv input file that includes a list of game titles to be searched for.<br/><br/>


--key:<br/>
    -Users can specify an App key that is required to access the database. If no keys are provided, the script will search based on my key, which has a limit on items returned per query, and a monthly query quota.<br/><br/>


--fields:<br/>
  Specifies which types of data to retrieve. Possible values are:
    'gameinfo': which corresponds to the basic info of a game
    'gameart': Art related data, such as cover photo
    'sideinfo': Information tangent to the game itself, such as the number of followers on IGDB, etc.<br/><br/>


--limit:<br/>
  The upper limit of the number of entries returned from the query.<br/><br/>


Note:
  package.py uses the external library Pandas.<br/><br/>


### Link to Dev Blog:
--https://www.projectzeta.org/blog
