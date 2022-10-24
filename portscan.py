import requests
import ipcalc
import sys
import os
import threading
import time

def scan(eachTreadsIP,eachTreadsEndIP,threadNumber):
	global finishFlag
	initialPort=int(sys.argv[3])
	
	#mulitple ports
	if len(sys.argv)==5 :
		endPort=int(sys.argv[4])
		for x in range(eachTreadsIP,eachTreadsEndIP):
			fileNameUnproccessed = "IP-Address-"+str(ipAddresses[x])+"-port-scan-between-"+str(initialPort)+"-and-"+str(endPort)+"-thread-number-"+str(threadNumber+1)
			fileNameProccessed = fileNameUnproccessed.replace("/", "-")
			fileNames.append(fileNameProccessed)
			file = open(fileNameProccessed,"w")
			for y in range(initialPort,endPort):
				pload = {'port':y,'ip':ipAddresses[x],'t':'2000'}
				r = requests.post('http://ports.my-addr.com/check_port.php',data = pload)
				if r.text=='1':
					file.write("port : "+str(y)+" is open on : " + str(ipAddresses[x])+"\n")
					print("port : "+str(y)+" is open on : " + str(ipAddresses[x]))
				else:
					file.write("port : "+str(y)+" is closed on : " + str(ipAddresses[x])+"\n")
					print("port : "+str(y)+" is closed on : " + str(ipAddresses[x]))
		finishFlag=finishFlag+1
		print(finishFlag)

	
	#single port
	else :
		for x in range(eachTreadsIP,eachTreadsEndIP):
			fileNameUnproccessed = "IP-Address-"+str(ipAddresses[x])+"-port-scan-for-"+str(initialPort)+"-thread-number-"+str(threadNumber+1)
			fileNameProccessed = fileNameUnproccessed.replace("/", "-")
			fileNames.append(fileNameProccessed)
			file = open(fileNameProccessed,"w")
			pload = {'port':initialPort,'ip':ipAddresses[x],'t':'2000'}
			r = requests.post('http://ports.my-addr.com/check_port.php',data = pload)
			if r.text=='1':
				file.write("port : "+str(initialPort)+" is open on : " + str(ipAddresses[x])+"\n")
				print("port : "+str(initialPort)+" is open on : " + str(ipAddresses[x]))
			else:
				file.write("port : "+str(initialPort)+" is closed on : " + str(ipAddresses[x])+"\n")
				print("port : "+str(initialPort)+" is closed on : " + str(ipAddresses[x]))
		
		finishFlag=finishFlag+1


	
	

fileNames= []
finishFlag = 0
whileChar = 1
ipAddresses = []



if len(sys.argv) > 3 :
	if len(sys.argv)==5 :
		fileNameFinalUnproccessed = str(sys.argv[1])+"-port-scan-between-"+str(int(sys.argv[3]))+"-and-"+str(int(sys.argv[4]))+"-Final"
		fileNameFinalProccessed = fileNameFinalUnproccessed.replace("/", "-")
		finalFile = open(fileNameFinalProccessed,"w")
	else:
		fileNameFinalUnproccessed = str(sys.argv[1])+"-port-scan-for-"+str(int(sys.argv[3]))+"-Final"
		fileNameFinalProccessed = fileNameFinalUnproccessed.replace("/", "-")
		finalFile = open(fileNameFinalProccessed,"w")	

	for x in ipcalc.Network(sys.argv[1]):
		ipAddresses.append(x)


	if len(ipAddresses)<int(sys.argv[2]):
		print("The number of threads cannot exceed the number of IPs. Which is:"+str(len(ipAddresses)))
		sys.exit()

	eachThreadsIP=int(len(ipAddresses)/(int(sys.argv[2])))
	lastThreadsExtraIP=(len(ipAddresses)-(int(sys.argv[2]))*(int(len(ipAddresses)/(int(sys.argv[2])))))


	for i in range(int(sys.argv[2])+1):
		if (len(ipAddresses))>=((eachThreadsIP*(i+1)+lastThreadsExtraIP+1)):
			worker = threading.Thread(target=scan,args=((eachThreadsIP*i),(eachThreadsIP*(i+1)),i))
			worker.start()
		else :
			worker = threading.Thread(target=scan,args=((eachThreadsIP*i),((eachThreadsIP*(i+1))+lastThreadsExtraIP),i))
			worker.start()
			break


	#dosyaların üzerinde gezip tek dosyaya yazma
	while whileChar==1:
		if finishFlag == (int(sys.argv[2])):
			for k in fileNames:
				print("-----------")
				print(str(k))
				file = open(k,'r')
				lines = file.readlines()
				count=0
				for line in lines:
					count += 1
					finalFile.write(line.strip())
				os.remove(k)
			whileChar=0
			break
else:
	print("Usage for single port: python3 portscan.py <IP Subnet> <Thread Number> <Port>")
	print("Usage for port range: python3 portscan.py <IP Subnet> <Thread Number> <Starting Port> <End Port>")
			

		
