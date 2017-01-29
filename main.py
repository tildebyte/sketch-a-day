import os
import random
import datetime as dt

import yaml
import webapp2
import cloudstorage as gcs

import sketchadayhtml

from google.appengine.api import app_identity as ai

default_retry_parms = gcs.RetryParams(initial_delay=0.2,
                                      max_delay=5.0,
                                      backoff_factor=2,
                                      max_retry_period=15)
gcs.set_default_retry_params(default_retry_parms)


class MainPage(webapp2.RequestHandler):

    def readfile(self, filename):
        with gcs.open(filename, mode='r') as gcs_file:
            return yaml.safe_load(gcs_file)

    def writefile(self, filename, stream):
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        with gcs.open(filename, 'w',
                      content_type='text/plain',
                      retry_params=write_retry_params) as gcs_file:
            gcs_file.write(stream)

    def do_it(self, datafilename, historyfilename):
        self.promptdata = self.readfile(datafilename)
        self.historydata = self.readfile(historyfilename)
        self.existing_date = self.promptdata['existing_date']
        self.existing_prompt = self.promptdata['existing_prompt']
        self.existing_tool = self.promptdata['existing_tool']
        self.history = self.historydata['history']
        if (self.today - self.existing_date):
            self.prompts = self.promptdata['prompts']
            self.tools = self.promptdata['tools']
            
            # Stash yesterday. We don't much care about the tool.
            self.history[self.existing_date] = self.existing_prompt
            self.existing_date = self.today
            promptslist = [
                prompt for prompt in self.prompts if self.prompts[prompt]
            ]
            self.todayprompt = random.choice(promptslist)
            self.todaytool = random.choice(self.tools)
            self.prompts[self.todayprompt] = False
            self.writefile(datafilename, yaml.safe_dump(self.promptdata))
            self.writefile(hitoryfile, yaml.safe_dump(self.history))

    def get(self):
        bucket_name = os.environ.get('BUCKET_NAME',
                                     ai.get_default_gcs_bucket_name())
        bucket = '/' + bucket_name
        datafilename = bucket + '/data.yaml'
        historyfilename = bucket + '/history.yaml'
        self.today = dt.date.today()
        self.do_it(datafilename, historyfilename)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(sketchadayhtml.htmltext.format(self.existing_date, self.existing_prompt, self.existing_tool))
        # write history
        self.response.write('<ul>')
        for item in sorted(self.history, reverse=True):
            self.response.write('<li>{0} &mdash; {1}</li>'.format(item, self.history[item]))
        self.response.write('</ul>')

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
