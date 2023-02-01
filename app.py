#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Wednesday 01 Feb. 2023
# ==============================================================================

import json
import requests

from pymongo import MongoClient


# -- Connection to the mongoDB
client = MongoClient('mongodb://root:example@localhost:27017/')

# -- Load API Data
request_API = requests.get('https://pokebuildapi.fr/api/v1/pokemon')
extract_data = request_API.text     # extract data from the request
pokemon_data = json.loads(extract_data)     # convert into json




def from_api_to_mongo() -> None:
    """ Duplicate data from an API to insert it into a new Collection on MongoDB """

    try:
        # -- Get list of DB
        list_DB = client.list_database_names()

        # -- Check if JDG DB exists
        if 'JDG' not in list_DB:
            # -- Create DB JDG
            db_JDG = client['JDG']

            # -- Create 'pokemon' collection
            Collection = db_JDG['pokemon']

            # Insert into the new collection
            if isinstance(pokemon_data, list):
                Collection.insert_many(pokemon_data)
            else:
                Collection.insert_one(pokemon_data)

            print("The Collection 'Pokemon' is filled")

        else:
            print("The DB 'JDG' is already exists")

            # -- Get collection list of JDG DB
            db_JDG = client['JDG']
            list_coll = db_JDG.list_collection_names()

            # -- Check if 'pokemon' collection exists
            if 'pokemon' not in list_coll:
                # -- Create 'pokemon' collection
                Collection = db_JDG['pokemon']

                # -- Insert into the new collection
                if isinstance(pokemon_data, list):
                    Collection.insert_many(pokemon_data)
                else:
                    Collection.insert_one(pokemon_data)

                print("The Collection 'Pokemon' is filled")

            else:
                print("The Collection 'pokemon' is already exists")

                # -- Collection
                Collection = db_JDG['pokemon']

                # -- Check if 'pokemon' collection is already filled or not
                results = list(Collection.find())

                if len(results) == 0:
                    # -- Insert into the collection
                    if isinstance(pokemon_data, list):
                        Collection.insert_many(pokemon_data)
                    else:
                        Collection.insert_one(pokemon_data)

                    print("The Collection 'Pokemon' is filled")

                else:
                    # -- Update the collection
                    if isinstance(pokemon_data, list):
                        for data in pokemon_data:
                            Collection.update_one({'id': data['id']},  {'$set': data}, upsert=True)
                    else:
                        Collection.update_one({'id': data['id']},  {'$set': data}, upsert=True)

                    print("The Collection 'Pokemon' is updated")

    except Exception as e:
        print(f"""Error : {e}""")


def add_Darty_Papa() -> None:
    """ Add a new pokemon 'Darty Papa' into the Collection 'pokemon' """

    # Darty Papa Data
    data = {
            "id": 899,
            "pokedexId": 899,
            "name": "Darty Papa",
            "image": "https://tenor.com/fr/view/kassos-darty-papa-gif-5752923",
            "videoYoutube": "https://www.youtube.com/watch?v=Gt5-xU1-Ows",
            "slug": "Darty Papa",
            "stats": { "HP": 100000000, "attack": 100000000, 
                       "defense": 2, "special\_attack": 100000000, 
                       "special\_defense": 2, "speed": 1 }
    }

    try:
        # -- Connect to the 'pokemon' collection
        db_JDG = client['JDG']
        Collection = db_JDG['pokemon']

        # -- Check if Darty Papa exist or not
        darty_papa_id = Collection.find_one({'id': 899}, None)

        if darty_papa_id:
        # -- Insert the Darty Papa data
            Collection.update_one({'id': data}, {'$set': data}, upsert=True)
            print("Darty Papa is updated")

        else:
            Collection.insert_one(data)
            print("Darty Papa has been added")

    except Exception as e:
        print(f"""Error : {e}""")


def export_in_json() -> None:
    """ Export a MongoDB Collection in JSON """

    # -- Get the DB and the Collection
    db_JDG = client['JDG']
    Collection = db_JDG['pokemon']

    # -- Fetch all documents from the collection, but dont get the '_id'
    documents = Collection.find({}, {'_id': 0})

    # -- Save in JSON
    with open('database.json', 'w') as export:
        json.dump(list(documents), export, indent=2)




if __name__ == '__main__':
    from_api_to_mongo()
    add_Darty_Papa()
    export_in_json()

    # -- Close the connection
    client.close()