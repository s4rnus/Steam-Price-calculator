from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow ( QMainWindow ):

    def button_clicked( self ):
        print ( "Button clicked" )


    def __init__ ( self ):
        super().__init__()
        
        self.setWindowTitle ( "Steam USD|Price parser" )
        self.setMinimumSize ( 400,400 )

        button = QPushButton( "Press me!" )
        button.clicked.connect ( self.button_clicked )

        self.setCentralWidget( button )


app = QApplication ([])

window = MainWindow ()
window.show ()

app.exec ()