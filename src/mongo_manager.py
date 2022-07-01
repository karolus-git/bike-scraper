from pymongo import MongoClient

from config import MONGO_HOST
from config import MONGO_PORT
from config import MONGO_DATABASE
from config import MONGO_TABLE
from config import MONGO_USER
from config import MONGO_PWD

def init_db():
    """Initialization of the mongo Databse

    Returns:
        collection: the desired collection
    """

    #Get a client
    client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PWD}@{MONGO_HOST}:{MONGO_PORT}/")

    #Load the DB
    mongo_database = client[MONGO_DATABASE]

    #Get the collection and return it
    mongo_collection = mongo_database[MONGO_TABLE]

    return mongo_collection

def update_db(mongo_collection, result):
    """Insert or update an object in the mongo collection

    Args:
        mongo_collection (_type_): _description_
        result (_type_): _description_
    """

    # Filter to find the wanted object
    filter = {
        "name" : result.get("name"), 
        "source" : result.get("source")
        }

    # Get the object
    stored_obj = mongo_collection.find_one(filter)

    # If the object exists, we update it
    if stored_obj:

        # Create tuples for dates and prices if they are not already in the stored object
        for key in ["datetimes", "prices"]:
            if key not in stored_obj.keys():
                #Push the key for initialization
                stored_obj[key] = [stored_obj.get(key[:-1])]

        # If a price has been found during scraping, we put it at the end of the prices tuple
        if ("price" in result.keys()) and ("datetime" in result.keys()):
            stored_obj["prices"].append(result.get("price"))
            stored_obj["datetimes"].append(result.get("datetime"))

        # Update the object with the scraped data
        stored_obj.update(result)
        newvalues = { "$set": stored_obj }

        # Push back in database
        x = mongo_collection.update_many(filter, newvalues)

        print(f"{stored_obj.get('name')} updated")

    #Otherwise, we create it
    else:
        #Create the object
        x = mongo_collection.insert_one(result)

        print(f"{result.get('name')} inserted")