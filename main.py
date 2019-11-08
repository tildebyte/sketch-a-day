# [START gae_python37_app]
import datetime as dt
import random
import os

import yaml

from flask import Flask
from google.cloud import storage

import sketchadayhtml

from google.appengine.api import app_identity as ai

gcsc = storage.Client()


app = Flask(__name__)


@app.route('/')
def main():

    def read_file(self, filename):
        with gcsc.open(filename, mode='r') as gcsc_file:
            return yaml.safe_load(gcsc_file)

    def write_file(self, filename, stream):
        write_retry_params = gcsc.RetryParams(backoff_factor=1.1)
        with gcsc.open(filename, 'w',
                       content_type='text/plain',
                       retry_params=write_retry_params) as gcsc_file:
            gcsc_file.write(stream)

    def read_files(self, datafilename, historyfilename, galleryfilename):
        self.promptdata = self.read_file(datafilename)
        self.historydata = self.read_file(historyfilename)
        with open(galleryfilename, mode='r') as stream:
            self.gallerydata = yaml.safe_load(stream)

    def do_it(self, datafilename, historyfilename, galleryfilename):
        self.read_files(datafilename, historyfilename, galleryfilename)
        self.existing_date = self.promptdata['existing_date']
        self.existing_prompt = self.promptdata['existing_prompt']
        self.existing_tool = self.promptdata['existing_tool']
        self.history = self.historydata['history']
        if (self.today - self.existing_date):
            self.prompts = self.promptdata['prompts']
            self.tools = self.promptdata['tools']

            # Stash yesterday. We don't much care about the tool.
            self.history[self.existing_date] = self.existing_prompt
            promptslist = [
                prompt for prompt in self.prompts if self.prompts[prompt]
            ]
            self.todayprompt = random.choice(promptslist)
            self.todaytool = random.choice(self.tools)
            self.prompts[self.todayprompt] = False
            self.promptdata['existing_date'] = self.today
            self.promptdata['existing_prompt'] = self.todayprompt
            self.promptdata['existing_tool'] = self.todaytool
            self.historydata['history'] = self.history
            self.write_file(datafilename, yaml.safe_dump(self.promptdata))
            self.write_file(historyfilename, yaml.safe_dump(self.historydata))

    def build_gallery(self):
        self.galleryhtml = ''
        for item in self.gallerydata['galleryitems']:
            self.galleryhtml += '''
            <div class="item">
                <a href="{0}" target="_blank">
                    <p>{1}</p>
                </a>
            </div>'''.format(item['url'], item['caption'])

    def build_history(self):
        self.historyhtml = '<ul>'
        for item in sorted(self.history, reverse=True):
            self.historyhtml += f'<li>{item}&mdash;{self.history[item]}</li>\n'
        self.historyhtml += '</ul>'

    def get(self):
        bucket_name = os.environ.get('BUCKET_NAME',
                                     ai.get_default_gcs_bucket_name())
        bucket = '/' + bucket_name
        datafilename = bucket + '/data.yaml'
        historyfilename = bucket + '/history.yaml'
        galleryfilename = 'static/gallery_items.yaml'
        self.today = dt.date.today()
        self.do_it(datafilename, historyfilename, galleryfilename)
        self.build_gallery()
        self.build_history()
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(sketchadayhtml.htmltext.format(self.existing_date,
                                                           self.existing_prompt,
                                                           self.existing_tool,
                                                           self.galleryhtml,
                                                           self.historyhtml))


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
