from PySide6.QtWidgets import (QWidget, QMainWindow)
from RDM_DMX_Master_ui import Ui_MainWindow

class RDM_DMX_Master(QWidget, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.setWindowTitle("RDM DMX Master")
        

        self.classe.activated.connect(self.ChangeParameter)
        self.send_command.clicked.connect(self.SendCommand)
        self.menuSair.triggered.connect(self.quit)

    def ChangeParameter(self):
        classe = self.classe.currentText()
        if(classe == "DISC"):
            self.parametro.clear()
            self.parametro.addItems(["Unique Branch","Mute","Unmute"])
                                   
        elif(classe == "GET"):
            self.parametro.clear()
            self.parametro.addItems(["Supported parameters","Parameter description","Device info", "Software version label", "DMX start address", "Identify device"])

        else:
            self.parametro.clear()
            self.parametro.addItems(["DMX start address","Identify device"])

    def SendCommand(self):
        classe = self.classe.currentText()
        parameter = self.parametro.currentText()
        destination_UID = self.destination_UID.displayText()
        source_UID = self.source_UID.displayText()
        sub_device = self.sub_device.displayText()
        port_id = self.port_ID.displayText()
        
        print(port_id)
        self.slave_Response.setText(source_UID)
        # Modo de escrever texto

    def quit(self):
        self.app.quit()