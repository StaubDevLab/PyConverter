from PySide2 import QtWidgets
import currency_converter
import json

class App(QtWidgets.QWidget) : 

    def __init__(self):
        super().__init__()
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("PyConverter")
        self.setup_ui()
        self.set_default_values()
        self.setup_connections()
       

    def setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout(self)
        self.cbb_devisesFrom = QtWidgets.QComboBox()
        self.spn_montant = QtWidgets.QDoubleSpinBox()
        self.cbb_devisesTo = QtWidgets.QComboBox()
        self.spn_montantConverti = QtWidgets.QDoubleSpinBox()
        self.btn_inverser = QtWidgets.QPushButton("Reverse currencies")
        self.cbb_currency_long_From = QtWidgets.QComboBox()
        self.cbb_currency_long_To = QtWidgets.QComboBox()

        self.layout.addWidget(self.cbb_devisesFrom)
        self.layout.addWidget(self.cbb_currency_long_From)
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.cbb_devisesTo)
        self.layout.addWidget(self.cbb_currency_long_To)
        self.layout.addWidget(self.spn_montantConverti)
        self.layout.addWidget(self.btn_inverser)
        
    def setup_currency_list(self,file):
        with open (file, "r") as f :
          self.contenu = json.load(f) 
          return self.contenu
          

    def set_default_values(self):
        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesTo.addItems(sorted(list(self.c.currencies)))
        self.cbb_currency_long_From.addItems(sorted(list(self.setup_currency_list("./datas/currencies.json").values())))
        self.cbb_currency_long_To.addItems(sorted(list(self.setup_currency_list("./datas/currencies.json").values())))
        self.cbb_devisesFrom.setCurrentText("EUR")
        self.cbb_devisesTo.setCurrentText("USD")
        self.cbb_currency_long_From.setCurrentText("Euro")
        self.cbb_currency_long_To.setCurrentText("Dollar")
        self.spn_montant.setRange(1, 1000000)
        self.spn_montantConverti.setRange(1,1000000)
        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)
        

    def setup_connections(self):
        self.cbb_devisesFrom.activated.connect(self.compute)
        self.cbb_devisesTo.activated.connect(self.compute)
        self.cbb_currency_long_From.activated.connect(self.compute_2)
        self.cbb_currency_long_To.activated.connect(self.compute_2)
        self.spn_montant.valueChanged.connect(self.compute)
        self.btn_inverser.clicked.connect(self.inverser_devise)

    def compute_2(self):
        montant = self.spn_montant.value()
        devise_From_name = self.cbb_currency_long_From.currentText()
        devise_From_abrg = self.setup_currency_list("./datas/currencies_2.json").get(devise_From_name)
        devise_To_name = self.cbb_currency_long_To.currentText()
        devise_To_abrg = self.setup_currency_list("./datas/currencies_2.json").get(devise_To_name)
        self.cbb_devisesFrom.setCurrentText(devise_From_abrg)
        self.cbb_devisesTo.setCurrentText(devise_To_abrg)
        try : 
            resultat = self.c.convert(montant, devise_From_abrg, devise_To_abrg)
        except currency_converter.currency_converter.RateNotFoundError : 
            print("The conversion didn't work")
        else : 
            self.spn_montantConverti.setValue(resultat)

    def compute(self):
        montant = self.spn_montant.value()
        devise_from = self.cbb_devisesFrom.currentText()
        devise_From_name = self.setup_currency_list("./datas/currencies.json").get(devise_from)
        self.cbb_currency_long_From.setCurrentText(devise_From_name)
        devise_to = self.cbb_devisesTo.currentText()
        devise_To_name = self.setup_currency_list("./datas/currencies.json").get(devise_to)
        self.cbb_currency_long_To.setCurrentText(devise_To_name)
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