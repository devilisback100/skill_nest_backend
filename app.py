from flask import Flask, request, jsonify
import flask
from flask_cors import CORS
from bson import ObjectId
from User_data import (
    check_usn_password, get_soft_skills, get_tech_skills, get_points,
    get_projects, get_profile_photo, get_all_users_data, update_email,
    update_soft_skills, update_tech_skills, update_points,
    update_prev_month_points, update_profile_photo, add_new_user,
    get_all_users_points, get_all_users_prev_month_points, add_project
)
import base64

app = Flask(__name__)
CORS(app)

# Helper function to convert ObjectId to string for JSON serialization


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
    result = check_usn_password(usn, password)
    if result["status"] == "success":
        result["user"] = convert_objectid(result["user"])
        return jsonify({"status": "success", "data": result["user"]})
    return jsonify({"status": "error", "message": "Invalid USN or password"})


@app.route('/get_soft_skills', methods=['POST'])
def get_soft_skills_route():
    data = request.get_json()
    usn = data['usn']
    result = get_soft_skills(usn)
    return jsonify({"status": "success", "data": convert_objectid(result)})


@app.route('/get_tech_skills', methods=['POST'])
def get_tech_skills_route():
    data = request.get_json()
    usn = data['usn']
    result = get_tech_skills(usn)
    return jsonify({"status": "success", "data": convert_objectid(result)})


@app.route('/get_points', methods=['POST'])
def get_points_route():
    data = request.get_json()
    usn = data['usn']
    result = get_points(usn)
    return jsonify({"status": "success", "data": convert_objectid(result)})


@app.route('/get_projects', methods=['POST'])
def get_projects_route():
    data = request.get_json()
    usn = data['usn']
    result = get_projects(usn)
    return jsonify({"status": "success", "data": [convert_objectid(project) for project in result]})


@app.route('/get_profile_photo', methods=['POST'])
def get_profile_photo_route():
    data = request.get_json()
    usn = data['usn']
    result = get_profile_photo(usn)
    return jsonify({"status": "success", "data": convert_objectid(result)})


@app.route('/get_all_users_data', methods=['GET'])
def get_all_user_data_route():
    result = get_all_users_data()
    return jsonify({"status": "success", "data": [convert_objectid(user) for user in result]})


@app.route('/update_email', methods=['POST'])
def update_email_route():
    data = request.get_json()
    usn = data['usn']
    password = data['password']
    new_email = data['new_email']
    result = update_email(usn, password, new_email)
    return jsonify({"status": "success", "message": result})


@app.route('/update_soft_skills', methods=['POST'])
def update_soft_skills_route():
    data = request.get_json()
    usn = data['usn']
    password = data['password']
    new_soft_skills = data['new_soft_skills']
    result = update_soft_skills(usn, password, new_soft_skills)
    return jsonify({"status": "success", "message": result})


@app.route('/update_tech_skills', methods=['POST'])
def update_tech_skills_route():
    data = request.get_json()
    usn = data['usn']
    password = data['password']
    new_tech_skills = data['new_tech_skills']
    result = update_tech_skills(usn, password, new_tech_skills)
    return jsonify({"status": "success", "message": result})


@app.route('/update_points', methods=['POST'])
def update_points_route():
    data = request.get_json()
    usn = data['usn']
    password = data['password']
    new_points = data['new_points']
    result = update_points(usn, password, new_points)
    return jsonify({"status": "success", "message": result})


@app.route('/update_profile_photo', methods=['POST'])
def update_profile_photo_route():
    data = request.get_json()
    usn = data['usn']
    password = data['password']
    new_profile_photo = data['new_profile_photo']
    result = update_profile_photo(usn, password, new_profile_photo)
    return jsonify({"status": "success", "message": result})


@app.route('/add_new_user', methods=['POST'])
def add_new_user_route():
    data = request.get_json()
    current_usn = data['current_usn']
    current_password = data['current_password']
    new_user_data = data['new_user_data']
    result = add_new_user(current_usn, current_password, new_user_data)
    return jsonify({"status": "success", "message": result})


@app.route('/get_all_users_points', methods=['GET'])
def get_all_users_points_route():
    result = get_all_users_points()
    return jsonify({"status": "success", "data": [convert_objectid(user) for user in result]})


@app.route('/get_all_users_prev_month_points', methods=['GET'])
def get_all_users_prev_month_points_route():
    result = get_all_users_prev_month_points()
    return jsonify({"status": "success", "data": [convert_objectid(user) for user in result]})


@app.route('/add_project', methods=['POST'])
def add_project_route():
    data = request.get_json()
    usn = data['usn']
    password = data['password']
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
    result = add_project(usn, password, project_data)
    return jsonify({"status": "success", "message": result})


if __name__ == '_main_':
    app.run(debug=True)
