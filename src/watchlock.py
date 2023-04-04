#!/usr/bin/env python3
import os,time,sys
import psutil
import subprocess

watchdogLaunchDelay=1
found=True
name=""
time.sleep(watchdogLaunchDelay)
managedTools=os.listdir("/usr/share/software-unlocker/profiles.d")
excluded=["rebost-dbus.py"]
while found==True:
	found=False
	for proc in psutil.process_iter(["pid","name"]):
		for app in managedTools:
			name=os.path.basename(app)
			if name in excluded:
				continue
			if os.path.basename(proc.info.get("name","")) in name:
				if name=="flatpak":
					if "install" or "uninstall" in proc.cmdline():
                        :x
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
	time.sleep(1)
print("Locking...")
cmd=["/usr/share/software-unlocker/software-unlocker.py","default"]
subprocess.run(cmd)
