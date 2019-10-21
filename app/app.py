from PySide2 import QtWidgets
import currency_converter

class App(QtWidgets.QWidget) : 

    def __init__(self):
        super().__init__()
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("PyConverter")
        self.setup_ui()
        self.set_default_values()

    def setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout(self)
        self.cbb_devisesFrom = QtWidgets.QComboBox()
        self.spn_montant = QtWidgets.QSpinBox()
        self.cbb_devisesTo = QtWidgets.QComboBox()
        self.spn_montantConverti = QtWidgets.QSpinBox()
        self.btn_inverser = QtWidgets.QPushButton("Reverse currencies")

        self.layout.addWidget(self.cbb_devisesFrom)
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.cbb_devisesTo)
        self.layout.addWidget(self.spn_montantConverti)
        self.layout.addWidget(self.btn_inverser)

    def set_default_values(self):
        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesTo.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesFrom.setCurrentText("EUR")
        self.cbb_devisesTo.setCurrentText("USD")


        self.spn_montant.setRange(1, 1000000)
        self.spn_montantConverti.setRange(1,1000000)
        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)
        

app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()