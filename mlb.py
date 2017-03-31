#
# Goal Light for MLB games.
# Triggers whenever a run is scored for the given team
#
from datetime import datetime
from dateutil.parser import parse
import requests
import time
import sys
from light import triggerGoalLight

API_HOST = 'https://statsapi.mlb.com';

TEAM_TO_WATCH = sys.argv[1].upper()
print 'Check for', TEAM_TO_WATCH

def checkForRunScore(link, team_position):
	gameRunning = True
	while gameRunning:
		resp = requests.get(API_HOST + link)
		data = resp.json()
		if data['gameData']['status']['abstractGameState'] == 'Final':
			gameRunning = False
			print 'Game Over'
		else:
			try:
				lastEvent = data['liveData']['plays']['currentPlay']
				if lastEvent['about']['isScoringPlay'] and lastEvent['about']['halfInning'] == team_position:
					print 'RUN SCORED', lastEvent['about']['halfInning']
					triggerGoalLight()
					# Certainly won't have another run within 90 seconds
					time.sleep(90)
				else:
					time.sleep(10)
			except:
				time.sleep(60)



def getSchedule():
	resp = requests.get(API_HOST + '/api/v1/schedule?sportId=1')
	data = resp.json()['dates']
	for date in data:
		for game in date['games']:
			team_type = None
			for x in game['teams']:
				if TEAM_TO_WATCH in game['teams']['away']['team']['name'].upper():
					team_type = x

			if team_type is not None:
				gameDate = parse(game['gameDate']).replace(tzinfo=None)
				now = datetime.utcnow()
				if(gameDate > now):
					diff = gameDate - now
					print TEAM_TO_WATCH, 'Will play today at', game['gameDate'], team_type
					print 'Delaying', diff
					time.sleep(diff.total_seconds()-60)
					# Trigger the Goal Light to let us know to start watching
					# the game...
					goalLED.on()
					time.sleep(30)
					goalLED.off()
				team_position = 'top'
				if team_type == 'home':
					team_position = 'bottom'
				print 'Checking', game['link'], team_type, team_position
				checkForRunScore(game['link'], team_position)

getSchedule()
