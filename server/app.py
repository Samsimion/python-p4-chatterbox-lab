from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET","POST"])
def messages():
    if request.method=="GET":
        mess= [m.to_dict() for m in Message.query.order_by('created_at').all()]
        response=make_response(
            mess,
            200
        )
        return response
    elif request.method=="POST":
        data= request.get_json()
        new_mess = Message(
            body=data.get("body"),
            username=data.get("username"),
        )
        db.session.add(new_mess)
        db.session.commit()
        return make_response(
            new_mess.to_dict(),
            201
        )

@app.route('/messages/<int:id>', methods=["GET","PATCH","DELETE"])
def messages_by_id(id):
    messa= Message.query.filter(Message.id==id).first()
    if request.method=="GET":
        messa_dict = messa.to_dict()
        response= make_response(
            messa_dict,
            200
        )
        return response
    elif request.method=="PATCH":
        data =request.get_json()
        if "body" in data:
            messa.body = data["body"]
        db.session.commit()
        return make_response(
            messa.to_dict(),
            200
        )
    
    elif request.method=="DELETE":
        db.session.delete(messa)
        db.session.commit()
        response_body = {
            "deleted_successfully": True,
            "message": "Message deleted"
        }
        response= make_response(
            response_body,
            200
        )
        return response
    


if __name__ == '__main__':
    app.run(port=5555)
