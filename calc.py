import requests
from requests.api import get, head
from requests.models import Response
import locale #will be used to format 
# use user's default settings
locale.setlocale(locale.LC_ALL, 'en_US')

import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QFormLayout, QLineEdit, QPushButton, QHBoxLayout,
                             QGridLayout, QWidget, QMessageBox)

class Window(QMainWindow):
    def __init__(self):
        # super().__init__()
        QMainWindow.__init__(self)
        
        # layout for form elements
        self.form_elements = QFormLayout()
        self.label_sats = QLabel("USD amount")
        self.edit_sats = QLineEdit()
        self.form_elements.addRow(self.label_sats, self.edit_sats)
        self.button_calculate = QPushButton("Calculate")
        self.button_clear = QPushButton("Clear")

        # layout for form action buttons
        self.action_buttons = QHBoxLayout()
        self.action_buttons.addWidget(self.button_calculate)
        self.action_buttons.addWidget(self.button_clear)
        
        # Connecting the two methods below 
        self.button_calculate.clicked.connect(self.on_button_calc_click)
        self.button_clear.clicked.connect(self.on_button_clear_clicked)
        
        self.main_layout = QGridLayout()
        self.main_layout.addLayout(self.form_elements, 0, 0)
        self.main_layout.addLayout(self.action_buttons, 1, 0)        
        
        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        widget = QWidget()
        # widget.setStyleSheet('background-color: pink;')
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)
        self.setFixedSize(400, 200)
        
    def on_button_calc_click(self):
        # if the text feild is empty
        if self.edit_sats.text() == "" :
            QMessageBox.about(self, "Missing values",
                            "U$D box empty")
        else:
            # Grabs from the text box and converts into a float 
            usd = float(self.edit_sats.text()) # entered text from the text box 
            btc_price = float(self.calc_sats()) # convert to a float the bitcoin price 
            sats_conversion = float(usd/btc_price) # convert the usd amount entered / current price into a float
            sats_in_thousands = (sats_conversion * 100000000) # mutiply that result * 100,000,000 (100 million sats in a bitcoin)
            sats = locale.format_string("%d", sats_in_thousands, grouping= True) # Now we can format it so it reads nicely
            
            self.label_sats.setText(str(sats))

    
    def on_button_clear_clicked(self):
        self.edit_sats.setText(self.edit_sats.clear())
    
    def calc_sats(self):
        try:
                
                api_key = 'YOUR API KEY'
                api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
                headers = {
                    "Accepts" : 'application/json',
                    'X-CMC_PRO_API_KEY': api_key
                }
                response = requests.get(api_url,  headers= headers)
                response_json = response.json()
                btc_price = response_json['data'][0]
                exact_price = btc_price['quote']['USD']['price']
                return exact_price
                
        
        except ConnectionError as e:
            print(e)
             

def main(args):
    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) is fine.
    app = QApplication(args)
    # create the form
    application = Window()
    # set the form title
    application.setWindowTitle("U$D to Sats")
    # windows are hidden by default.
    application.show()
    # start the event loop.
    app.exec_()
    # Your application won't reach here until you exit and the event
    # loop has stopped.
if __name__ == "__main__":
    main(sys.argv)
