import urllib.request
from pprint import pprint

class ANURandom:
    BINARY = "BINARY"
    HEX = "HEX"
    CHAR = "CHAR"
    
    def __init__(self, numchar):
        self.numchar = numchar
        
    def getRandom(self,type):
        if type == self.BINARY:
            url = 'http://150.203.48.55/RawBin.php'
        elif type == self.HEX:
            url = 'http://150.203.48.55/RawHex.php'
        elif type == self.CHAR:
            url = 'https://qrng.anu.edu.au/wp-content/plugins/colours-plugin/get_block_alpha.php' #ho visto dal codice della pagina che richiama questa pagina via ajax
            
        page = urllib.request.urlopen(url, timeout=5)

        data = page.read().decode("utf-8") #Convert bytes to a Python string
        #print(data)
        #exit()
        #num = data.split('"rng"')[1].split('<td>\n')[1].split('</td>')[0]
        #return num[:self.numchar] #ritorno da 0 a self.numchar caratteri
        return data[:self.numchar]

    def getBin(self):
        return self.getRandom(self.BINARY)

    def getHex(self):
        return self.getRandom(self.HEX)

    def getChar(self):
        return self.getRandom(self.CHAR)