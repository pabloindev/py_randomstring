#################### IMPORT ####################
# qt
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QFileDialog, 
    QGridLayout,
    QPushButton, 
    QLabel,
    QProgressBar,
    QMessageBox,
    QDialog
)
from PyQt6.QtCore import QThread, QProcess, pyqtSignal #threads

# python standard lib
import sys, os, json, logging, re
from logging.handlers import RotatingFileHandler
import urllib.request

#https://docs.python.org/3/library/secrets.html
import secrets

# file esterni
import ANURandom


#################### FUNZIONI ####################
class MainWindow(QtWidgets.QMainWindow):

    working_dir = None        # percorso alla directory corrente
    config = None             # file di configurazione, dictionary caricato dal file config.json
    worker_thread = None      # worker thread che si occupa di fare l'hash dei file
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # setto variili della classe che mi possono essere utili
        self.working_dir = get_working_directory()
        set_working_directory()
        
        # carico il file creato con qt designer
        uic.loadUi("main.ui", self)


        # creo la cartella dei log se non esiste
        if not os.path.exists(os.path.join(self.working_dir,"logs")): 
            os.makedirs(os.path.join(self.working_dir,"logs")) 

        # imposto logging su file
        logging.basicConfig(
            # appendo log al file, non vado a sovrascrivere, non specifico filemode poichè di default è già append
            format='%(asctime)s - %(levelname)s - %(message)s'  # formato
            , level=logging.DEBUG
            , handlers=[
                #logging.FileHandler(LOG_FILENAME), # nome del file di log, di questo handler non ho bisogno poichè sul file disk scrive già RotatingFileHandler
                logging.StreamHandler(sys.stdout),  # quando vado a inserire un log stampo anche su console
                logging.handlers.RotatingFileHandler(os.path.join(self.working_dir,"logs","app.log"), maxBytes=1000000, backupCount=5, encoding='utf-8') # log rotating 1MB
            ]
        )
        logging.debug('*********************************************')
        logging.debug('Applicazione py_hash avviata')


        # carico il thread e definisco gli eventi 
        #self.worker_thread = WorkerThread()
        #self.worker_thread.sig_job_update.connect(self.thread_job_update)
        #self.worker_thread.sig_job_complete.connect(self.thread_job_complete)
        #self.worker_thread.sig_all_complete.connect(self.thread_all_complete)
        

        #self.config = readConfigJson()
        #machine = self.config["machine"]


        # modifico ulteriormente la gui poichè non riesco a fare tutto da qtdesigner
        self.changeUI()

        # setto gli eventi dei vari widgets
        self.settaEventi()
        
        
    
    # -------------------------------------------------------------------------------
    # modifica ulteriore della UI
    # -------------------------------------------------------------------------------
    def changeUI(self):
        
        # imposta l'icona della finestra
        self.setWindowIcon(QtGui.QIcon('icona.ico'))

        # setto l'lfabeto di default
        self.lineEditAlfabeto.clear()
        self.lineEditAlfabeto.setText("abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ$_")


    # -------------------------------------------------------------------------------
    # definizione degli eventi 
    # -------------------------------------------------------------------------------
    # entry per settare tutti gli eventi
    def settaEventi(self):
        # toolbar - esco dall'app
        self.actionExit.triggered.connect(self.close) 
        
        # pulsante per calcolare una stringa casuale utilizzando i metodi antivi di python
        self.pushButtonRandomStr.clicked.connect(self.getRanddomString) 
        
        # pulsante che ritorna una stringa causale da ANU Random number generator
        self.pushButtonAnu.clicked.connect(self.getRanddomANU) 

        # pulsante che mi ritorna il salt dal servizio di wordpress
        self.pushButtonWpSalt.clicked.connect(self.getRanddomWpSalt) 

        
    # pulsante per calcolare una stringa casuale utilizzando i metodi antivi di python
    def getRanddomString(self):
        lunghezza = self.spinBoxNumChars.value()
        alfabeto = self.lineEditAlfabeto.text()
        
        # calcolo una lista di caratteri presi a caso dall'alfabeto
        lista_temp = [secrets.choice(alfabeto) for i in range(lunghezza)]
        stringa_casuale = ''.join(lista_temp)

        # aggiorno la textarea
        self.plainTextEditResult.clear()
        self.plainTextEditResult.appendPlainText(stringa_casuale)



    # pulsante che ritorna una stringa causale da ANU Random number generator
    def getRanddomANU(self):

        lunghezza = self.spinBoxNumChars.value()
        alfabeto = self.lineEditAlfabeto.text()
        
        a = ANURandom.ANURandom(lunghezza)
        stringa_casuale = a.getChar()

        # aggiorno la textarea
        self.plainTextEditResult.clear()
        self.plainTextEditResult.appendPlainText(stringa_casuale)


    # pulsante che mi ritorna il salt dal servizio di wordpress
    def getRanddomWpSalt(self):
        lunghezza = self.spinBoxNumChars.value()
        alfabeto = self.lineEditAlfabeto.text()
		
        # recupero il contenuto dalla pagina online
        lista_results = []
        with urllib.request.urlopen('https://api.wordpress.org/secret-key/1.1/salt/') as f:
            html = f.read().decode('utf-8')
            for line in html.splitlines():
                x = re.search("\\s\\'.*\\'", line)
                stringa_casuale = x.group().strip()[1:-1]
                lista_results.append(stringa_casuale)


        # aggiorno la textarea
        self.plainTextEditResult.clear()

        # aggiungo le righe recuperate dentro la textarea
        for x in lista_results:
            self.plainTextEditResult.appendPlainText(x)


    # -------------------------------------------------------------------------------
    # EVENTI del thread
    # -------------------------------------------------------------------------------
    




# #leggo il file di config con tutti le configurazioni del programma
def readConfigJson():
    with open('config.json') as json_data_file:
        appsetting = json.load(json_data_file)
        return appsetting


def set_working_directory():
    absPath = get_working_directory()
    os.chdir(absPath)


def get_working_directory():
    absPath = ""
    # mi costruisco il percorso assoluto della directory che contiene il file main.py
    if(os.path.isabs(sys.argv[0])):
        absPath = os.path.dirname(sys.argv[0])
    else:
        #provo a costruirmi la directory in questo modo (sonogià dentro la directory del programma)
        absPath = os.path.dirname(os.path.abspath('.') + "/" + sys.argv[0])

    return absPath


# mi dice se sono un mac linux oppure windows
def get_os():
    os_name = "nix"
    if os.name == 'nt':
        os_name = "windows"
    return os_name



#################### ENTRY PROGRAMMA ####################
if __name__ == "__main__":
    #main(sys.argv[1:])
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

'''
nomi dei widget presenti 


actionExit


lineEditAlfabeto
spinBoxNumChars
plainTextEditResult


pushButtonRandomStr    pushButtonAnu    pushButtonWpSalt
'''
