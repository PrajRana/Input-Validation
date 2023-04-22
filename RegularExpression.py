from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api, fields, abort
import re
from flask_sqlalchemy import SQLAlchemy
import json
import datetime

# phone_number = input("Enter your phone number: ")
pattern2 = re.compile("^((\+?(?!0)|(00|011))?[ .-]?(\d{1,3})?[ .-]?\(?(?!0)[0-9]{2,3}\)?[ .-]?)?(\d{3})[ -.](\d{4})$")
# print(pattern.search(phone_number))
#
# name = input("Enter your full name: ")
pattern = re.compile("^([A-Z]?[a-z]*[ ]?[A-Z][’]?)?([A-Z][a-z]*[-,]\s?)?[A-Z][a-z]*[ ]?[A-Z]?[a-z]*[.]?$")
# print(pattern.search(name))

phonebook_db = SQLAlchemy()
app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///phoneBook.db"
phonebook_db.init_app(app)



class UserInfo(phonebook_db.Model):
    name = phonebook_db.Column(phonebook_db.String, nullable=False)
    phone = phonebook_db.Column(phonebook_db.String, primary_key=True, unique=True, nullable=False)

    def dict(self):
        return {
            'name': self.name,
            'phone': self.phone
        }

with app.app_context():
     phonebook_db.create_all()



@app.route("/PhoneBook/add", methods=["POST"])
def get_user_input():
    if request.method == "POST":
        try:
            if ("name" in request.form) and ("phoneNumber" in request.form):
                user_name = request.form["name"]
                user_phone = request.form["phoneNumber"]
                if pattern.search(user_name) and pattern2.search(user_phone):
                    if (UserInfo.query.filter(UserInfo.phone == user_phone).first()):
                        return "user already exists"
                    else:
                        user_info = UserInfo(
                            name=user_name,
                            phone=user_phone
                        )
                        phonebook_db.session.add(user_info)
                        phonebook_db.session.commit()
                        file_open = open("RecordAuditdata.txt", "a+")
                        file_open.write(f"time stamp:{datetime.datetime.now()},POST , name:{user_name},phone:{user_phone} " "")
                        file_open.close()
                        return "Added to database", 200
                else:
                    return 'invalid input', 406
        except:
            return "Unable to add to database", 400
    return 'Sorry other methods not supported at this endpoint', 400


@app.route("/PhoneBook/list", methods=["GET"])
def return_list_phonebook():
    if request.method == "GET":
        try:
            all_data = phonebook_db.session.execute(phonebook_db.select(UserInfo).order_by(UserInfo.name)).scalars()
            fetched_data = all_data.fetchall()
            new_strcut = [val.dict() for val in fetched_data]
            return json.dumps(new_strcut)
        except Exception as e:
            print(e)
            return "Unable to retrieve from database", 400
    return 'Sorry other methods are not supported at this endpoint', 400

@app.route("/PhoneBook/deleteByName",methods=["PUT"])
def delete_by_name():
    if("name" in request.form and "phonenumber" not in request.form):
        Name = request.form["name"]
        if pattern.search(Name):
            if UserInfo.query.filter(UserInfo.name == Name).first():
                phonebook_db.session.delete(UserInfo.query.filter(UserInfo.name == Name).first())
                phonebook_db.session.commit()
                file_open2 = open("RecordAuditdata.txt", "a+")
                file_open2.write(f"time stamp:{datetime.datetime.now()},PUT , name:{Name}")
                file_open2.close()
                return "success", 200
            else:
                return "Username does not exist", 404
        else:
            return "invalid input", 406

@app.route("/PhoneBook/deleteByNumber",methods=["PUT"])
def delete_by_number():
    if ("name" not in request.form and "phoneNumber"  in request.form):
        Phone = request.form["phoneNumber"]
        if pattern2.search(Phone):
            if UserInfo.query.filter(UserInfo.phone == Phone).first():
                phonebook_db.session.delete(UserInfo.query.filter(UserInfo.phone == Phone).first())
                phonebook_db.session.commit()
                file_open3 = open("RecordAuditdata.txt", "a+")
                file_open3.write(f"time stamp:{datetime.datetime.now()},PUT , name:{Phone}\n")
                file_open3.close()
                return "success", 200
            else:
                return "Phone number does not exist", 404
        else:
            return "invalid input", 406


if __name__ == '__main__':
    app.run(debug=True, port=5001)
