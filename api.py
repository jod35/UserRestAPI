from flask import (Flask,
                    request,
                    jsonify,
                    make_response)

from marshmallow import Schema,fields
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
import os


BASE_DIR=os.path.realpath(os.path.dirname(__file__))



app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///'+ os.path.join(BASE_DIR,'myapp.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SQLALCHEMY_ECHO"]=True


db=SQLAlchemy(app)


class User(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(255),nullable=False)
    email=db.Column(db.String(80),nullable=False)
    password=db.Column(db.Text)


    """def __init__(self,username,email,password):
        self.username=username
        self.email=email
        self.password=password
    """


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def create_password(self,password):
        self.password=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)


class userSchema(Schema):
    id=fields.Integer()
    username=fields.Str()
    email=fields.Str()
    password=fields.Str()



@app.route('/users',methods=['GET'])
def get_users():
    users=User.query.order_by(User.id.desc()).all()

    users_=userSchema(many=True).dump(users)


    return make_response(jsonify({
        "users":users_}),200)

@app.route('/users',methods=['POST'])
def create_user():
    data=request.get_json()
    username=data.get('username')
    email=data.get('email')
    password=data.get('password')

    new_user=User(username=username,email=email)

    new_user.create_password(password)

    new_user.save()

    user_=userSchema().dump(new_user)


    return make_response(jsonify({"user":user_,"message":"User Created"}),201)

@app.route('/user/<int:id>')
def get_user_by_id(id):
    user=User.query.get_or_404(id)

    user_=userSchema().dump(user)


    return make_response(jsonify({"success":True,"user":user_}))

@app.route('/user/<int:id>',methods=['PATCH'])
def update_user_infor(id):
    user=User.query.get_or_404(id)

    data=request.get_json()


    user.username=data.get('username')
    user.email=data.get('email')


    db.session.commit()
    

    user_=userSchema().dump(user)


    return make_response(jsonify({"message":"Info Updated","success":True,"user":user_}))


@app.route('/user/<int:id>',methods=['DELETE'])
def delete_user(id):
    user=User.query.get_or_404(id)

    user.delete()

    user_=userSchema().dump(user)

    return make_response(jsonify({"message":"User Deleted","success":True,"user":user_}))


@app.errorhandler(404)
def not_found(err):
    return make_response(jsonify({"message":"Not Found"}))

@app.errorhandler(500)
def server_error(err):
    return make_response(jsonify({"message":"Something went wrong"}))





@app.shell_context_processor
def make_shell_context():
    return {
            "app":app,
            "db":db,
            "User":User}



if __name__ == "__main__":
    app.run(debug=True)
