from User_data import init_db
import logging
from flask import Flask, request, jsonify
import flask
from flask_cors import CORS
from bson import ObjectId
from User_data import (
    check_usn_password, get_soft_skills, get_tech_skills, get_points,
    get_projects, get_profile_photo, get_all_users_data, update_email,
    update_soft_skills, update_tech_skills, update_points,
    update_prev_month_points, update_profile_photo, add_new_user,
    get_all_users_points, get_all_users_prev_month_points, add_project,
    update_social_profiles, update_password, create_batch, add_user_to_batch, get_batch_users, check_admin, update_project
)
import base64
from flask_pymongo import PyMongo

app = Flask(__name__)
# Update MongoDB configuration with the correct URI
app.config["MONGO_URI"] = "mongodb+srv://Suresh_10001:Suresh1001databaseAcess@cluster0.7yxg4.mongodb.net/skill_nest?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)
CORS(app)

# Add this to make mongo instance available to other modules


def get_db():
    return mongo.db


# Make mongo instance available to User_data module
init_db(mongo)

logging.basicConfig(level=logging.INFO)


def convert_objectid(document):
    if isinstance(document, dict):
        for key, value in document.items():
            if isinstance(value, ObjectId):
                document[key] = str(value)
            elif isinstance(value, dict):
                convert_objectid(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        convert_objectid(item)
    return document


@app.route('/check_usn_password', methods=['POST'])
def check_usn_password_route():
    data = request.get_json()
    usn = data['usn']
    password = data['password']
    batch_id = data['batch_id']
    result = check_usn_password(usn, password, batch_id)
    if result["status"] == "success":
        result["user"] = convert_objectid(result["user"])
        return jsonify({"status": "success", "data": result["user"]})
    return jsonify({"status": "error", "message": "Invalid USN, password, or batch ID"})


@app.route('/get_soft_skills', methods=['POST'])
def get_soft_skills_route():
    data = request.get_json()
    usn = data['usn']
    batch_id = data['batch_id']
    result = get_soft_skills(usn, batch_id)
    return jsonify({"status": "success", "data": convert_objectid(result)})


@app.route('/get_tech_skills', methods=['POST'])
def get_tech_skills_route():
    data = request.get_json()
    usn = data['usn']
    batch_id = data['batch_id']
    result = get_tech_skills(usn, batch_id)
    return jsonify({"status": "success", "data": convert_objectid(result)})


@app.route('/get_points', methods=['POST'])
def get_points_route():
    data = request.get_json()
    usn = data['usn']
    batch_id = data['batch_id']
    result = get_points(usn, batch_id)
    return jsonify({"status": "success", "data": convert_objectid(result)})


@app.route('/get_projects', methods=['POST'])
def get_projects_route():
    data = request.get_json()
    usn = data['usn']
    batch_id = data['batch_id']
    result = get_projects(usn, batch_id)
    return jsonify({"status": "success", "data": [convert_objectid(project) for project in result]})


@app.route('/get_profile_photo', methods=['POST'])
def get_profile_photo_route():
    data = request.get_json()
    usn = data['usn']
    batch_id = data['batch_id']
    result = get_profile_photo(usn, batch_id)
    return jsonify({"status": "success", "data": convert_objectid(result)})


@app.route('/get_all_users_data', methods=['POST'])
def get_all_user_data_route():
    data = request.get_json()
    batch_id = data['batch_id']
    result = get_all_users_data(batch_id)
    return jsonify({"status": "success", "data": [convert_objectid(user) for user in result]})


@app.route('/update_email', methods=['POST'])
def update_email_route():
    data = request.get_json()
    usn = data['usn']
    password = data['password']
    batch_id = data['batch_id']
    new_email = data['new_email']
    result = update_email(usn, password, batch_id, new_email)
    return jsonify({"status": "success", "message": result})


@app.route('/update_soft_skills', methods=['POST'])
def update_soft_skills_route():
    data = request.get_json()
    usn = data['usn']
    password = data['password']
    batch_id = data['batch_id']
    new_soft_skills = data['new_soft_skills']
    result = update_soft_skills(usn, password, batch_id, new_soft_skills)
    return jsonify({"status": "success", "message": result})


@app.route('/update_tech_skills', methods=['POST'])
def update_tech_skills_route():
    data = request.get_json()
    usn = data['usn']
    password = data['password']
    batch_id = data['batch_id']
    new_tech_skills = data['new_tech_skills']
    result = update_tech_skills(usn, password, batch_id, new_tech_skills)
    return jsonify({"status": "success", "message": result})


@app.route('/update_points', methods=['POST'])
def update_points_route():
    data = request.get_json()
    usn = data['usn']
    password = data['password']
    batch_id = data['batch_id']
    new_points = data['new_points']
    result = update_points(usn, password, batch_id, new_points)
    return jsonify({"status": "success", "message": result})


@app.route('/update_profile_photo', methods=['POST'])
def update_profile_photo_route():
    data = request.get_json()
    usn = data['usn']
    password = data['password']
    batch_id = data['batch_id']
    new_profile_photo = data['new_profile_photo']
    result = update_profile_photo(usn, password, batch_id, new_profile_photo)
    return jsonify({"status": "success", "message": result})


@app.route('/add_new_user', methods=['POST'])
def add_new_user_route():
    data = request.get_json()
    current_usn = data['current_usn']
    current_password = data['current_password']
    batch_id = data['batch_id']
    new_user_data = data['new_user_data']
    result = add_new_user(current_usn, current_password,
                          batch_id, new_user_data)
    return jsonify({"status": "success", "message": result})


@app.route('/get_all_users_points', methods=['POST'])
def get_all_users_points_route():
    data = request.get_json()
    batch_id = data['batch_id']
    result = get_all_users_points(batch_id)
    return jsonify({"status": "success", "data": [convert_objectid(user) for user in result]})


@app.route('/get_all_users_prev_month_points', methods=['POST'])
def get_all_users_prev_month_points_route():
    data = request.get_json()
    batch_id = data['batch_id']
    result = get_all_users_prev_month_points(batch_id)
    return jsonify({"status": "success", "data": [convert_objectid(user) for user in result]})


@app.route('/add_project', methods=['POST'])
def add_project_route():
    logging.info("add_project endpoint hit")
    data = request.get_json()
    usn = data['usn']
    password = data['password']
    batch_id = data['batch_id']
    project_data = {
        "title": data['title'],
        "description": data['description'],
        "live_url": data['live_url'],
        "github_url": data['github_url'],
        "skills_needed": data['skills_needed'],
        "team_project": data['team_project']
    }
    if data['team_project']:
        project_data["team_members"] = data['team_members']
    result = add_project(usn, password, batch_id, project_data)
    return jsonify({"status": "success", "message": result})


@app.route('/update_social_profiles', methods=['POST'])
def update_social_profiles_route():
    data = request.get_json()
    usn = data['usn']
    password = data['password']
    batch_id = data['batch_id']
    new_social_profiles = data['new_social_profiles']
    result = update_social_profiles(
        usn, password, batch_id, new_social_profiles)
    return jsonify({"status": "success", "message": result})


@app.route('/update_password', methods=['POST'])
def update_password_route():
    data = request.get_json()
    usn = data['usn']
    old_password = data['old_password']
    batch_id = data['batch_id']
    new_password = data['new_password']
    result = update_password(usn, old_password, batch_id, new_password)
    return jsonify({"status": "success", "message": result})


@app.route('/create_batch', methods=['POST'])
def create_batch_route():
    """
    Expect JSON data with:
    {
        "batch_name": string,
        "batch_id": string,
        "admin_usn": string,
        "admin_password": string,
        "admin_name": string,
        "admin_email": string
    }
    """
    try:
        data = request.get_json()
        required_fields = ["batch_name", "batch_id", "admin_usn",
                           "admin_password", "admin_name", "admin_email"]

        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({"status": "error", "message": f"Missing required field: {field}"})

        result = create_batch(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/check_admin', methods=['POST'])
def check_admin_route():
    data = request.get_json()
    result = check_admin(data['usn'], data['password'], data['batch_id'])
    return jsonify(result)


@app.route('/add_user_to_batch', methods=['POST'])
def add_user_to_batch_route():
    try:
        data = request.get_json()
        required_fields = ["admin_usn", "admin_password",
                           "batch_id", "new_user_data"]

        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({"status": "error", "message": f"Missing required field: {field}"})

        result = add_user_to_batch(
            data['admin_usn'],
            data['admin_password'],
            data['batch_id'],
            data['new_user_data']
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/get_batch_users', methods=['GET'])
def get_batch_users_route():
    batch_id = request.args.get('batch_id')
    result = get_batch_users(batch_id)
    return jsonify({"status": "success", "data": [convert_objectid(user) for user in result]})


@app.route('/update_project', methods=['POST'])
def update_project_route():
    data = request.get_json()
    result = update_project(
        data['usn'],
        data['password'],
        data['batch_id'],
        {
            "title": data['title'],
            "description": data['description'],
            "live_url": data['live_url'],
            "github_url": data['github_url'],
            "skills_needed": data['skills_needed'],
            "team_project": data['team_project'],
            "team_members": data['team_members']
        }
    )
    return jsonify({"status": "success", "message": result})


@app.route('/get_batch_name', methods=['POST'])
def get_batch_name_route():
    try:
        data = request.get_json()
        batch_id = data.get('batch_id')

        if not batch_id:
            return jsonify({"status": "error", "message": "Batch ID is required"})

        batch = mongo.db.Batches.find_one({"batch_id": batch_id})

        if batch and 'batch_name' in batch:
            return jsonify({
                "status": "success",
                "batch_name": batch['batch_name']
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Batch not found"
            })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Server error"
        })


if __name__ == '__main__':
    app.run(debug=True)
