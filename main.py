from datetime import datetime
from dateutil.parser import parse
import requests
import time

game_id = '2016021117'

API_ROOT = 'https://statsapi.web.nhl.com'

#TEAM_TO_WATCH = 'COLUMBUS BLUE JACKETS'
TEAM_TO_WATCH = 'CHICAGO BLACKHAWKS'

def triggerGoalLight():
	print '!!!!!!!!!!!GOAL!!!!!!!!'
	time.sleep(10)
	print 'Light Off'

def checkForGoal(link):
	gameRunning = True
	while gameRunning:
		resp = requests.get(API_ROOT + link)
		data = resp.json()
		if data['gameData']['status']['abstractGameState'] == 'Final':
			gameRunning = False
			print 'Game Over'
		else:
			lastEvent = data['liveData']['plays']['currentPlay']
			if lastEvent['result']['eventTypeId'] == 'GOAL':
				print 'GOAL', lastEvent['team']['triCode']
				triggerGoalLight()
			else:
				print 'No goal', lastEvent['result']['eventTypeId']
				time.sleep(10)

def getSchedule():
	resp = requests.get(API_ROOT + '/api/v1/schedule')
	data = resp.json()['dates']
	for date in data:
		for game in date['games']:
			team_names = [
				game['teams']['away']['team']['name'].upper().strip(),
				game['teams']['home']['team']['name'].upper().strip(),
			]
			if TEAM_TO_WATCH in team_names:
				print 'Track Game', game, game['gameDate']
				gameDate = parse(game['gameDate']).replace(tzinfo=None)
				now = datetime.utcnow()
				if(gameDate > now):
					diff = gameDate - now
					time.sleep(diff)
				checkForGoal(game['link'])
			else:
				print 'Ignore', team_names, game['gameDate']

getSchedule()
