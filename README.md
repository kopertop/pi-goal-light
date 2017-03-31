# Raspberry Pi Goal Light
This simple script is designed to help you turn a Raspberry Pi into an automated Goal Light. Automatically light up a Goal Light in your own Man Cave every time your favorite NHL team scores.

This uses a reverse-engineered API from NHL.com. The same API they use for their mobile apps can be pingged to determine when games start, as well as when a team scores a goal.

Fortunately this is also the same API that runs MLB.com, (MLBAM), so this also works for MLB games. There's a slight modification here, so a separate script mlb.py is provided to check for runs scored in any MLB game.

The idea of this script is to trigger a GPIO port every time we detect a GOAL event from a given team.

# Usage
On a raspberry Pi (I used a Zero W), run:

```
python main.py "columbus blue jackets"
```

You can replace any team name as the first argument. Whenever that team scores, GPIO port 17 will be enabled.

If the provided team is not playing yet today, it will delay until 60 seconds before faceoff, then trigger the Goal Light to let you know the game is about to start.

Once the game has started, the script will ping the NHL.com API every 10 seconds looking for a GOAL event. If it matches your team, it will trigger GPIO port 17 for 30 seconds, then wait 60 seconds before trying again. Note that in some cases duplicate goal events may be received because the NHL.com API is slow and quite crappy. This also may mean that there will be a delay, sometimes as long as a minute, from the time between when the goal is scored and the light can be triggered.

For MLB Support use:
```
python mlb.py "cleveland indians"
```

# Setting Up

## Hardware
This script is designed to run on a Raspberry Pi, with Python, python-dateutil, and gpiozero which is installed by default in the latest version of Raspian. I recommend the following hardware:

* Raspberry Pi Zero W (I picked one up from Microcenter)
* Controllable Four Outlet Power Relay Module (https://www.adafruit.com/products/2935)
* Novelty 7" Police Beacon (https://www.amazon.com/gp/product/B0011CZV5A/)
* Micro SD Card with Raspbian Installed (I recommend Raspian Light since you don't want any GUI)

I also purchased a simple $5 case for my Pi Zero W, and had some left over wires from an old Cannakit that was designed for a Raspberry Pi Model B+. Any control wires will work, however, as they need to be soldered onto the Zero W. You can also use a Hammer Header or other solderless solution instead, or even purchase a Raspberry Pi 3 so you don't have to do any soldering at all.

Install the SD Card with Raspian Light, and configure wireless.

## Software

Clone this repository or just download the main.py file to your Raspberry Pi. Run it with the team name when you want it to check, or set up a cron tab to check daily.
