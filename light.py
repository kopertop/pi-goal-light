# Shared Goal Light resources
from gpiozero import LED
goalLED = LED(17)

def triggerGoalLight():
	print '!!!!!!!!!!!GOAL!!!!!!!!'
	goalLED.on()
	time.sleep(30)
	goalLED.off()
	# Probably not going to have another goal within a minute of
	# the last one
	time.sleep(60)
