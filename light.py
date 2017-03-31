# Shared Goal Light resources
import time
from gpiozero import LED
goalLED = LED(17)

def triggerGoalLight():
	goalLED.on()
	time.sleep(30)
	goalLED.off()
