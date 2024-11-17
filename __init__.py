from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *
from anki.notes import Note 
from anki.consts import MODEL_CLOZE
from anki.hooks import addHook
import re
import json
import subprocess
import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
from googletrans import Translator


def show_progress_bar(): # Create a dialog 
	dialog = QDialog(mw) 
	dialog.setWindowTitle("Preparing your cards...") # Create a progress bar 
	progress_bar = QProgressBar(dialog) 
	progress_bar.setMinimum(0) 
	progress_bar.setMaximum(100) 
	progress_bar.setValue(0) # Create a layout and add the progress bar to it 
	layout = QVBoxLayout() 
	layout.addWidget(progress_bar) 
	dialog.setLayout(layout) # Show the dialog 
	dialog.show() # Update the progress bar 
	return dialog, progress_bar



def pull_from_dl():
	with open(os.path.join(os.path.dirname(__file__), "config.json")) as f:
		config = json.load(f)
	deckname = config["deck_name"]
	deckid = mw.col.decks.id(deckname)
	oldnoteids = mw.col.find_notes(f'deck:{deckname}')
	oldnotes = [mw.col.get_note(noteid)["Front"] for noteid in oldnoteids]
	out = subprocess.run([os.path.join(os.path.dirname(__file__), "Python", "python.exe"), os.path.join(os.path.dirname(__file__), "getdat.py")], capture_output = True)
	dialog, progress_bar = show_progress_bar()
	out = out.stdout
	out = out.decode("Latin-1")
	out = out.split(",")
	transwords = []
	inlang = out[0]
	outlang = out[1]
	out = out[2:]
	i = 0
	for word in out:
		i += 1
		progress_bar.setValue((i*100)/len(out))
		QCoreApplication.processEvents() 
		if word not in oldnotes:
			print(word)
			trans = translator.translate(word, src=inlang, dest=outlang)
			time.sleep(0.2)
			note = Note(mw.col, mw.col.models.by_name("Basic"))
			note["Front"] = word 
			note["Back"] = trans.text
			mw.col.add_note(note, deckid)
	mw.reset()







translator = Translator()
# create a new menu item, "test"
runsync = QAction("DuolingoSync", mw)

# set it to call testFunction when it's clicked
qconnect(runsync.triggered, pull_from_dl)

# and add it to the tools menu
mw.form.menuTools.addAction(runsync)
