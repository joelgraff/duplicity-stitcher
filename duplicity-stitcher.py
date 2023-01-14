#!/usr/bin/env python
# Author: David Huss
# Website: http://blog.atoaudiovisual.com
# Usage instructions http://blog.atoav.com/2013/09/restore-broken-deja-dup-backup-hand/
# Modified by Antonio Roberts to preserve folder structure
# Modified by Joel Graff to run with python3

import tkinter as tk
from tkinter.filedialog import *
import sys, os

class ExampleApp(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		toolbar = tk.Frame(self)
		toolbar.pack(side="left", fill="y")
		b1 = tk.Button(self, text="open", command=self.open)
		b2 = tk.Button(self, text="join!", command=self.save)
		b1.pack(in_=toolbar, side="top")
		b2.pack(in_=toolbar, side="top")
		self.title("duplicity_joiner")
		self.scrollbar = tk.Scrollbar(self)
		self.scrollbar.pack(side="right", fill="y")
		self.text = tk.Text(self, wrap="word", bg="#151515", bd="10", padx=20)
		self.text.pack(side="top", fill="both", expand=True)
		self.text.tag_configure("stderr", foreground="#b22222")
		self.text.tag_configure("stdout", foreground="#808080")
		self.text.tag_configure("green", foreground="#00DD00")

		sys.stdout = TextRedirector(self.text, "stdout")
		sys.stderr = TextRedirector(self.text, "stderr")
		sys.green = TextRedirector(self.text, "green")

		self.text.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.text.yview)

		self.directory = None
		self.savedirectory = None
		print ("This is the duplicity file joiner, which will try to join the files of an duplicity multivol_snapshot.")
		print ()
		print ("Note: this is not professional software, this is something I put up when I thought my backup will be lost otherwise. As far as I tested it works (it worked for me). I wont guarantee it works for you.")
		print ()
		print ("Good Luck!")
		print ()

	def open(self):
		if self.directory is None and self.savedirectory is None:
			self.directory = askdirectory(title="Open the folder containing the files to join", mustexist=True)
			if len(self.directory) != 0:
				sys.green.write("Selected for joining: "+self.directory+"\n")
				self.savedirectory = askdirectory(title="Select where to save the resaved "+os.path.basename(self.directory))
				if len(self.savedirectory) != 0:
					sys.green.write("Selected for saving: "+self.savedirectory+"\n\n")
					print ("Press Join")
					print ()
				else:
					sys.stderr.write("Cancled Selection\n")
					self.savedirectory = None
					self.directory = None	
			else:
				sys.stderr.write("Cancled Selection\n")
				self.directory = None
				self.savedirectory = None

	def save(self):
		if self.savedirectory is not None and self.directory is not None:
			self.find_leafes(self.directory)
			self.directory = None
			self.savedirectory = None
		else:
			sys.stderr.write("Select Input und Outputfile first: press open\n")

	def find_leafes(self, directory):
		print ("Scanning for leaf directories ...")
		for i, x in enumerate(os.walk(directory)):
			if not x[1]:
				self.appendfile(x[0], self.savedirectory, i)
				#sys.green.write("Sucess! Saved "+os.path.basename(x[0])+"\n\n")
				print ()
				print ()
				self.text.see("end")
				self.update_idletasks()
		sys.green.write("Saved all leafes\n\n\n")
		print ()

	def sortlist(self, liste):
		for i, entry in enumerate(liste):
			liste[i] = int(entry)
		liste.sort(key=int)
		return liste

	def appendfile(self, path, selecteddirectory, pos):
		tempfiles = []
		filename = os.path.basename(path)
		splitpath = os.path.dirname(path).split("\\", 1)
		rootpath = os.path.basename(splitpath[0])
		print ("rootpath: "+rootpath)
		print ("filename: "+filename)
		filepath = splitpath[0]
		savepath = selecteddirectory+"/"+filepath

		print ("savepath: "+savepath)
		print ()

		fragments = self.sortlist(os.listdir(path))
		collection = []

		if not os.path.exists(savepath):
			os.makedirs(savepath)

		for fragment in fragments:
			with open(path+"/"+str(fragment),"rb") as f:
				collection.append(f.read())

		with open(savepath+"/"+filename, "wb") as o:
			for part in collection:
				o.write(part)

		print ("Saved ["+str(pos)+"]: "+filename+" in directory "+savepath)
		print ()
		self.text.see("end")
		self.update_idletasks()

	def stellen(self, number):
		return len(str(number).replace('.', ''))

class TextRedirector(object):
	def __init__(self, widget, tag="stdout"):
		self.widget = widget
		self.tag = tag

	def write(self, str):
		self.widget.configure(state="normal")
		self.widget.insert("end", str, (self.tag,))
		self.widget.configure(state="disabled")

app = ExampleApp()
app.mainloop()