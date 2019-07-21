from tkinter import *
from tkinter import ttk
import configparser
import requests
import json

DEFAULTPADDING=4

class Exchanger(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,width="400", height="150")


        config=configparser.ConfigParser()
        config.read("config.ini")
        self.api_key=config['fixer.io']['API_KEY']
        self.all_symbols_ep=config['fixer.io']['ALL_SYMBOLS_EP']
        self.rate_ep=config['fixer.io']['RATE_LATEST_EP']

        currencies=self.getCurrencies()

        #Variable de control

        self.strInQuantity= StringVar(value="")
        self.strOldInQuantity=self.strInQuantity.get()
        self.strInQuantity.trace("w",self.convertirDivisas)
        self.strInCurrency= StringVar()
        self.strOutCurrency= StringVar()

        frErrorMessages=ttk.Frame(self,height=40)
        frErrorMessages.place(x=0,y=360)
        frErrorMessages.pack_propagate(0)


        frIncurrency =ttk.Frame(self)
        frIncurrency.pack_propagate(0)

        lblQ= ttk.Label(frIncurrency,text="Cantidad")
        lblQ.pack(side=TOP, fill=X, padx=DEFAULTPADDING,pady=DEFAULTPADDING)

        self.inquantityEntry = ttk.Entry(frIncurrency, font=("Helvetica",24,'bold'), width= 10, textvariable = self.strInQuantity)
        self.inquantityEntry.pack(side=TOP,fill=X, padx=DEFAULTPADDING,pady=DEFAULTPADDING)

        self.incurrencyCombo= ttk.Combobox(frIncurrency,width=25,height=5,values=currencies, textvariable=self.strInCurrency)
        self.incurrencyCombo.pack(side=TOP,fill=X, padx=DEFAULTPADDING,pady=DEFAULTPADDING)
        self.incurrencyCombo.bind('<<ComboboxSelected>>',self.convertirDivisas)


        frIncurrency.pack(side=LEFT, fill=BOTH, expand=TRUE)

        frOutCurrency = ttk.Frame(self)
        frOutCurrency.pack_propagate(0)

       

        self.lblErrorMessages = ttk.Label(frErrorMessages,text='texto de prueba',foreground='red')
        self.lblErrorMessages.pack(side=TOP,fill=X,expand=TRUE)

        lblQ=ttk.Label(frOutCurrency, text="Cantidad")
        lblQ.pack(side=TOP, fill=X)

        self.outQuantityLbl= ttk.Label(frOutCurrency,font=('Helvetica',26),width=10,anchor=E)
        self.outQuantityLbl.pack(side=TOP,fill=X)

        self.outCurrencyCombo= ttk.Combobox(frOutCurrency,width=25,height=5,values=currencies ,textvariable=self.strOutCurrency)
        self.outCurrencyCombo.pack(side=TOP,fill=X)
        self.outCurrencyCombo.bind('<<ComboboxSelected>>',self.convertirDivisas)

        frOutCurrency.pack(side=LEFT,fill=BOTH,expand=TRUE)

    def validadCantidad(self,*args):
        try:
            v = float(self.strInQuantity.get())
            self.strOldInQuantity=v
            self.convertirDivisas
        except:
            self.strInQuantity.set(self.strOldInQuantity)

        
            
    def convertirDivisas(self,*args):
        print("in", self.strInCurrency.get())
        print("out",self.strOutCurrency.get())
        print("Cantidad",self.strInQuantity.get())

        base='EUR'
        _from=self.strInCurrency.get()
        _from=_from[0:3]
        _to=self.strOutCurrency.get()
        _to=to[:3]
        self.strInCurrency.get()
        symbols=_from+","+_to
        

        if self.strInCurrency.get() and self.strOutCurrency.get() and self.strInQuantity.get(): 

            print("Llama a fixer.io las dos veces")

            self.lblErrorMessages('Conectando...')  

            response=requests.get(self.rate_ep.format(self.api_key,base, symbols)

            

            if response.status_code == 200:
                data=json.loads(response.text)
                if data['succes']:
                    tasa_conversion=data['rates'][_from]
                    tasa_conversion2=data['rates'][_to]
                    self.lblErrorMessages.config(Text='')

                else:
                    msgError = data['error']['code'] + "-" + data['error']['type']
                    print(msgError)
            
            else:
                msgError= "Se ha producido un error en la consulta API: " + response.status_code
                print(msgError)
                self.lblErrorMessages.config(text=msgError)
                return
         
            #valor_label=Cantidad/tasa_conversion*tasa_conversion2

            valor_label=float(self.strInQuantity.get()/tasa_conversion*tasa_conversion2
            self.outQuantityLbl.config(text=valor_label)


    def getCurrencies(self):
        response = requests.get(self.all_symbols_ep.format(self.api_key))

        if response ==200:
            currencies= json.loads(response.txt)
            result=[]
            symbols=currencies['symbols']
            for symbol in symbols:
                text="{}-{}".format(symbol,symbols['symbol'])
                result.append(text)

            return result
        else:
                msgError= "Se ha producido un error en la consulta API: " + response.status_code
                print(msgError)
                self.lblErrorMessages.config(text=msgError)
                return

class MainApp(Tk):

     def __init__(self):
        Tk.__init__(self)
        self.geometry("400x150")
        self.title('Exchanger fixer.io')
        self.exchanger= Exchanger(self)
        self.exchanger.place(x=0,y=0)

     def start(self):
         self.mainloop()

if __name__=='__main__':
    exchanger=MainApp()
    exchanger.start()

