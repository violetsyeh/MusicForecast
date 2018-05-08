"""Models and database for Flask app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#####################################################################
# Model definitions

class User(db.Model):
    """Users of website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)
    fname = db.Column(db.String(64), nullable=True)
    lname = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Return user info"""

        return "< User user_id={} email={} zipcode={} >".format(self.user_id, self.email,
                                                            self.zipcode, self.city)

class Playlist(db.Model):
    """Playlists from website"""

    __tablename__ = "playlists"

    playlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    uri = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    user = db.relationship("User", backref=db.backref("playlists"))

    def __repr__(self):
        """Return playlist info."""

        return "< Playlist playlist_id={} user_id={} uri={} name{} >".format(
                    self.playlist_id, self.user_id, self.uri, self.name)



def connect_to_db(app):
    """Connect database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///weather'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
