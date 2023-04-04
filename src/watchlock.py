#!/usr/bin/env python3
import os,time,sys
import psutil
import subprocess

if len(sys.argv)<=1:
	watchdogLaunchDelay=60
elif isinstance(sys.argv[1],int)==False:
	watchdogLaunchDelay=60
else:
	watchdogLaunchDelay=int(sys.argv[1])
found=True
name=""
managedTools=os.listdir("/usr/share/software-unlocker/profiles.d")
excluded=["rebost-dbus.py","unsecuresnap","unsecureflatpak","unsecuredpkg","unsecuredpkcon","zero-center.py"]
while found==True:
	time.sleep(watchdogLaunchDelay)
	found=False
	for proc in psutil.process_iter(["pid","name"]):
		for app in managedTools:
			name=os.path.basename(app)
			if name in excluded:
				continue
			if os.path.basename(proc.info.get("name","")) in name:
				if name=="flatpak":
					if "install" or "uninstall" in proc.cmdline():
						break
				elif name=="snap":
					if "install" or "remove" in proc.cmdline():
						found=True
						break
				else:
					found=True
					break
		if found==True:
			break
cmd=["/usr/share/software-unlocker/software-unlocker.py","default"]
try:
	subprocess.run(cmd)
except Exception as e:
	print(e)
