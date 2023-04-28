from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime

connection_string = 'mongodb+srv://nurulhidayahsianipar1:nurulsianipar01@cluster0.kbrbk2l.mongodb.net/test'
client= MongoClient(connection_string)
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    # sample__receive = request.args.get('sample_give')
    # print(sample__receive)
    articles = list(db.diary.find({},{'_id' : False}))
    return jsonify ({'articles' : articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    filename = f'file-{mytime}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    filename = f'profile-{mytime}.{extension}'
    profilename = f'static/{filename}'
    profile.save(profilename)
    

    doc={
        'file': save_to,
        'profile':profilename,
        'title' : title_receive,
        'content' : content_receive
    }
    db.diary.insert_one(doc)
    return jsonify ({'msg': 'data tersimpan'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)