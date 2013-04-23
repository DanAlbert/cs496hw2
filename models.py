from google.appengine.ext import db
from google.appengine.api import users


class University(db.Model):
    name = db.StringProperty("Name of the university")
    image_url = db.StringProperty("Image to diplay for this univeristy")
    post_time = db.DateTimeProperty("Date and time this was posted",
                                    auto_now_add=True)
