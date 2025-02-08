from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
import base64

uri = "mongodb+srv://Suresh_10001:Suresh1001databaseAcess@cluster0.7yxg4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client['skill_nest']
users_collection = db['Users']

def check_usn_password(usn, password):
    user = users_collection.find_one({"USN": usn})
    if user:
        if user.get("password") == password:
            return {"status": "success", "user": user}
        else:
            return {"status": "error", "message": "Incorrect password"}
    else:
        return {"status": "error", "message": "USN not found"}

def get_soft_skills(usn):
    user = users_collection.find_one(
        {"USN": usn}, {"Soft-skills": 1, "_id": 0})
    return user.get("Soft-skills", [])

def get_tech_skills(usn):
    user = users_collection.find_one(
        {"USN": usn}, {"Tech-skills": 1, "_id": 0})
    return user.get("Tech-skills", {
        "skills": [],
        "Tools": [],
        "Programming languages": [],
        "DSA": ""
    })

def get_points(usn):
    user = users_collection.find_one({"USN": usn}, {"points": 1, "_id": 0})
    return user.get("points", "")

def get_projects(usn):
    user = users_collection.find_one({"USN": usn}, {"Projects": 1, "_id": 0})
    return user.get("Projects", [])

def get_profile_photo(usn):
    user = users_collection.find_one({"USN": usn}, {"profile_photo": 1, "_id": 0})
    return user.get("profile_photo", b'')

def get_all_users_data():
    users = list(users_collection.find({}, {"_id": 0}))
    if users:
        return users
    else:
        return {"error": "No users found in the collection"}

def update_user_field(usn, password, field_name, new_value):
    result = check_usn_password(usn, password)
    if result["status"] == "success":
        if field_name in ["USN", "admin"]:
            return "Error: Cannot update USN or admin fields."
        users_collection.update_one(
            {"USN": usn}, {"$set": {field_name: new_value}})
        return f"{field_name.capitalize()} updated successfully."
    else:
        return result["message"]

def update_email(usn, password, new_email):
    return update_user_field(usn, password, "email", new_email)

def update_soft_skills(usn, password, new_soft_skills):
    return update_user_field(usn, password, "Soft-skills", new_soft_skills)

def update_tech_skills(usn, password, new_tech_skills):
    return update_user_field(usn, password, "Tech-skills", new_tech_skills)

def update_points(usn, password, new_points):
    return update_user_field(usn, password, "points", new_points)

def update_prev_month_points(usn, password, new_prev_month_points):
    return update_user_field(usn, password, "prev_month_points", new_prev_month_points)

def update_profile_photo(usn, password, new_profile_photo):
    return update_user_field(usn, password, "profile_photo", new_profile_photo)

def add_new_user(current_usn, current_password, new_user_data):
    result = check_usn_password(current_usn, current_password)
    if result["status"] == "success" and result["user"].get("admin", False):
        new_user_data['admin'] = False
        users_collection.insert_one(new_user_data)
        return "New user added successfully."
    elif result["status"] == "success":
        return "Error: You do not have permission to add a new user."
    else:
        return result["message"]

def get_all_users_points():
    users = users_collection.find({}, {"name": 1, "points": 1, "_id": 0})
    user_points = []
    for user in users:
        user_points.append(
            {"name": user.get("name"), "points": user.get("points", "")})
    return user_points

def get_all_users_prev_month_points():
    users = users_collection.find(
        {}, {"name": 1, "prev_month_points": 1, "_id": 0})
    user_prev_month_points = []
    for user in users:
        user_prev_month_points.append({"name": user.get(
            "name"), "prev_month_points": user.get("prev_month_points", "")})
    return user_prev_month_points

def add_project(usn, password, project_data):
    result = check_usn_password(usn, password)
    if result["status"] == "success":
        users_collection.update_one(
            {"USN": usn},
            {"$push": {"Projects": project_data}}
        )
        return "Project added successfully."
    else:
        return result["message"]


