import json
import sys
from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
from app.utils.auth import login_required

bp = Blueprint('api', __name__, url_prefix='/api')

# add a new route that will resolve to /api/users
# specify the method to be of type POST
@bp.route('/users', methods=['POST'])
def signup():
    print('In Signup function')
    data = request.get_json()
    db = get_db()
    print('db: ', db)

    # attempt to create new user
    try:
        userData = json.loads(data)
        print('Data: ', userData['username'], userData['email'], userData['password'])
        # create a new user using dictionary syntax data['property']
        newUser = User(
            username = userData['username'],
            email = userData['email'],
            password = userData['password']
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
    print('inside login function')
    data = request.get_json()
    db = get_db()

    # check if email address entered is in database
    try:
        user_data = json.loads(data)
        user = db.query(User)
        user_filtered = user.filter(User.email == user_data['email'])
        one_user = user_filtered.one()
        print('user is ', user)
        print('user_filtered is ', user_filtered)
        print("in line 63 of api.py and one_user is: ", one_user)
    except:
        print(sys.exc_info()[0])

        return jsonify(message = 'Incorrect credentials'), 400

    if one_user.verify_password(user_data['password']) == False:
        return jsonify(message = 'Incorrect credentials'), 400

    session.clear()
    session['user.id'] = one_user.id
    session['loggedIn'] = True

    return jsonify(id = one_user.id)

@bp.route('/comments', methods=['POST'])
@login_required
def comment():
    data = request.get_json()
    db = get_db()

    # attempt to add comment to database
    try:
        newComment = Comment(
            comment_text = data['comment_text'],
            post_id = data['post_id'],
            user_id = session.get('user_id')
        )

        db.add(newComment)
        # performs the INSERT against the database
        db.commit()

    except:
        print(sys.exc_info()[0])
        # discards the pending commit if it fails
        db.rollback()
        return jsonify(message = 'Comment failed'), 500

    return jsonify(id = newComment.id)

@bp.route('/posts/upvote', methods=['PUT'])
@login_required
def upvote():
    data = request.get_json()
    db = get_db()

    try:
        vote_data = json.loads(data)
        # create a new vote w/ incoming id and session id
        newVote = Vote(
            post_id = vote_data['post_id'],
            user_id = session.get('user_id')
        )

        db.add(newVote)
        db.commit()

    except:
        print(sys.exc_info()[0])
        # discards the pending commit if it fails
        db.rollback()
        return jsonify(message = 'Upvote failed'), 500

    return '', 200

@bp.route('/posts', methods=['POST'])
@login_required
def create():
    data = request.get_json()
    db = get_db()

    try:
        # create a new post
        newPost = Post(
            title = data['title'],
            post_url = data['post_url'],
            user_id = session.get('user_id')
        )

        db.add(newPost)
        db.commit()

    except:
        print(sys.exc_info()[0])
        # discards the pending commit if it fails
        db.rollback()
        return jsonify(message = 'Post failed'), 500

    return jsonify(id = newPost.id)

@bp.route('/posts/<id>', methods=['PUT'])
@login_required
def update(id):
  data = request.get_json()
  db = get_db()

  try:
    # retrieve post and update title property
    post = db.query(Post).filter(Post.id == id).one()
    post.title = data['title']
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204

@bp.route('/posts/<id>', methods=['DELETE'])
@login_required
def delete(id):
  db = get_db()

  try:
    # delete post from db
    db.delete(db.query(Post).filter(Post.id == id).one())
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204

