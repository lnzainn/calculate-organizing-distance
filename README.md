# Calculate organizing distnace

I will be calculating which organizer has organized a WCA competition farthest from where they live. 

It is not possible to know where each person lives and it is not feasible to use 'country_id' of any given person since people may be living in foreign countries while not necessarily holding its citizenship. 

The major components here are -

- Calculate the country where each organizer has competed the most and use that as a starting point. Here, it will be considered as 'home_country'
- Use an online library to get the coordinates of each country. I used this [website](https://www.naturalearthdata.com/downloads/110m-cultural-vectors/)
    - Download the csv and use it along with geopandas
    - Make sure that you clean the data and that the variables are uniformly stored. For example -- USA in WCA's database while it is United States of America in the natural earth data, one of them needs to be changed to the other in order to have uniform naming
- Write code to finally compile everything


## SQL code to get home_country of all the organizers
This is calculated by checking where each organizer has competed the most and then storing that.

All the SQL code is available [here](https://github.com/lnzainn/calculate-organizing-distance/blob/main/home_country.sql)

1. The second query will generate a list of WCA ID and the country where they have competed the most. That csv can be found [here](https://github.com/lnzainn/calculate-organizing-distance/blob/main/generated_csv/most_frequent_country.csv)
2. The third query will return everyone's organized competitions and would additionally have a column 'home_country'


## Extracting coordinates
I then wrote a small python script to extract the coordinates and store it in a csv file.

- Script link: [here](https://github.com/lnzainn/calculate-organizing-distance/blob/main/scripts/extract_coordinates.py)
- Generated CSV: [here](https://github.com/lnzainn/calculate-organizing-distance/blob/main/generated_csv/country_coordinates.csv)

## Compile everything together
And then finally compile everything together using a [script](https://github.com/lnzainn/calculate-organizing-distance/blob/main/scripts/main.py)

And then further refine your search by adding specific filters [somewhat like this](https://github.com/lnzainn/calculate-organizing-distance/blob/main/scripts/filtering.ipynb)
