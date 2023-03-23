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
		self.watchdogLaunchDelay=10
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
		#systemApps=self._getSystemApps()
		fcontent=["#include <tunables/global>\n"]
		#seen=[]
		#for key,kapp in systemApps.items():
		#	for app in kapp:
		#		if app in seen:
		#			continue
		#		seen.append(app)
		#		cmd="profile %s {\n"%(app)
		#		cmd+="  audit deny %s mr,\n"%(app)
		#		cmd+="}\n"
		#		fcontent.append(cmd)
		includedProfiles=self._getManagedProfiles()
		fcontent.extend(includedProfiles)
		with open (self.aaFile,"w") as f:
			f.writelines(fcontent)
	#def _generateAAProfile

	def _getSystemApps(self):
		apps={"apt":[],"dpkg":[],"pkcon":[],"flatpak":[]}
		#envDirs=os.environ.get("PATH","/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/sbin:/usr/sbin").split(":")
		#for envDir in envDirs:
		#	if os.path.isdir(envDir)==False:
		#		continue
		#	pathApps=os.listdir(envDir)
		#	for app in apps.keys():
		#		for pathApp in pathApps:
		#			if "/{}".format(app) in "/{}".format(pathApp):
		#				if "dpkg-unlocker" in pathApp:
		#					continue
		#				apps[app].append(os.path.join(envDir,pathApp))
		return(apps)
	#def _getSystemApps

	def _getApps(self,appsFilter=[]):
		apps=[]
		self._generateAAProfile()
		profileDir="/usr/share/software-unlocker/profiles.d"
		if os.path.isdir(profileDir)==True:
			apps=os.listdir(profileDir)
		print(apps)
		return(apps)
	#def _getApps

	def setStatus(self,enforce=True,apps=[]):
		apps=[]
		if enforce==self.getStatus():
			return()

		if len(apps)==0:
			apps=self._getApps()
		for app in apps:
			if enforce==True:
				cmd=["/usr/sbin/aa-enforce",app]
				if "lliurex" in app or "zero-center" in app or "rebost" in app:
					cmd=["/usr/sbin/aa-complain",app]
			else:
				cmd=["/usr/sbin/aa-complain",app]
				if app not in self.enforced:
					self.enforced.append(app)
			proc=subprocess.run(cmd,capture_output=True,universal_newlines=True)
		if enforce==False:
			self.setLock()
	#def setStatus

	def unlockApt(self,enforce=True):
		apps=self._getApps(appsFilter=["apt","dpkg"])
		self.setStatus(enforce=enforce,apps=apps)
	#def unlockApt

	def setLock(self):
		multiprocessing.set_start_method('fork')
		mproc=multiprocessing.Process(target=self._watchdog)
		mproc.start()
		return
	#def setLock

	def _watchdog(self):
		return()
		print("Waiting for apt...")
		found=False
		name=""
		time.sleep(self.watchdogLaunchDelay)
		while found==False:
			found=True
			for proc in psutil.process_iter(["pid","name"]):
				for app in self.enforced:
					name=os.path.basename(app)
					if os.path.basename(proc.info.get("name","")) in name:
						found=False
						break
			if found==False:
				time.sleep(10)
		self.setStatus(enforce=True,apps=self.enforced)
		self.enforced=[]
