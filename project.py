
import pandas as pd
import pymongo
from flask import Flask

import bson

df = pd.read_csv('intro_bees.csv')
dictionary_list = []
for i in range(0,4590):
    df2 = df.loc[i]

    bee_dict = {
                "Year":  bson.Int64(df2['Year']),
                "Period": df2['Period'],
                "State": df2['State'],
                "ANSI": bson.Int64(df2['ANSI']),
                "Affected by": df2['Affected by'],
                "Pct of Colonies Impacted": bson.Int64(df2['Pct of Colonies Impacted']),
                "state_code": df2['state_code']
                }
    dictionary_list.append(bee_dict)

mylist = dictionary_list

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycollection = mydb["bees"]
# print(myclient.list_database_names())
mycollection.delete_many({})
x = mycollection.insert_many(mylist)

data = mycollection.find({})
# for n in data:
#     print(n)

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': mydb,
    'host': 'localhost',
    'port': 27017
}

# db = MongoEngine()
# db.init_app(app)

@app.route('/')
def index():
    return 'Hello'

@app.route('/data')
def get_data():
    data = mycollection.find({})
    output = []
    for item in data:
        item_data = {"Year":  item['Year'],
                "Period": item['Period'],
                "State": item['State'],
                "ANSI": item['ANSI'],
                "Affected by": item['Affected by'],
                "Pct of Colonies Impacted": item['Pct of Colonies Impacted'],
                "state_code": item['state_code']
                }
        output.append(item_data)
    print(output)
    return {"Data":output}

