from movie_app import db


class Movie_model(db.Model):
    __tablename__ = "movie_model"

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    moviename = db.Column(db.VARCHAR(64), nullable=False)
    year = db.Column(db.Integer(), nullable=True)
    rating = db.Column(db.Integer(), nullable=True)
    genre = db.Column(db.VARCHAR(128), nullable=False)
    summary = db.Column(db.VARCHAR(400), nullable=False)
    like_id = db.Column(db.Integer(), db.ForeignKey("likelist.id"), nullable=True)

    def __repr__(self):
        return f"Movie_model {self.id}"


class Likelist(db.Model):
    __tablename__ = "likelist"

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    moviename = db.Column(db.VARCHAR(64), nullable=False)
    likemovie = db.relationship(
        "Movie_model", backref="likelist", lazy="subquery", cascade="all,delete"
    )

    def __repr__(self):
        return f"Likelist {self.id}"