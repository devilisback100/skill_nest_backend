from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
import base64
from datetime import datetime
from flask import current_app
import logging

# Global mongo instance
_mongo = None


def init_db(mongo_instance):
    global _mongo
    _mongo = mongo_instance


def get_db():
    if (_mongo is None):
        raise RuntimeError("Database not initialized")
    return _mongo.db


def check_usn_password(usn, password, batch_id):
    db = get_db()
    user = db.Users.find_one(
        {"USN": usn, "password": password, "batch_id": batch_id})
    if user:
        return {"status": "success", "user": user}
    else:
        return {"status": "error", "message": "Invalid USN, password, or batch ID"}


def get_soft_skills(usn, batch_id):
    db = get_db()
    user = db.Users.find_one({"USN": usn, "batch_id": batch_id}, {
        "Soft-skills": 1, "_id": 0})
    return user.get("Soft-skills", [])


def get_tech_skills(usn, batch_id):
    db = get_db()
    user = db.Users.find_one({"USN": usn, "batch_id": batch_id}, {
        "Tech-skills": 1, "_id": 0})
    return user.get("Tech-skills", {
        "skills": [],
        "Tools": [],
        "Programming languages": [],
        "DSA": ""
    })


def get_points(usn, batch_id):
    db = get_db()
    user = db.Users.find_one(
        {"USN": usn, "batch_id": batch_id}, {"points": 1, "_id": 0})
    return user.get("points", "")


def get_projects(usn, batch_id):
    db = get_db()
    user = db.Users.find_one({"USN": usn, "batch_id": batch_id}, {
        "Projects": 1, "_id": 0})
    return user.get("Projects", [])


def get_profile_photo(usn, batch_id):
    db = get_db()
    user = db.Users.find_one({"USN": usn, "batch_id": batch_id}, {
        "profile_photo": 1, "_id": 0})
    return user.get("profile_photo", b'')


def get_all_users_data(batch_id):
    db = get_db()
    users = list(db.Users.find({"batch_id": batch_id}, {"_id": 0}))
    if users:
        return users
    else:
        return {"error": "No users found in the collection"}


def update_user_field(usn, password, batch_id, field_name, new_value):
    result = check_usn_password(usn, password, batch_id)
    if result["status"] == "success":
        if field_name in ["USN", "admin"]:
            return "Error: Cannot update USN or admin fields."
        db = get_db()
        db.Users.update_one({"USN": usn, "batch_id": batch_id}, {
            "$set": {field_name: new_value}})
        return f"{field_name.capitalize()} updated successfully."
    else:
        return result["message"]


def update_email(usn, password, batch_id, new_email):
    return update_user_field(usn, password, batch_id, "email", new_email)


def update_soft_skills(usn, password, batch_id, new_soft_skills):
    return update_user_field(usn, password, batch_id, "Soft-skills", new_soft_skills)


def update_tech_skills(usn, password, batch_id, new_tech_skills):
    return update_user_field(usn, password, batch_id, "Tech-skills", new_tech_skills)


def update_points(usn, password, batch_id, new_points):
    return update_user_field(usn, password, batch_id, "points", new_points)


def update_prev_month_points(usn, password, batch_id, new_prev_month_points):
    return update_user_field(usn, password, batch_id, "prev_month_points", new_prev_month_points)


def update_profile_photo(usn, password, batch_id, new_profile_photo):
    return update_user_field(usn, password, batch_id, "profile_photo", new_profile_photo)


def update_social_profiles(usn, password, batch_id, new_social_profiles):
    return update_user_field(usn, password, batch_id, "Social_profiles", new_social_profiles)


def add_new_user(current_usn, current_password, batch_id, new_user_data):
    result = check_usn_password(current_usn, current_password, batch_id)
    if result["status"] == "success" and result["user"].get("admin", False):
        new_user_data['admin'] = False
        db = get_db()
        db.Users.insert_one(new_user_data)
        return "New user added successfully."
    elif result["status"] == "success":
        return "Error: You do not have permission to add a new user."
    else:
        return result["message"]


def get_all_users_points(batch_id):
    db = get_db()
    users = db.Users.find({"batch_id": batch_id}, {
        "name": 1, "points": 1, "_id": 0})
    user_points = []
    for user in users:
        user_points.append(
            {"name": user.get("name"), "points": user.get("points", "")})
    return user_points


def get_all_users_prev_month_points(batch_id):
    db = get_db()
    users = db.Users.find({"batch_id": batch_id}, {
        "name": 1, "prev_month_points": 1, "_id": 0})
    user_prev_month_points = []
    for user in users:
        user_prev_month_points.append({"name": user.get(
            "name"), "prev_month_points": user.get("prev_month_points", "")})
    return user_prev_month_points


