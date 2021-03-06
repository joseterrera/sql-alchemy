"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://picsum.photos/200/300"

class User(db.Model):
  """Site User"""
  # """Better reoresentation:"""
  # def __repr__(self):
  #     """Show info about pet."""

  #     p = self
  #     return f"<User {p.id} {p.first_name} {p.last_name} {p.image_url}>"

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key = True)
  first_name = db.Column(db.Text, nullable=False)
  last_name = db.Column(db.Text, nullable=False)
  image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

  posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

  @property
  def full_name(self):
    """Return full name of user"""
    return f" {self.first_name} {self.last_name} "

class Post(db.Model):
  """Blog Post"""

  __tablename__= "posts"

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.Text, nullable=False)
  content = db.Column(db.Text, nullable=False)
  created_at = db.Column(
    db.DateTime,
    nullable=False,
    default= datetime.datetime.now
  )
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


  @property
  def friendly_date(self):
    """Return formatted date"""
    # these directives, first 2 mean Weekday/Month as locale’s abbreviated name, and the third oneDay of the month as a decimal number.

    # second part %Y year without a decimal
    # %-I Hour (12-hour clock) as a decimal number. 
    # %M Month as a zero-padded decimal number.
    # %p AM or PM
    return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

# Many to many, a post can have many tags, and a tag can be associated to many posts.
# The new table PostTag will connect to Post --E PostTag. ( "--E" is a crow feet ) and Tag --E PostTag.

class PostTag(db.Model):
  """Tag on a post"""
  __tablename__ = "posts_tags"

  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)



class Tag(db.Model):
  """Tag that can be added to posts"""
  __tablename__ = 'tags'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.Text, nullable=False, unique=True)

# through relationship, many to many. The association table is indicated by the secondary argument, which will be two way as indicated by the backref paremeter.
  posts = db.relationship('Post', secondary="posts_tags", backref='tags',) 


def connect_db(app):
  """Connect this database to provided flask app.
  Call this in your flask app"""

  db.app = app
  db.init_app(app)