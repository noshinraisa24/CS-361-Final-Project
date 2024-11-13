from flask import Flask, jsonify, request
import json
import os


app = Flask(__name__)
PROFILE_FILE = 'profile.json'


def load_profile():
   if os.path.exists(PROFILE_FILE):
       with open(PROFILE_FILE, 'r') as file:
           return json.load(file)
   return {}


def save_profile(profile_data):
   with open(PROFILE_FILE, 'w') as file:
       json.dump(profile_data, file)


@app.route('/profile', methods=['GET'])
def get_profile():
   profile = load_profile()
   return jsonify(profile)


@app.route('/profile', methods=['POST'])
def update_profile():
   profile_data = request.json
   save_profile(profile_data)
   return jsonify({'status': 'Profile updated successfully'})


if __name__ == '__main__':
   app.run(port=5001)

