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
TIMEOUT=6
i18n={"USAGE":_("Usage"),
	"LOCK":_("Locks software management"),
	"UNLOCK":_("Unlocks software management"),
	"FULL":_("Loads all apps (unfiltered)"),
	"FILTERED":_("Only load apps from catalogue"),
	"DEFAULT":_("Load values from configuration file"),
	"LAUNCHGUI":_("Without arguments launches the gui")
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
	showH=True
	for i in args:
		if i=="unlock":
			showH=False
			enforce=False
		elif i=="full":
			showH=False
			catalogue=True
		elif i=="default":
			showH=False
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
				if jconf.get("timeout","0").isdigit()==True:
					timeout=int(jconf.get("timeout","0"))
		elif i in ["lock","filtered"]:
			showH=False
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
	#config.setWiki('https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Accesibilidad%20en%20Lliurex:%20Access%20Helper')
	config.setBanner('unlocker_banner.png')
	config.hideNavMenu(False)
	#config.setBackgroundImage('repoman_login.svg')
	config.setConfig(confDirs={'system':'/usr/share/software-unlocker','user':os.path.join(os.environ['HOME'],".config/software-unlocker")},confFile="lock.json")
	config.Show()
	app.exec_()
else:
	(enforce,catalogue,timeout)=processParms(sys.argv)
	locker=liblocker.softlocker()
	locker.setTimeout(timeout)
	locker.setStatus(enforce=enforce)
	rebost=store.client()
	if rebost.getFiltersEnabled()==catalogue:
		rebost.disableFilters()
	print(_("Software management will be locked in {} minutes".format(int(timeout/60))))
