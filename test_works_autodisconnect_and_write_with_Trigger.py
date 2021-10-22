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

#getting input signal
def button():
	dType.SetIOMultiplexingExtEx(api, 10, 3, 1);

#sending output signal
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
	file = open("filename1.txt", "w")
	print(os.path.dirname(os.path.abspath("filename.txt")))
	headers = "time(ms)\ttrigger\tinput\tx\t\ty\t\t\tz\n\n"
	file.write(headers)
	
	while(flag == 0):
		#get time
		utc_dt = datetime.now(timezone.utc) # UTC time
		timeMS = utc_dt.astimezone().strftime('%H:%M:%S.%f')[:-3]

		#format data
		txt = "{:<10}"
		data = timeMS + "\t" + str(dType.GetIODOExt(api,6)) + "\t" + str(dType.GetIODIExt(api,10)[0]) + "\t" +  txt.format(dType.GetPoseEx(api,1)) + "\t" + txt.format(dType.GetPoseEx(api,2)) + "\t" + txt.format(dType.GetPoseEx(api,3)) + "\n"

		#write to file
		file.write(data)

		#save the file after each time it is written ( f.close not needed)
		file.flush()
		os.fsync(file.fileno())

def movementFunc():
	def setPenPosition():
		dType.SetPTPCmdEx(api, 0, 226.3027, 0, (-38.5), 0, 1)
		dType.SetARCParams(api,100,100,100,100)

	def move(x, y, z, r, changeX, changeY, changeZ, changeR):
		global speed2
		currentPosition = dType.GetPose(api)
		print(currentPosition[0])
		for count in range(4):
			dType.SetArmSpeedRatioEx(api, 1, 100, 1)
			if (y != 0) and (changeY != 0) :
				dType.SetPTPCmdEx(api, 4, currentPosition[4] + y,  currentPosition[5],  currentPosition[6], currentPosition[7], 1)
				dType.SetPTPCmdEx(api, 4, currentPosition[4] + changeY,  currentPosition[5],  currentPosition[6], currentPosition[7], 1)
			else:
				dType.SetPTPCmdEx(api, 7, x,  y,  z, r, 1)
				dType.SetPTPCmdEx(api, 7, changeX, changeY,  changeZ, changeR, 1)
			dType.dSleep(1000)
			speed2 = dType.GetArmSpeedRatio(api, 1)[0]
		off()

	def setMove():
		#move( x, y, z, r, change in x, change in Y, change in Z)
		move(20,0,0,0, -20,0,0,0)
		move(0,20,0,0, 0,-20,0,0)
	
	setPenPosition()
	setMove()

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
