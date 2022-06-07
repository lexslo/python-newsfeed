import sys
from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

# add a new route that will resolve to /api/users
# specify the method to be of type POST
@bp.route('/users', methods=['POST'])
def signup():
    data = request.get_json()
    db = get_db()

    # attempt to create new user
    try:
        # create a new user using dictionary syntax data['property']
        newUser = User(
            username = data['username'],
            email = data['email'],
            password = data['password']
        )

        # save in database
        db.add(newUser)
        db.commit()
    except:
        print(sys.exc_info()[0])

        # INSERT failed, so rollback and send error to front end
        # ensures that the database won't lock up when deployed to Heroku
        db.rollback()
        return jsonify(message = 'Signup Failed'), 500

    session.clear()
    session['user.id'] = newUser.id
    session['loggedIn'] = True

    return jsonify(id = newUser.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
    # remove session variables
    session.clear()
    # 204 indicates there is no content
    return '', 204

@bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()

    # check if email address entered is in database
    try:
        user = db.query(User).filter(User.email == data['email']).one()
    except:
        print(sys.exc_info()[0])

        return jsonify(message = 'Incorrect credentials'), 400

    if user.verify_password(data['password']) == False:
        return jsonify(message = 'Incorrect credentials'), 400

    session.clear()
    session['user.id'] = user.id
    session['loggedIn'] = True

    return jsonify(id = user.id)