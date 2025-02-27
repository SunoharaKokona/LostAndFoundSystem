from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId
from os import remove
from datetime import datetime, timedelta

try:
    client = MongoClient('mongodb://localhost:27017/')
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
except ConnectionFailure as e:
    print("Could not connect to MongoDB: ", e)

def insert_lost_item(item_data):
    db = client['lost_and_found']
    collection = db['lost_items']
    item_data['isRetrieved'] = False
    result = collection.insert_one(item_data)
    return result.inserted_id

def get_lost_items(query=None):
    db = client['lost_and_found']
    collection = db['lost_items']
    if query is None:
        query = {}
    items = collection.find(query)
    item_list = []
    for item in items:
        item_list.append({
            'itemName': item['itemName'],
            'ownerName': item['ownerName'],
            'submitter': item.get('submitter', ''),
            'storageDate': item['storageDate'],
            'itemPhotoPath': item['itemPhotoPath'],
            'notes': item.get('notes', ''),
            'id': ObjectId(item['_id']),
            'isRetrieved': item['isRetrieved'],
            'retriever': item.get('retriever', ''),
            'retrieve_date': item.get('retrieve_date', '')
        })
    return item_list

def get_lost_item_by_id(item_id):
    db = client['lost_and_found']
    collection = db['lost_items']
    item = collection.find_one({'_id': ObjectId(item_id)})
    if item:
        return {
            'itemName': item['itemName'],
            'ownerName': item['ownerName'],
            'submitter': item.get('submitter', ''),
            'storageDate': item['storageDate'],
            'itemPhotoPath': item['itemPhotoPath'],
            'notes': item.get('notes', ''),
            'isRetrieved': item['isRetrieved']
        }
    return None

def delete_lost_item(item_id):
    db = client['lost_and_found']
    collection = db['lost_items']
    item = collection.find_one({'_id': ObjectId(item_id)})  
    result = collection.delete_one({'_id': ObjectId(item_id)}) 
    return result.deleted_count > 0

def setting_delete_lost_item(item_id):
    db = client['lost_and_found']
    collection = db['lost_items']
    item = collection.find_one({'_id': ObjectId(item_id)})  
    result = collection.delete_one({'_id': ObjectId(item_id)})
    if result.deleted_count > 0 and item:
        remove(item['itemPhotoPath'])  
    return result.deleted_count > 0

def mongodb_retrieve_item(item_id, retriever, retrieve_date):
    db = client['lost_and_found']
    collection = db['lost_items']
    result = collection.update_one({'_id': ObjectId(item_id)}, {'$set': {'isRetrieved': True, 'retriever': retriever, 'retrieve_date': retrieve_date}})
    return result.modified_count > 0
