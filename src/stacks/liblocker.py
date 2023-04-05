#!/usr/bin/env python3
import os,sys,re
import subprocess
import psutil
import json,time
import multiprocessing

class softlocker():
	def __init__(self):
		self.status=False
		self.dbg=False
		self.enforced=[]
		multiprocessing.set_start_method('fork')
		self.watchdogLaunchDelay=60
		self.aaFile="/etc/apparmor.d/security.profile"
	#def _init__

	def _debug(self,msg):
		if self.dbg==True:
			print("{}".format(msg))
	#def _debug

	def setTimeout(self,timeout):
		self.watchdogLaunchDelay=timeout
	#def setTimeout

	def getStatus(self):
		jout={}
		status=False
		cmd=["/usr/sbin/aa-status","--json"]
		proc=subprocess.run(cmd,capture_output=True,universal_newlines=True)
		out=proc.stdout
		if len(out)>0:
			jout=json.loads(out)
		if len(jout)>0:
			if jout.get("profiles",{}).get("/usr/bin/apt","").lower()=="enforce":
				status=True
		return(status)
	#def getStatus

	def _getManagedProfiles(self):
		profiles=[]
		profileDir="/usr/share/software-unlocker/profiles.d"
		if os.path.isdir(profileDir)==True:
			for profile in os.listdir(profileDir):
				fcontents=[]
				self._debug("Reading {}".format(profile))
				try:
					with open (os.path.join(profileDir,profile)) as f:
						fcontents=f.readlines()
				except Exception as e:
					self._debug("{0}: {1}".format(profile,e))
					continue
				if len(fcontents)>0:
					profiles.extend(fcontents)

		return(profiles)
	#def _getManagedProfiles

	def _generateAAProfile(self):
		fcontent=["#include <tunables/global>\n"]
		includedProfiles=self._getManagedProfiles()
		fcontent.extend(includedProfiles)
		with open (self.aaFile,"w") as f:
			f.writelines(fcontent)
	#def _generateAAProfile

	def setStatus(self,enforce=True,apps=[]):
		apps=[]
		if enforce==self.getStatus():
			return()
		if enforce==True:
			self._generateAAProfile()
			cmd=["/usr/sbin/aa-enforce","security.profile"]
		else:
			if os.path.isfile(self.aaFile)==False:
				self._generateAAProfile()
			cmd=["/usr/sbin/aa-disable","security.profile"]
		proc=subprocess.run(cmd,capture_output=True,universal_newlines=True)
		self.setPolkitStatus(status=enforce)
		if enforce==False:
			self.setLock()
	#def setStatus

	def setPolkitStatus(self,status=True):
		configDir="/usr/share/software-unlocker/polkit/"
		polkitDir="/etc/polkit-1/localauthority"
		actionsDir="/usr/share/polkit-1"
		for d in os.listdir(configDir):
			if os.path.isdir(os.path.join(polkitDir,d))==False:
				os.makedirs(os.path.join(polkitDir,d))
			for fconf in os.listdir(os.path.join(configDir,d)):
				if status:
					wrkf=os.path.join(configDir,d,fconf)
					with open(wrkf,'r') as f:
						fcontent=f.read()
					if d=="actions":
						dstf=os.path.join(actionsDir,d,fconf)
					else:
						dstf=os.path.join(polkitDir,d,fconf)
					with open(dstf,'w') as f:
						f.write(fcontent)
				else:
					if d=="actions":
						dstf=os.path.join(actionsDir,d,fconf)
					else:
						dstf=os.path.join(polkitDir,d,fconf)
					if os.path.isfile(dstf):
						os.unlink(dstf)
	#def setPolkitStatus


	def unlockApt(self,enforce=True):
		self.setStatus(enforce=enforce,apps=apps)
	#def unlockApt

	def setLock(self):
		subprocess.Popen(['/usr/share/software-unlocker/watchlock.py',"{}".format(self.watchdogLaunchDelay)],close_fds=True,start_new_session=True)
	#def setLock
