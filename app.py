from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)   #flask application object
api = Api(app)          

client = MongoClient('localhost')  #connection class MongoClient acknowledges all writes to MongoDB
db = client.comments               #db is the database 
users = db["users"]                #users is the collection in db used to store comments and usernames

# insert class is defined for inserting username and comment in the database db
class insert(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data["username"]      #username is the name of a person who is commenting
        comment = posted_data["comment"]        #comment is the comment of the person
        
        #if the username doesn't exist, then we have to insert a new user to the database
        if users.count({"username":username})==0:
            db.users.insert({"username":username,"comment":comment,"reply":[],"comment_num":1})     
       #else if the username already exists, then we will increase the count of the comment of that user
        else:
            comment_num = users.find({"username":username})[0]["comment_num"]    #comment_num stores the count of comments of a particular user
            comment_num+=1
            db.users.insert({"username":username,"comment":comment,"reply":[],"comment_num":comment_num})   #this method inserts the data to the database

        retJson = {
            "status":200     # if no error has occured, then this "status":200 is shown on the console
        }
        return jsonify(retJson)

# reply class is defined for replying to a particular comment of a particular user
class reply(Resource):
    def post(self):   
        posted_data = request.get_json()       #Posted_data is the dictionary used to store the already existing data(usernames and comments)
        username = posted_data["username"]      # username is the user whose comment we have to reply on
        reply_username = posted_data["reply_username"]    #reply_username is the user who is replying
        reply_comment = posted_data["reply_comment"]      #reply_comment is the comment by the reply_username
        comment_num = posted_data["comment_num"]          #count of the total comments of the user whose comment we have to reply on
        user = db.users.find({"username":reply_username,"comment_num":comment_num})[0]   #it finds the reply_username and the comment_num in the users collection 
        temp_list = user["reply"]                         #a new list is created
        temp_list.append({"reply_username":username,"reply_comment":reply_comment})      #the reply_comment and reply_username is appended to that list
        users.update_one({"username" : reply_username,"comment_num":comment_num},{"$set":{"reply" : temp_list}})   #the above list is then updated to the collection
        retJson = {
            "status":200     # if no error has occured, then this "status":200 is shown on the console
        }
        return jsonify(retJson)

#view_all class is defined to view the comments
class view_all(Resource):     
    def get(self):
        users = {}                   #a new dictionary is created to store the usernames and comments for viewing 
        data = db.users.find({})     #all the data from the 'users' collection is stored in data
        for doc in data:                  #we update all the usernames and comments to the dictionary 
            user = doc["username"]      
            comment = doc["comment"]
            users.update({user:comment})
        return jsonify(users)      #the dictionary is returned for viewing
        
        
#add_resource is used to add a resource to the api.
api.add_resource(insert,'/insert_comment')    
api.add_resource(reply,'/reply')
api.add_resource(view_all,'/view_all')

if __name__=="__main__":
    app.run(debug=True)  # by debug = True, the server will reload on source changes, and provide a debugger for errors