def add_project(usn, password, batch_id, project_data):
    result = check_usn_password(usn, password, batch_id)
    if result["status"] == "success":
        db = get_db()
        db.Users.update_one({"USN": usn, "batch_id": batch_id}, {
            "$push": {"Projects": project_data}})
        return "Project added successfully."
    else:
        return result["message"]


def update_project(usn, password, batch_id, project_data):
    result = check_usn_password(usn, password, batch_id)
    if result["status"] == "success":
        db = get_db()
        db.Users.update_one(
            {"USN": usn, "batch_id": batch_id,
                "Projects.title": project_data["title"]},
            {"$set": {
                "Projects.$.description": project_data["description"],
                "Projects.$.live_url": project_data["live_url"],
                "Projects.$.github_url": project_data["github_url"],
                "Projects.$.skills_needed": project_data["skills_needed"],
                "Projects.$.team_project": project_data["team_project"],
                "Projects.$.team_members": project_data["team_members"]
            }}
        )
        return {"status": "success", "message": "Project updated successfully."}
    else:
        return result["message"]


def update_password(usn, old_password, batch_id, new_password):
    db = get_db()
    user = db.Users.find_one({"USN": usn, "batch_id": batch_id})
    if user and user.get("password") == old_password:
        db.Users.update_one({"USN": usn, "batch_id": batch_id}, {
            "$set": {"password": new_password}})
        return "Password updated successfully."
    else:
        return "Incorrect current password."


def check_admin(usn, password, batch_id):
    db = get_db()
    user = db.Users.find_one(
        {"USN": usn, "password": password, "batch_id": batch_id})
    if user and user.get("admin", False):
        return {"status": "success", "is_admin": True}
    return {"status": "error", "message": "Not authorized as admin", "is_admin": False}


def create_batch(batch_data):
    """
    Create a new batch and its admin user
    """
    try:
        db = get_db()
        # Check if batch already exists
        if db.Batches.find_one({"batch_id": batch_data["batch_id"]}):
            return {"status": "error", "message": "Batch ID already exists"}

        # Create admin user first
        admin_user = {
            "USN": batch_data["admin_usn"],
            "password": batch_data["admin_password"],
            "name": batch_data["admin_name"],
            "email": batch_data["admin_email"],
            "batch_id": batch_data["batch_id"],
            "admin": True,
            "profile_photo": "",
            "points": 0,
            "prev_month_points": 0,
            "Soft-skills": [],
            "Tech-skills": {},
            "Projects": [],
            "Social_profiles": [],
            "date_account_created": datetime.now().strftime("%d-%m-%Y")
        }

        # Create batch
        batch = {
            "batch_id": batch_data["batch_id"],
            "batch_name": batch_data["batch_name"],
            "admin_usn": batch_data["admin_usn"],
            "date_created": datetime.now().strftime("%d-%m-%Y"),
            "members": [batch_data["admin_usn"]]
        }

        # Insert both documents
        db.Users.insert_one(admin_user)
        db.Batches.insert_one(batch)

        return {"status": "success", "message": "Batch created successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def add_user_to_batch(admin_usn, admin_password, batch_id, new_user_data):
    """
    Add a new user to a batch. Only batch admin can add users.
    """
    # Verify admin
    admin_check = check_admin(admin_usn, admin_password, batch_id)
    if not admin_check["is_admin"]:
        return {"status": "error", "message": "Not authorized to add users"}

    try:
        db = get_db()
        # Check if user already exists
        if db.Users.find_one({"USN": new_user_data["USN"]}):
            return {"status": "error", "message": "User already exists"}

        # Add default fields to new user
        new_user_data.update({
            "admin": False,
            "profile_photo": "",
            "points": 0,
            "prev_month_points": 0,
            "Soft-skills": [],
            "Tech-skills": {},
            "Projects": [],
            "Social_profiles": [],
            "date_account_created": datetime.now().strftime("%d-%m-%Y"),
            "batch_id": batch_id  # Use admin's batch_id
        })

        # Insert new user
        db.Users.insert_one(new_user_data)

        # Add user to batch members
        db.Batches.update_one(
            {"batch_id": batch_id},
            {"$push": {"members": new_user_data["USN"]}}
        )

        return {"status": "success", "message": "User added successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_batch_users(batch_id):
    db = get_db()
    users = list(db.Users.find({"batch_id": batch_id}, {"_id": 0}))
    return users


def get_batch_name(batch_id):
    """
    Get batch name from Batches collection
    """
    try:
        db = get_db()
        batch = db.Batches.find_one({"batch_id": batch_id})

        if batch and 'batch_name' in batch:
            return {"status": "success", "batch_name": batch['batch_name']}
        return {"status": "error", "message": "Batch not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
