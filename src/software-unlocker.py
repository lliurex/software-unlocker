#!/usr/bin/env python3
import sys
import subprocess
import os,shutil
import json
from PySide2.QtWidgets import QApplication,QDialog,QGridLayout,QLabel,QPushButton,QLayout,QSizePolicy
from PySide2.QtCore import Qt
from PySide2 import QtGui
from appconfig.appConfigScreen import appConfigScreen as appConfig
from appconfig import appconfigControls
import gettext
import time
from stacks import liblocker
from rebost import store
_ = gettext.gettext
TIMEOUT=60
i18n={"USAGE":_("Usage"),
	"LOCK":_("Locks software management"),
	"UNLOCK":_("Unlocks software management"),
	"FULL":_("Loads all apps (unfiltered)"),
	"FILTERED":_("Only load apps from catalogue"),
	"DEFAULT":_("Load values from configuration file"),
	"LAUNCHGUI":_("Without arguments launches the gui"),
	"MSG_UNLOCK":_("Software management will be locked in"),
	"MSG_LOCK":_("Software management locked."),
	"MINUTES":_("minutes")
}

def showHelp():
	print("{0}: {1} (lock|unlock|full|filtered|default)\n".format(i18n.get("USAGE"),sys.argv[0]))
	print("  lock:\t{}".format(i18n.get("LOCK")))
	print("  unlock:\t{}".format(i18n.get("UNLOCK")))
	print("  full:\t{}".format(i18n.get("FULL")))
	print("  filtered:\t{}".format(i18n.get("FILTERED")))
	print("  default:\t{}".format(i18n.get("DEFAULT")))
	print("{}\n".format(i18n.get("LAUNCHGUI")))
	sys.exit(1)

def processParms(args):
	enforce=True
	fullcatalogue=False
	timeout=TIMEOUT
	showH=False
	for i in args[1:]:
		if i=="unlock":
			enforce=False
		elif i=="full":
			fullcatalogue=True
		elif i=="default":
			fconf="/usr/share/software-unlocker/lock.json"
			jconf={}
			if os.path.isfile(fconf):
				try:
					with open (fconf,"r") as f:
						jconf=json.load(f)
				except Exception as e:
					print(e)
			if jconf.get("lock","true")=="false":
				enforce=False
			if jconf.get("catalogue","false")=="true":
				fullcatalogue=True
			if jconf.get("timeout","0")!="0":
				if jconf.get("timeout").isdigit()==True:
					timeout=int(jconf.get("timeout",TIMEOUT))
		elif i not in ["unlock","full","lock","filtered"]:
			print("Unknown parm {}".format(i))
			showH=True
	if showH==True:
		showHelp()
	return(enforce,fullcatalogue,timeout)
#def processParms

if len(sys.argv)==1:
	app=QApplication(["Software-Unlocker"])
	config=appConfig("Software-Unlocker",{'app':app})
	config.setWindowTitle("Software Unlocker")
	config.setRsrcPath("/usr/share/software-unlocker/rsrc")
	config.setIcon('software-unlocker')
	#config.setWiki('https://wiki.edu.gva.es/lliurex/tiki-index.php?page=software-unlocker')
	config.setBanner('unlocker_banner.png')
	config.hideNavMenu(False)
	config.setConfig(confDirs={'system':'/usr/share/software-unlocker','user':os.path.join(os.environ['HOME'],".config/software-unlocker")},confFile="lock.json")
	config.Show()
	app.exec_()
else:
	(enforce,catalogue,timeout)=processParms(sys.argv)
	locker=liblocker.softlocker()
	locker.setTimeout(timeout)
	locker.setStatus(enforce=enforce)
	rebost=store.client()
	currentState=rebost.getFiltersEnabled()
	if isinstance(currentState,int):
		if currentState==1:
			currentState=True
		else:
			currentState==False
		if currentState==catalogue:
			lastUpdate="/usr/share/rebost/tmp/sq.lu"
			if os.path.isfile(lastUpdate)==True:
				os.unlink(lastUpdate)
			rebost.disableFilters()
	if enforce==True:
		print("{0}".format(i18n["MSG_LOCK"]))
	else:
		print("{0} {1} {2}".format(i18n["MSG_UNLOCK"],int(timeout/60),i18n["MINUTES"]))
