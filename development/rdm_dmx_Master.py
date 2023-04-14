from PySide6.QtWidgets import (QWidget, QMainWindow)
from RDM_DMX_Master_ui import Ui_MainWindow
import RDM
from ast import literal_eval

class RDM_DMX_Master(QWidget, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.setWindowTitle("RDM DMX Master")

        self.classe.activated.connect(self.ChangeParameter)
        self.send_command.clicked.connect(self.SendCommand)
        self.menuSair.triggered.connect(self.quit)

        # Atualização dos bytes das caixas de exibição
        self.destination_UID.textEdited.connect(self.caixaCommand)
        self.source_UID.textEdited.connect(self.caixaCommand)
        self.sub_device.textEdited.connect(self.caixaCommand)
        self.port_ID.textEdited.connect(self.caixaCommand)

    def ChangeParameter(self):
        classe = self.classe.currentText()
        if(classe == "DISC"):
            self.parametro.clear()
            self.parametro.addItems(["Unique Branch","Mute","Unmute"])
            self.additional_parameter.setEnabled(False) # Faz com que o parametro adicional não esteja disponivel para edição
                                   
        elif(classe == "GET"):
            self.parametro.clear()
            self.parametro.addItems(["Supported parameters","Parameter description","Device info", "Software version label", "DMX start address", "Identify device"])
            self.additional_parameter.setEnabled(False) 

        else:   # Então é comando SET
            self.parametro.clear()
            self.parametro.addItems(["DMX start address","Identify device"])
            self.additional_parameter.setEnabled(True) 

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

    def caixaCommand(self):
        classe = self.classe.currentText()
        parameter = self.parametro.currentText()
        destination_UID = "0x" + (self.destination_UID.displayText())
        print(destination_UID)
        source_UID = "0x" + self.source_UID.displayText()
        sub_device = "0x" + self.sub_device.displayText()
        port_id = "0x" + self.port_ID.displayText()
        additional_parameter = "0x" + self.additional_parameter.displayText()

        if not destination_UID:
            destination_UID = 0x0
        if not source_UID:
            source_UID = 0x0
        if not sub_device:
            sub_device = 0x0
        if not port_id:
            port_id = 0x0
        if not additional_parameter:
            additional_parameter = 0x0
            
        destination_UID = literal_eval(destination_UID)
        print(type(destination_UID))
        print(destination_UID)
        source_UID = literal_eval(source_UID)
        sub_device = literal_eval(sub_device)
        port_id = literal_eval(port_id)
        additional_parameter = literal_eval(additional_parameter)

        if(classe == "SET"):
            if(parameter == "DMX start address"):
                command2send = RDM.SET_dmx_start_address(destination_UID, source_UID, 0, port_id, sub_device, additional_parameter)
            
            else: # Então é Identify device
                command2send = RDM.SET_identify_device(destination_UID, source_UID, 0, port_id, sub_device, additional_parameter)
        
        elif(classe == "GET"):
            if(parameter == "Supported parameters"):
                command2send = RDM.GET_supported_parameters(destination_UID, source_UID, 0, port_id, sub_device)

            elif(parameter == "Parameter description"):
                command2send = RDM.GET_parameter_description(destination_UID, source_UID, 0, port_id, additional_parameter)

            elif(parameter == "Device info"):
                command2send = RDM.GET_device_info(destination_UID, source_UID, 0, port_id, sub_device)

            elif(parameter == "Software version label"):
                command2send = RDM.GET_software_version_label(destination_UID, source_UID, 0, port_id, sub_device)

            elif(parameter == "DMX start address"):
                command2send = RDM.GET_dmx_start_address(destination_UID, source_UID, 0, port_id, sub_device)

            else:                       #(parameter == "Identify device"):
                command2send = RDM.GET_identify_device(destination_UID, source_UID, 0, port_id, sub_device)
        
        else:   # Classe DISC
            if(parameter == "Unique Branch"):
                command2send = RDM.DISC_unique_branch(destination_UID, source_UID, 0, port_id, additional_parameter)
            elif(parameter == "Mute"):
                command2send = RDM.DISC_mute(destination_UID, source_UID, 0, port_id)
            else:                       # (parameter == "Unmute"):
                command2send = RDM.DISC_un_mute(destination_UID, source_UID, 0, port_id)

        #self.slave_Response.setText(command2send)
        self.command_1.setText(hex(command2send[0]))