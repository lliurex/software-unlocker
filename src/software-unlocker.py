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
_ = gettext.gettext

TIMEOUT=6
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
elif "lock" in sys.argv[-1]:
	enforce=True
	if sys.argv[-1]=="unlock":
		enforce=False
	locker=liblocker.softlocker()
	locker.setTimeout(TIMEOUT)
	if sys.argv[-2]=="apt":
		locker.unlockApt(enforce=enforce)
	else:
		locker.setStatus(enforce=enforce)
	print(_("Software management will be locked in {} minutes".format(int(TIMEOUT/60))))
