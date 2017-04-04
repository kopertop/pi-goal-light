# Shared Goal Light resources
import time
from gpiozero import LED
goalLED = LED(17)

def triggerGoalLight(onTime=15):
	goalLED.on()
	time.sleep(onTime)
	goalLED.off()
