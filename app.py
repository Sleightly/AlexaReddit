from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/reddit")

def get_subreddits(text):
	with open('config.json') as f:
		user_pass = json.load(f)
	sess = requests.Session()
	sess.headers.update({'User-Agent': 'Alexa Test: Sleightly_'})
	sess.post('https://www.reddit.com/api/login', data=user_pass)
	time.sleep(1)

	sub = 'jokes'
	if text == '':
		print('failed')
		text = sub
	
	url = 'https://reddit.com/r/'+text+'/.json?limit=3'
	html = sess.get(url)
	data = json.loads(html.content.decode('utf-8'))
	titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']][1:]
	bodies = [unidecode.unidecode(listing['data']['selftext']) for listing in data['data']['children']][1:]
	response = ''
	for i, j in zip(titles, bodies):
		response += i + '... ...' + j + '... ... ... ... next ... ...'
	response = response[:-16]
	return 'reading subreddit '+ text+ "... ... ... " + response

titles = get_subreddits('')

@app.route('/')
def home():
	return 'Substitute homepage'

@ask.launch
def init_skill():
	hello_msg = 'Opening Reddit, which sub reddit would you like to read?'
	return question(hello_msg)

#@ask.launch
@ask.intent('CommandIntent')
def read_any_subreddit(command):
	command = command.strip()
	print("subreddit: "+command)
	subreddits = get_subreddits(command)
	sub_reddit_msg = 'The found subreddits are {}'.format(subreddits)
	return statement(sub_reddit_msg)


@ask.intent("YesIntent")
def read_subreddits():
	print('here')
	subreddits = get_subreddits('')
	sub_reddit_msg = 'The found subreddits are {}'.format(subreddits)
	return statement(sub_reddit_msg)

@ask.intent("NoIntent")
def stop_action():
	bye = "Okay... bye"
	return statement(bye)


if __name__ == '__main__':
	app.run(debug=True)
