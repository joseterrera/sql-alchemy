from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def root():
    """Homepage redirects to list of users."""
    return redirect("/users")


@app.route('/users')
def users_index():
    """Show a page with info on all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods={"GET"})
def users_new_form():
  """Show form that creates a new user"""
  return render_template('users/new.html')


@app.route('/users/new', methods={"POST"})
def users_new():
  """Form submission for creating a new user"""
  new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

  db.session.add(new_user)
  db.session.commit()

  return redirect("/users")



@app.route('/users/<int:user_id>')
def users_show(user_id):
  """Show a page with info on a specific user"""
  user = User.query.get_or_404(user_id)
  return render_template('users/edit.html', user=user)



