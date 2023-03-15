#!/usr/bin/python3
import sys
import os
from PySide2.QtWidgets import QApplication, QLabel, QPushButton,QGridLayout,QHeaderView,QHBoxLayout,QComboBox,QLineEdit,QWidget,QMenu,QCheckBox,QDialog,QDialogButtonBox,QApplication
from PySide2 import QtGui
from PySide2.QtCore import Qt,QSize,Signal,QThread
from appconfig.appConfigStack import appConfigStack as confStack
from appconfig import appconfigControls
from rebost import store 
import json
import random
import gettext
from . import liblocker
from rebost import store
_ = gettext.gettext
QString=type("")

i18n={
	"CONFIG":_("Lock Screen"),
	"DESCRIPTION":_("Set software lock state"),
	"MENUDESCRIPTION":_("Set software lock state"),
	"TOOLTIP":_(""),
	"ONAPPLYUNLOCK":_("After apply the software management will be unlocked\nfor {0} minutes and then will lock again as early as possible."),
	"ONAPPLYLOCK":_("After apply the software management will be locked"),
	"DLGTITLE":_("Warning"),
	"LBLLOCKER":_("Lock software management"),
	"LBLSTORE":_("Load full software catalogue"),
	"CHANGED":_("Software management is"),
	"LOCKED":_("locked"),
	"UNLOCKED":_("unlocked")
	}

class unlockSoftware(QThread):
	def __init__(self,parent=None):
		super().__init__()
		self.locker=None
		self.rebost=None
		self.lockstate=None
		self.filterstate=None
	#def __init__

	def setData(self,locker,rebost,lockstate,filterstate):
		self.locker=locker
		self.rebost=rebost
		self.lockstate=lockstate
		self.filterstate=filterstate
	#def setData

	def run(self):
		self.locker.setStatus(enforce=self.lockstate)
		currentState=self.rebost.getFiltersEnabled()
		if isinstance(currentState,int):
			print(bool(currentState))
			if currentState==1:
				currentState=True
			else:
				currentState==False
		if currentState==self.filterstate:
			self.rebost.disableFilters()
		return(False)
	#def run

class confirmDialog(QDialog):
	def __init__(self,timeout,status):
		super().__init__()
		self.setWindowTitle(i18n.get("DLGTITLE"))
		QBtn = QDialogButtonBox.Yes | QDialogButtonBox.No
		self.buttonBox = QDialogButtonBox(QBtn)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		self.layout = QGridLayout()
		if status==False:
			message = QLabel(i18n.get("ONAPPLYUNLOCK").format(int(timeout/60)))
		else:
			message = QLabel(i18n.get("ONAPPLYLOCK"))
		self.layout.addWidget(message)
		self.layout.addWidget(self.buttonBox)
		self.setLayout(self.layout)
	#def __init__
#class confirmDialog

class portrait(confStack):
	def __init_stack__(self):
		self.dbg=False
		self.enabled=True
		self._debug("portrait load")
		self.menu_description=i18n.get('MENUDESCRIPTION')
		self.description=i18n.get('DESCRIPTION')
		self.icon=('application-x-desktop')
		self.tooltip=i18n.get('TOOLTIP')
		self.changed=[]
		self.level='user'
		self.locker=liblocker.softlocker()
		self.rebost=store.client()
		self.timeout=600 #In seconds
		self.locker.setTimeout(self.timeout)
		self.lock=unlockSoftware()
		self.running=False
	#def __init__

	def _load_screen(self):
		self.config=self.getConfig()
		self.box=QGridLayout()
		self.setLayout(self.box)
		self.chkEnableLock=QCheckBox(i18n.get("LBLLOCKER"))
		self.chkEnableLock.setChecked(self.locker.getStatus())
		self.box.addWidget(self.chkEnableLock)
		self.chkEnableStore=QCheckBox(i18n.get("LBLSTORE"))
		self.chkEnableStore.setChecked(self.locker.getStatus())
		self.chkEnableStore.setChecked(not(self.rebost.getFiltersEnabled()))
		self.chkEnableLock.stateChanged.connect(self.updateScreen)
		self.box.addWidget(self.chkEnableStore)
	#def _load_screen

	def updateScreen(self):
		#self.chkEnableLock.setChecked(self.locker.getStatus())
		self.chkEnableStore.setEnabled(not(self.chkEnableLock.isChecked()))
		if self.chkEnableLock.isChecked()==True:
			self.chkEnableStore.setChecked(False)
	#def _update_screen

	def closeEvent(self):
		if self.running==True:
			return
	#def closeEvent

	def resetScreen(self):
		pass
	#def resetScreen

	def _unlockSoftware(self):
		self.running=True
		self.lock.setData(self.locker,self.rebost,self.chkEnableLock.isChecked(),self.chkEnableStore.isChecked())
		self.lock.start()
		#self.setEnabled(False)
		self.lock.finished.connect(self._finish)
	#def _unlockSoftware

	def _showMsg(self):
		dlg=confirmDialog(self.timeout,self.chkEnableLock.isChecked())
		sw=False
		if dlg.exec():
			self.setEnabled(False)
			QApplication.setOverrideCursor(Qt.WaitCursor)
			self._unlockSoftware()
			sw=True
		return(sw)
	#def _showMsg

	def _finish(self):
		print("Ending...")
		self.setEnabled(True)
		msg=i18n.get("UNLOCKED")
		if self.chkEnableLock.isChecked()==True:
			msg=i18n.get("LOCKED")
		msg="{} {}".format(i18n.get("CHANGED"),msg)
		#self.showMsg(msg)
		self.running=False
		QApplication.restoreOverrideCursor()
	#def _finish
	
	def writeConfig(self):
		self._showMsg()
	#def writeConfig

