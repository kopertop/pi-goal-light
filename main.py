from datetime import datetime
from dateutil.parser import parse
import requests
import time
import sys
from light import triggerGoalLight
API_ROOT = 'https://statsapi.web.nhl.com'

TEAM_TO_WATCH = sys.argv[1].upper()
print 'Check for', TEAM_TO_WATCH

def checkForGoal(link):
	gameRunning = True
	while gameRunning:
		resp = requests.get(API_ROOT + link)
		data = resp.json()
		if data['gameData']['status']['abstractGameState'] == 'Final':
			gameRunning = False
			print 'Game Over'
		else:
			try:
				lastEvent = data['liveData']['plays']['currentPlay']
				if lastEvent['result']['eventTypeId'] == 'GOAL':
					print 'GOAL', lastEvent['team']['triCode']
					if lastEvent['team']['name'].strip().upper() == TEAM_TO_WATCH:
						triggerGoalLight()
					else:
						print 'BAD GOAL!', lastEvent['team']['triCode']
					# Probably not going to have another goal within a minute
					time.sleep(60)
				else:
					print 'No goal', lastEvent['result']['eventTypeId'], lastEvent['team']['triCode']
					time.sleep(10)
			except:
				time.sleep(60)

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
					print TEAM_TO_WATCH, 'Will play today at', game['gameDate']
					print 'Delaying', diff
					time.sleep(diff.total_seconds()-60)
					# Trigger the Goal Light to let us know to start watching
					# the game...
					triggerGoalLight(30)
				checkForGoal(game['link'])
			else:
				print 'Ignore', team_names, game['gameDate']

getSchedule()
