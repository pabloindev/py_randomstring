from tkinter import *
import ANURandom
import urllib.request
import re, os, random
from tkinter.scrolledtext import ScrolledText

class App:
	def __init__(self, master):
		self.master = master
		self.config_windows(master)

        #set title
		self.master.title("Random String")
		self.master.iconbitmap(self.getScriptDirectory() + "\\icona.ico")

		frame=Frame(master) #frame=Frame(master, bg="blue")
		frame.grid(row=0, column=0, sticky=N+S+E+W)
		#Grid.rowconfigure(frame, 0, weight=1)
		#Grid.columnconfigure(frame, 0, weight=1) #Grid.rowconfigure(frame, 1, weight=1)
		Grid.columnconfigure(frame, 1, weight=1) #mi dice quale colonna e resizable
		Grid.columnconfigure(frame, 2, weight=1) #Grid.rowconfigure(frame, 2, weight=1)
		Grid.columnconfigure(frame, 3, weight=1)
		Grid.columnconfigure(frame, 4, weight=1)
		Grid.rowconfigure(frame, 2, weight=1)
		
		self.create_menu(master)
		self.add_controlli(master, frame)
	
	def add_controlli(self, master, frame):
		Label(frame, text="Dictionary").grid(row=0, sticky=W, padx=5, pady=5)
		Label(frame, text="Num Characters").grid(row=1, sticky=W, padx=5, pady=5)
		Label(frame, text="Result").grid(row=2, sticky=W+N, padx=5, pady=5)

		
		self.e1 = Entry(frame)
		self.e2 = Entry(frame)
		#self.e3 = Entry(frame)
		self.e3 = ScrolledText(frame, height=4)

		
		self.e1.grid(row=0, column=1, columnspan=4, padx=5, pady=5, sticky=W+E)
		self.e2.grid(row=1, column=1, columnspan=4, padx=5, pady=5, sticky=W+E)
		self.e3.grid(row=2, column=1, columnspan=4, padx=5, pady=5, sticky=W+E+S+N)
		
		self.e1.insert(0, "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ$_")
		#self.e2.insert(0, "10")
		self.create_popup_for_entry(master,self.e3)
		self.e3.bind("<Control-Key-c>", self.copy_all2)
		self.e3.bind("<Control-Key-C>", self.copy_all2) # just in case caps lock is on
		
		
		Button(frame, text="Exit",            command=master.quit).grid(row=3, column=1, padx=5, pady=5, sticky=W+E+S)
		Button(frame, text="Random String", command=self.calcola_stringa).grid(row=3, column=2, padx=5, pady=5, sticky=W+E+S)
		Button(frame, text="ANU Quantum RG",  command=self.chiama_anu_quantum).grid(row=3, column=3, padx=5, pady=5, sticky=W+E+S)
		Button(frame, text="Wordpress salt",         command=self.chiama_wp_salt).grid(row=3, column=4, padx=5, pady=5, sticky=W+E+S)
		
		""" ************************************************
		**** parte che non utlizza la grid ma il pack ******
		frame = Frame(master, bg="blue")
		frame.pack(fill=BOTH, expand=YES)
		
		frame.pack(fill=BOTH, expand=YES)
		
		lb = Label(master, text="Random String")
		lb.pack(side=LEFT)
		#lb.grid(row=0)
		
		e = Entry(master, width=10)
		e.pack(side=LEFT, fill=X, expand=YES, padx=10)
		#e.grid(row=0)
		
		self.button = Button(master, text="QUIT", fg="red", command=master.quit)
		self.button.pack(side=LEFT)
		#self.button.grid(row=0)

		self.hi_there = Button(master, text="Hello", command=self.say_hi)
		self.hi_there.pack(side=LEFT)
		#self.hi_there.grid(row=0)
		***********************************************  """
	
	def chiama_anu_quantum(self):
		size = self.getsize()
		
		a = ANURandom.ANURandom(size)
		str = a.getChar()
		self.e3.delete('1.0', END)
		self.e3.insert(INSERT, str)

	
	#mpostazioni iniziali della finestra
	def config_windows(self,master):
		#master.resizable(TRUE,FALSE)
		master.resizable(TRUE,TRUE)
		root.minsize(800, 350)
		master.geometry('{}x{}'.format(800, 350)) #dimensione inziale
		Grid.rowconfigure(master, 0, weight=1)
		Grid.columnconfigure(master, 0, weight=1)
	
	
	# creo il popup per l'entry 3
	def create_popup_for_entry(self, master, entry):
		self.popup = Menu(master, tearoff=0)
		self.popup.add_command(label="Copy", command=self.copy_all1) # , command=next) etc...
		#self.popup.add_separator()
		self.popup.add_command(label="nothing")
		entry.bind("<Button-3>", self.do_popup)
			
	#copio la stringa nella clip quando faccio ctrl + c
	def copy_all2(self, event):
		self.master.clipboard_clear()
		self.master.clipboard_append(self.e3.get())
	
	#copio la stringa nella clip quando seleziono voce menu "Copy"
	def copy_all1(self):
		testo = self.textFrame.get("1.0", END)
		self.master.clipboard_clear()
		self.master.clipboard_append(testo)

	def do_popup(self,event):
		# display the popup menu
		try:
			self.popup.tk_popup(event.x_root, event.y_root, 0)
		finally:
			# make sure to release the grab (Tk 8.0a1 only)
			self.popup.grab_release()
	
	#creo il menu inziale - per il momento non fa nulla
	def create_menu(self, master):
		menu = Menu(master)
		master.config(menu=menu)
		filemenu = Menu(menu)
		menu.add_cascade(label="File", menu=filemenu)
		filemenu.add_command(label="New", command=self.NewFile)
		filemenu.add_command(label="Open...", command=self.OpenFile)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=master.destroy)

		helpmenu = Menu(menu)
		menu.add_cascade(label="Help", menu=helpmenu)
		helpmenu.add_command(label="About...", command=self.About)
		
		
	# calcolo la stringa random
	def calcola_stringa(self):
		size = self.getsize()

		chars = self.e1.get()
		stringa = ''.join(random.SystemRandom().choice(chars) for _ in range(size))
		self.e3.delete('1.0', END)
		self.e3.insert(INSERT, stringa)
		#self.e3.insert(stringa, END)
		#self.e3.delete(0, END)
		#self.e3.insert(0, stringa)

	def chiama_wp_salt(self):
		size = self.getsize()
		
		lista_results = []
		with urllib.request.urlopen('https://api.wordpress.org/secret-key/1.1/salt/') as f:
			html = f.read().decode('utf-8')
			for line in html.splitlines():
				x = re.search("\\s\\'.*\\'", line)
				stringa_casuale = x.group().strip()[1:-1]
				lista_results.append(stringa_casuale)

		self.e3.delete('1.0', END)
		k = 0
		for line in lista_results:
			#print(type(line))
			#print(str(len(line)) + ": " + line)
			for c in line:
				#print(str(i))
				if k < size:
					self.e3.insert(INSERT, c)
					k += 1
			self.e3.insert(INSERT, "\n")


	def getsize(self):
		str_size = self.e2.get()
		isinteger = str.isdigit(str_size)
		if isinteger:	
			size = int(str_size)
		else:
			size = 1000
		return size

	def getScriptDirectory(self): # ritorna il percorso dove si trova lo script senza separatore finale
		return os.path.dirname(os.path.realpath(__file__))

		
	def NewFile(self):
		print("New File!")
	def OpenFile(self):
		name = askopenfilename()
		print(name)
	def About(self):
		print("This is a simple example of a menu")
	
	

root = Tk()
app = App(root)
root.mainloop()
