import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from MongoDB import *
from bson import ObjectId
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

scheduler = BackgroundScheduler()

def delete_retrieved_items():
    one_week_ago = datetime.now() - timedelta(weeks=1)
    delete_lost_items_by_date(one_week_ago)

def delete_lost_items_by_date(date):
    db = client['lost_and_found']
    collection = db['lost_items']
    result = collection.delete_many({'isRetrieved': True, 'retrieve_date': {'$lt': date}})
    for item in result.deleted_count:
        remove(item['itemPhotoPath'])
    print(f"Deleted {result.deleted_count} retrieved items older than {date}")

scheduler.add_job(delete_retrieved_items, 'cron', day_of_week='mon', hour=0, minute=0)
scheduler.start()

##########渲染页面的路由##########

@app.route("/", defaults={'path': 'Index.html'})
@app.route("/<path>")
def index(path):
    return render_template(path)

@app.route("/SubmitLostItem.html")
def submit_lost_item_page():
    return render_template("SubmitLostItem.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':  
            session['logged_in'] = True
            return redirect(url_for('settings'))  
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route("/Settings.html")
def settings():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    items_from_db1 = get_lost_items()  
    return render_template("Settings.html", items_db1=items_from_db1)

@app.route("/InquireLostItem.html", methods=['GET', 'POST']) 
def lost_items():
    if request.method == 'POST':
        item_name = request.form.get('itemName', '')
        owner_name = request.form.get('ownerName', '')
        submitter = request.form.get('submitter', '')  
        storage_date = request.form.get('storageDate', '')
        notes = request.form.get('notes', '')  
        is_retrieved = request.form.get('isRetrieved', None)  

        query = {'isRetrieved': False}  
        if item_name:
            query['itemName'] = {'$regex': item_name, '$options': 'i'}
        if owner_name:
            query['ownerName'] = {'$regex': owner_name, '$options': 'i'}
        if submitter:
            query['submitter'] = {'$regex': submitter, '$options': 'i'}  
        if storage_date:
            query['storageDate'] = storage_date
        if notes:
            query['notes'] = {'$regex': notes, '$options': 'i'}  

        items = get_lost_items(query)
    else:
        items = get_lost_items({'isRetrieved': False})  

    return render_template("InquireLostItem.html", items=items)

##########处理数据的路由##########

@app.route('/submit_lost_item', methods=['POST'])
def submit_lost_item():
    item_name = request.form['itemName']
    owner_name = request.form['ownerName']
    submitter = request.form['submitter']  
    storage_date = request.form['storageDate']
    item_photo = request.files['itemPhoto']
    notes = request.form['notes']  

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    photo_path = os.path.join('static', 'Images', f'{timestamp}_{item_photo.filename}')
    os.makedirs(os.path.dirname(photo_path), exist_ok=True)
    item_photo.save(photo_path)
    photo_path = photo_path.replace('\\', '/')

    item_data = {
        'itemName': item_name,
        'ownerName': owner_name,
        'submitter': submitter,  
        'storageDate': storage_date,
        'itemPhotoPath': photo_path,
        'notes': notes,
        'isRetrieved': False  
    }

    inserted_id = insert_lost_item(item_data)
    print(f"Item submitted successfully with ID: {inserted_id}")
    return jsonify({'message': 'Item submitted successfully', 'inserted_id': str(inserted_id)})

@app.route('/retrieve_item', methods=['POST'])
def retrieve_item():
    item_id = request.form['itemId']
    retriever = request.form['retriever']
    retrieve_date = request.form['retrieveDate']

    lost_item = get_lost_item_by_id(item_id)
    if not lost_item:
        return jsonify({'message': 'Item not found'}), 404

    if mongodb_retrieve_item(item_id,retriever,retrieve_date): 
        return jsonify({'message': 'Item retrieved successfully'})
    else:
        return jsonify({'message': 'Failed to update item retrieval status'}), 500

@app.route('/delete_item', methods=['POST'])
def delete_item():
    item_id = request.form['item_id']
    setting_delete_lost_item(item_id) 
    return jsonify({'message': 'Item deleted successfully'})

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

##########错误处理##########
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

##########主逻辑##########
if __name__ == '__main__':
    app.secret_key = 'your_secret_key'  
    app.run(debug=True)