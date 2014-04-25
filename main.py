import webapp2

from webfront.basePage import BaseHandler,JINJA_ENVIRONMENT

class MainPage(BaseHandler):

    def get(self):
        template_values = {
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))




app = webapp2.WSGIApplication([
  ('/', MainPage)
])