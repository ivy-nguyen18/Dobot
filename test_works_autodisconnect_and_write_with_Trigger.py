#Magic Box+Magician Lite
import threading
import os
import os.path
from os import path
from datetime import datetime, timezone

dType.SetQueuedCmdClear(api)
dType.SetQueuedCmdStopExec(api)
dType.SetQueuedCmdStartExec(api)
speed2 = None
speed1 = None
flag = 0


#Led blinks three times using output EIO06
def signal():
	dType.SetIOMultiplexingExtEx(api, 6, 1, 1)
	for count2 in range(3):
		dType.SetIODOExtEx(api, 6, 1, 1)
		print('eio06 ON')
		dType.dSleep(500)
		dType.SetIODOExtEx(api, 6, 0, 1)
		print('eio06 OFF')
		dType.dSleep(500)

def testSignal():
	dType.SetIOMultiplexingExtEx(api, 6, 1, 1)
	while (True):
		dType.SetIODOExtEx(api, 6, 1, 1)
		dType.SetIODOExtEx(api, 6, 0, 1)

def on():
	dType.SetIOMultiplexingExtEx(api, 6, 1, 1)
	dType.SetIODOExtEx(api, 6, 1, 1)

def off():
	dType.SetIODOExtEx(api, 6, 0, 1)


def getPoints():
	#change file name per run (otherwise, it will be overwritten)
	file = open("filename.txt", "w")
	print(os.path.dirname(os.path.abspath("filename.txt")))
	headers = "time(ms)\t trigger\t\t x\t\t y\t\t z\n\n"
	file.write(headers)
	
	while(flag == 0):
		#get time
		utc_dt = datetime.now(timezone.utc) # UTC time
		timeMS = utc_dt.astimezone().strftime('%H:%M:%S.%f')[:-3]

		#format data
		txt = "{:<10}"
		data = timeMS + "\t" + str(dType.GetIODOExt(api,6)) + "\t" + txt.format(dType.GetPoseEx(api,1)) + "\t" + txt.format(dType.GetPoseEx(api,2)) + "\t" + txt.format(dType.GetPoseEx(api,3)) + "\n"

		#write to file
		file.write(data)

		#save the file after each time it is written ( f.close not needed)
		file.flush()
		os.fsync(file.fileno())

def movementFunc():
	def setPenPosition():
		dType.SetPTPCmdEx(api, 0, 226.3027, 0, (-38.5), 0, 1)

	def move():
		global speed2
		for count in range(1):
			dType.SetArmSpeedRatioEx(api, 1, 100, 1)
			dType.SetPTPCmdEx(api, 7, 0,  5,  0, 0, 1)
			dType.SetPTPCmdEx(api, 7, 0,  (-5),  0, 0, 1)
			dType.dSleep(2000)
			speed2 = dType.GetArmSpeedRatio(api, 1)[0]
		off()
	def move2():
		global speed1
		for count2 in range(1):
			dType.SetArmSpeedRatioEx(api, 1, 100, 1)
			dType.SetPTPCmdEx(api, 7, 5,  0,  0, 0, 1)
			dType.SetPTPCmdEx(api, 7, (-5),  0,  0, 0, 1)
			dType.dSleep(2000)
			speed1 = dType.GetArmSpeedRatio(api, 1)[0]
	
	setPenPosition()
	move()
	move2()

	#End Signal -> turns LED off
	off()
	dType.DisconnectDobot(api)

#Start Signal -> turns LED on
off()
#Threading
t1 = threading.Thread(target = getPoints)
t2 = threading.Thread(target = movementFunc)
t3 = threading.Thread(target = testSignal)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()


#dType.RestartMagicBox(api)
#dType.DisconnectDobot(api)