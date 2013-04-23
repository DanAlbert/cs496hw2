import webapp2

from google.appengine.api import users
from google.appengine.ext import db

import jinja2

from datetime import datetime, timedelta
import json
import logging
import os
import urllib2

import settings

from models import University

jinja = jinja2.Environment(
            loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIR))


class RequestHandler(webapp2.RequestHandler):
    """Base request handler that handles site wide handling tasks."""
    def render(self, template_name, data={}):
        """Renders the template in the site wide manner.
        
        Merges template data with template helper methods to the view and
        renders the template. Templates are retrieved from the template
        directory specified in the settings and appended with the suffix
        ".html"
        
        Arguments:
        template_name: the name of the template. this is the file name of the
                       template without the .html extension.

        data: a dictionary containing data to be passed to the template.
        """
        data['uri_for'] = webapp2.uri_for
        
        template = jinja.get_template(template_name + '.html')
        return self.response.out.write(template.render(data))


class UniversityListHandler(RequestHandler):
    def get(self):
        return self.render('university-list')


class UniversityCleanHandler(webapp2.RequestHandler):
    def get(self):
        for university in University.all():
            if university.post_time < datetime.now() - timedelta(minutes=5):
                university.delete()


class JsonUniversityListHandler(RequestHandler):
    def get(self):
        universities = []
        for university in University.all().order('-post_time'):
            universities.append({
                'name': university.name,
                'image_url': university.image_url,
            })
        self.response.out.write(json.dumps(universities))

    def post(self):
        form = json.loads(self.request.get('form'))
        name = form['name']
        image_url = form['image-url']
        University(name=name, image_url=image_url).put()


app = webapp2.WSGIApplication([
    ('/', UniversityListHandler),
    webapp2.Route(r'/university', name='university-list',
                  handler=UniversityListHandler, methods=['GET']),
    webapp2.Route(r'/university/clean', name='unversity-clean',
                  handler=UniversityCleanHandler, methods=['GET']),
    webapp2.Route(r'/json/university', name='json-university-list',
                  handler=JsonUniversityListHandler, methods=['GET', 'POST']),
], debug=True)
