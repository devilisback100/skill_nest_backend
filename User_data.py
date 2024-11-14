from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://Suresh_10001:Suresh1001databaseAcess@cluster0.7yxg4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client['skill_nest']
users_collection = db['Users']


# Function 1: Check if USN and password are correct (returns user or detailed error)
def check_usn_password(usn, password):
    user = users_collection.find_one({"USN": usn})
    if user:
        if user.get("password") == password:
            return {"status": "success", "user": user}
        else:
            return {"status": "error", "message": "Incorrect password"}
    else:
        return {"status": "error", "message": "USN not found"}

# Function 2: Get specific data - Soft Skills


def get_soft_skills(usn):
    user = users_collection.find_one(
        {"USN": usn}, {"Soft-skills": 1, "_id": 0})
    return user.get("Soft-skills", [])


# Function 3: Get specific data - Tech Skills (including subfields: skills, Tools, Programming languages, DSA)
def get_tech_skills(usn):
    user = users_collection.find_one(
        {"USN": usn}, {"Tech-skills": 1, "_id": 0})
    return user.get("Tech-skills", {
        "skills": [],
        "Tools": [],
        "Programming languages": [],
        "DSA": ""
    })

# Function 4: Get specific data - Points


def get_points(usn):
    user = users_collection.find_one({"USN": usn}, {"points": 1, "_id": 0})
    return user.get("points", "")

# Function 5: Get specific data - Projects


def get_projects(usn):
    user = users_collection.find_one({"USN": usn}, {"Projects": 1, "_id": 0})
    return user.get("Projects", [])


# Function 6: Get specific data - Profile Photo
def get_profile_photo(usn):
    user = users_collection.find_one(
        {"USN": usn}, {"profile_photo": 1, "_id": 0})
    return user.get("profile_photo", "")

# Function 7: Get all data for a specific user

def get_all_users_data():
    users = list(users_collection.find({}, {"_id": 0}))
    if users:
        return users
    else:
        return {"error": "No users found in the collection"}



# Function 8: Update specific fields (email, soft skills, tech skills, points, etc.)
def update_user_field(usn, password, field_name, new_value):
    result = check_usn_password(usn, password)
    if result["status"] == "success":
        # Make sure that fields like 'USN' and 'admin' cannot be updated
        if field_name in ["USN", "admin"]:
            return "Error: Cannot update USN or admin fields."

        # Update the specific field in the document
        users_collection.update_one(
            {"USN": usn}, {"$set": {field_name: new_value}})
        return f"{field_name.capitalize()} updated successfully."
    else:
        return result["message"]

# Update email


def update_email(usn, password, new_email):
    return update_user_field(usn, password, "email", new_email)


# Update soft skills
def update_soft_skills(usn, password, new_soft_skills):
    return update_user_field(usn, password, "Soft-skills", new_soft_skills)


# Update full tech skills object (skills, Tools, Programming languages, DSA)
def update_tech_skills(usn, password, new_tech_skills):
    return update_user_field(usn, password, "Tech-skills", new_tech_skills)

# Update points


def update_points(usn, password, new_points):
    return update_user_field(usn, password, "points", new_points)


# Update prev month points
def update_prev_month_points(usn, password, new_prev_month_points):
    return update_user_field(usn, password, "prev_month_points", new_prev_month_points)


# Update profile photo
def update_profile_photo(usn, password, new_profile_photo):
    return update_user_field(usn, password, "profile_photo", new_profile_photo)


# Function 9: Add a new user (only if current user is admin)
def add_new_user(current_usn, current_password, new_user_data):
    # Check if the current user is an admin
    result = check_usn_password(current_usn, current_password)

    # User is admin
    if result["status"] == "success" and result["user"].get("admin", False):
        # Add the new user (admin flag for new user will be False by default)
        new_user_data['admin'] = False
        users_collection.insert_one(new_user_data)
        return "New user added successfully."
    elif result["status"] == "success":
        return "Error: You do not have permission to add a new user."
    else:
        return result["message"]

# Function 10: Get all users' points with their names


def get_all_users_points():
    users = users_collection.find({}, {"name": 1, "points": 1, "_id": 0})
    user_points = []
    for user in users:
        user_points.append(
            {"name": user.get("name"), "points": user.get("points", "")})
    return user_points

# Function 11: Get all users' previous month points with their names


def get_all_users_prev_month_points():
    users = users_collection.find(
        {}, {"name": 1, "prev_month_points": 1, "_id": 0})
    user_prev_month_points = []
    for user in users:
        user_prev_month_points.append({"name": user.get(
            "name"), "prev_month_points": user.get("prev_month_points", "")})
    return user_prev_month_points


