from flask import Blueprint, render_template
# Blueprint() lets us consolidate routes onto a single bp object 
# that the parent app can register later. 
# This corresponds to using the Router middleware of Express.js.
from app.models import Post
from app.db import get_db

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def index():
    # get all posts
    # returns a session connection that's tied to this route's context
    db = get_db()
    posts = db.query(Post).order_by(Post.created_at.desc()).all()

    return render_template('homepage.html', posts=posts)

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/post/<id>')
def single(id):
    # get single post by id
    db = get_db()
    # use the filter() method on the connection object to specify the SQL WHERE clause
    post = db.query(Post).filter(Post.id == id).one()

    return render_template('single-post.html', post=post)