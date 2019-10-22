from PySide2 import QtWidgets
import currency_converter
import json

class App(QtWidgets.QWidget) : 

    def __init__(self):
        super().__init__()
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("PyConverter")
        self.setup_ui()
        self.set_default_values("./currencies.json")
        self.setup_connections()
       

    def setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout(self)
        self.cbb_devisesFrom = QtWidgets.QComboBox()
        self.spn_montant = QtWidgets.QDoubleSpinBox()
        self.cbb_devisesTo = QtWidgets.QComboBox()
        self.spn_montantConverti = QtWidgets.QDoubleSpinBox()
        self.btn_inverser = QtWidgets.QPushButton("Reverse currencies")
        self.currency_From = QtWidgets.QComboBox()

        self.layout.addWidget(self.cbb_devisesFrom)
        self.layout.addWidget(self.currency_From)
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.cbb_devisesTo)
        self.layout.addWidget(self.spn_montantConverti)
        self.layout.addWidget(self.btn_inverser)
        
    def setup_currency_list(self,file):
        with open (file, "r") as f :
          self.contenu = json.load(f) 
          return self.contenu
          

    def set_default_values(self,file):
        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesTo.addItems(sorted(list(self.c.currencies)))
        self.currency_From.addItems(sorted(list(self.setup_currency_list(file).values())))
        self.cbb_devisesFrom.setCurrentText("EUR")
        self.cbb_devisesTo.setCurrentText("USD")
        self.currency_From.setCurrentText("Euro")
        self.spn_montant.setRange(1, 1000000)
        self.spn_montantConverti.setRange(1,1000000)
        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)
        
        

    def setup_connections(self):
        self.cbb_devisesFrom.activated.connect(self.compute)
        self.cbb_devisesTo.activated.connect(self.compute)
        self.currency_From.activated.connect(self.compute_2)
        self.spn_montant.valueChanged.connect(self.compute)
        self.btn_inverser.clicked.connect(self.inverser_devise)

    def compute_2(self):
        montant = self.spn_montant.value()
        devise_name = self.currency_From.currentText()
        devise_abrg = self.setup_currency_list("./currencies_2.json").get(devise_name)
        self.cbb_devisesFrom.setCurrentText(devise_abrg)
        devise_to = self.cbb_devisesTo.currentText()
        try : 
            resultat = self.c.convert(montant, devise_abrg, devise_to)
        except currency_converter.currency_converter.RateNotFoundError : 
            print("The conversion didn't work")
        else : 
            self.spn_montantConverti.setValue(resultat)

    def compute(self):
        montant = self.spn_montant.value()
        devise_from = self.cbb_devisesFrom.currentText()
        devise_name = self.setup_currency_list("./currencies.json").get(devise_from)
        self.currency_From.setCurrentText(devise_name)
        devise_to = self.cbb_devisesTo.currentText()
        try : 
            resultat = self.c.convert(montant, devise_from, devise_to)
        except currency_converter.currency_converter.RateNotFoundError : 
            print("The conversion didn't work")
        else : 
            self.spn_montantConverti.setValue(resultat)

    def inverser_devise(self):
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()
        self.cbb_devisesFrom.setCurrentText(devise_to)
        self.cbb_devisesTo.setCurrentText(devise_from)
        self.compute()


app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()