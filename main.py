import random
from datetime import date

import yaml
import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        today = date.today()
        with open('data.yaml', mode='r') as stream:
            data = yaml.safe_load(stream)
        if (today - data['current_date']):
            data['current_date'] = today
            prompts_list = [prompt
                            for prompt in data['prompts']
                            if data['prompts'][prompt]]
            data['current_prompt'] = random.choice(prompts_list)
            data['current_tool'] = random.choice(data['tools'])
            data['prompts'][data['current_prompt']] = False
            with open('data.yaml', mode='w') as stream:
                stream.write(yaml.safe_dump(data))
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Prompt for {0}: {1}, using {2}.'.format(today, data['current_prompt'], data['current_tool']))


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
