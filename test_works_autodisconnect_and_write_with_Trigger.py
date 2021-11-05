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
		dType.SetPTPCmdEx(api, 2, 270, 0, (-80.5), 0, 1)
		#dType.SetPTPCmdEx(api, 2, 226.3025, 0, (-38.5), 0, 1)
		dType.SetARCParams(api,100,100,100,100)

	def move(x, y, z, r, changeX, changeY, changeZ, changeR, J1, changeJ1):    # xyzr for Cartesian coordinate system, J for joint coordinate system
		global speed2
		currentPosition = dType.GetPose(api)
		for count in range(4):                                 
			dType.SetArmSpeedRatioEx(api, 1, 100, 1)
			if (J1 != 0):                                    
				dType.SetPTPCmdEx(api, 4, currentPosition[4] + J1,  currentPosition[5],  currentPosition[6], currentPosition[7], 1)        # mode 4, joint mode in joint coordinate system    
				dType.SetPTPCmdEx(api, 4, currentPosition[4] + changeJ1,  currentPosition[5],  currentPosition[6], currentPosition[7], 1)
			else:
				dType.SetPTPCmdEx(api, 7, x,  y,  z, r, 1)                                                                                 # mode 7, linear mode in Cartesian coordinate system
				dType.SetPTPCmdEx(api, 7, changeX, changeY,  changeZ, changeR, 1)
			dType.dSleep(1000)
			speed2 = dType.GetArmSpeedRatio(api, 1)[0]
	def wait(waitTime):                                      
		global speed2
		for count2 in range(1):
			dType.SetArmSpeedRatioEx(api, 1, 100, 1)
			dType.SetPTPCmdEx(api, 7, 0,  0,  0, 0, 1)
			dType.SetPTPCmdEx(api, 7, 0,  0,  0, 0, 1)
			dType.dSleep(waitTime)
			speed1 = dType.GetArmSpeedRatio(api, 1)[0]
		off()

	def setMove():                                                        
		#move( x, y, z, r, change in x, change in Y, change in Z, J1, change in J1)
	
		move(20,0,0,0, -20,0,0,0, 0,0) # move on X axis
		move(0,0,0,0, 0,0,0,0, 20,-20) # rotate Joint1, around Z axis
		setPenPosition() #Reset pen position 

		#Test movement starts here
		move(1,0,0,0, -1,0,0,0, 0,0) #move on X by 1
		move(3,0,0,0, -3,0,0,0, 0,0) #move on X by 3
		move(5,0,0,0, -5,0,0,0, 0,0) #move on X by 5
		
		move(0,1,0,0, 0,-1,0,0, 0,0) #move on Y by 1
		move(0,3,0,0, 0,-3,0,0, 0,0) #move on Y by 3
		move(0,5,0,0, 0,-5,0,0, 0,0) #move on Y by 5

		move(0,0,1,0, 0,0,-1,0, 0,0) #move on Z by 1
		move(0,0,3,0, 0,0,-3,0, 0,0) #move on Z by 3
		move(0,0,5,0, 0,0,-5,0, 0,0) #move on Z by 5

		move(0,0,0,0, 0,0,0,0, 1,-1) # rotate Joint1 by 1°
		move(0,0,0,0, 0,0,0,0, 3,-3) # rotate Joint1 by 3°
		move(0,0,0,0, 0,0,0,0, 5,-5) # rotate Joint1 by 5°
	
	setPenPosition()
	wait(25000)
	setMove()
	wait(35000)
	
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