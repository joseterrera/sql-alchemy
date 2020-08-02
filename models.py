"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://picsum.photos/200/300"

class User(db.Model):
  """Site User"""
  """Better reoresentation:"""
  def __repr__(self):
      """Show info about pet."""

      p = self
      return f"<User {p.id} {p.first_name} {p.last_name} {p.image_url}>"

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key = True)
  first_name = db.Column(db.Text, nullable=False)
  last_name = db.Column(db.Text, nullable=False)
  image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

# decorator @property
  @property
  def full_name(self):
    """Return full name of user"""
    return f"( {self.first_name} {self.last_name} )"


def connect_db(app):
  """Connect this database to provided flask app.
  Call this in your flask app"""

  db.app = app
  db.init_app(app)