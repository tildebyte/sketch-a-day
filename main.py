import os
import random
import datetime as dt

import yaml
import webapp2
import cloudstorage as gcs

from google.appengine.api import app_identity as ai

top = '''
<!DOCTYPE html>
<html>

    <head>
        <link rel="stylesheet" type="text/css" href="https://fonts.googleapis.com/css?family=Fira+Sans:300|Source+Serif+Pro">
        <style>
            * {
                box-sizing: border-box;
                text-align: center;
                border-radius: 5px;
                margin: auto;
                padding: 5px;
                color: hsl(36, 100%, 98%);
            }

            body {
                font-family: 'Fira Sans', sans-serif;
                font-family: 'Source Serif Pro', serif;
                background-color: hsl(38, 42%, 12%);
            }

            #title-box {
                color: hsl(39, 23%, 53%);
                font-family: sans-serif;
                font-size: 66px;
            }

            #text-box {
                background-color: hsl(39, 66%, 35%);
                width: 90%;
                font-size: 32px;
            }

            p {
                width: 80%;
                font-family: serif;
            }

            #highlight {
                background-color: hsl(39, 23%, 53%);
            }

            #highlight-date {
                color: hsl(39, 23%, 68%);
            }
        </style>
    </head>

    <body>
        <div id="title-box">Sketch-a-Day</div>
        <div id="text-box">
'''

bottom = '''
        </div>

    </body>

</html>
'''

default_retry_parms = gcs.RetryParams(initial_delay=0.2,
                                      max_delay=5.0,
                                      backoff_factor=2,
                                      max_retry_period=15)
gcs.set_default_retry_params(default_retry_parms)


class MainPage(webapp2.RequestHandler):

    def read_file(self, filename):
        with gcs.open(filename, mode='r') as gcs_file:
            return yaml.safe_load(gcs_file)

    def write_file(self, filename, stream):
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        with gcs.open(filename, 'w',
                      content_type='text/plain',
                      retry_params=write_retry_params) as gcs_file:
            gcs_file.write(stream)

    def do_it(self, filename):
        self.data = self.read_file(filename)
        if (self.today - self.data['current_date']):
            self.data['current_date'] = self.today
            prompts_list = [
                prompt for prompt in self.data['prompts'] if self.data['prompts'][prompt]
            ]
            self.data['current_prompt'] = random.choice(prompts_list)
            self.data['current_tool'] = random.choice(self.data['tools'])
            self.data['prompts'][self.data['current_prompt']] = False
            self.write_file(filename, yaml.safe_dump(self.data))

    def get(self):
        bucket_name = os.environ.get('BUCKET_NAME',
                                     ai.get_default_gcs_bucket_name())
        bucket = '/' + bucket_name
        filename = bucket + '/data.yaml'
        self.today = dt.date.today()
        self.do_it(filename)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(top)
        self.response.write('<p>Prompt for <span id="highlight-date">{0}</span>: <span id="highlight">{1}</span>, using <span id="highlight">{2}</span>.</p>'.format(
            self.today, self.data['current_prompt'], self.data['current_tool']))
        self.response.write(bottom)


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
