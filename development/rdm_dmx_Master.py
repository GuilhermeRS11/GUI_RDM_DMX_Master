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

        # Aproveitando a chamada para atualizar os demais campos que devem ou não ser ativados

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
        # Anexa o valor das caixas de texto a 0x para poder converter posteriormente usando o "literal_eval"
        destination_UID = "0x" + self.destination_UID.displayText()
        source_UID = "0x" + self.source_UID.displayText()
        sub_device = "0x" + self.sub_device.displayText()
        port_id = "0x" + self.port_ID.displayText()
        additional_parameter = "0x" + self.additional_parameter.displayText()

        # Inicializa as caixas de texto caso o valor delas esteja vazio
        if destination_UID == "0x":
            destination_UID = "0x0"
        if source_UID == "0x":
            source_UID = "0x0"
        if sub_device == "0x":
            sub_device = "0x0"
        if port_id == "0x":
            port_id = "0x0"
        if additional_parameter == "0x":
            additional_parameter = "0x0"
            
        # Converte o valor das caixes de texto de str para int
        destination_UID = literal_eval(destination_UID)
        source_UID = literal_eval(source_UID)
        sub_device = literal_eval(sub_device)
        port_id = literal_eval(port_id)
        additional_parameter = literal_eval(additional_parameter)

        # Aproveitando a chamada para atualizar os demais campos que devem ou não ser ativados
        if(classe == "SET"):
            if(parameter == "DMX start address"):
                command2send = RDM.SET_dmx_start_address(destination_UID, source_UID, 0, port_id, sub_device, additional_parameter)
                self.additional_parameter.setEnabled(True) 
                self.sub_device.setEnabled(True)
            
            else: # Então é Identify device
                command2send = RDM.SET_identify_device(destination_UID, source_UID, 0, port_id, sub_device, additional_parameter)
                self.additional_parameter.setEnabled(True) 
                self.sub_device.setEnabled(True)
        
        elif(classe == "GET"):
            if(parameter == "Supported parameters"):
                command2send = RDM.GET_supported_parameters(destination_UID, source_UID, 0, port_id, sub_device)
                self.additional_parameter.setEnabled(False) 
                self.sub_device.setEnabled(True)

            elif(parameter == "Parameter description"):
                command2send = RDM.GET_parameter_description(destination_UID, source_UID, 0, port_id, additional_parameter)
                self.additional_parameter.setEnabled(True) 
                self.sub_device.setEnabled(False)

            elif(parameter == "Device info"):
                command2send = RDM.GET_device_info(destination_UID, source_UID, 0, port_id, sub_device)
                self.additional_parameter.setEnabled(False) 
                self.sub_device.setEnabled(True)

            elif(parameter == "Software version label"):
                command2send = RDM.GET_software_version_label(destination_UID, source_UID, 0, port_id, sub_device)
                self.additional_parameter.setEnabled(False) 
                self.sub_device.setEnabled(True)

            elif(parameter == "DMX start address"):
                command2send = RDM.GET_dmx_start_address(destination_UID, source_UID, 0, port_id, sub_device)
                self.additional_parameter.setEnabled(False) 
                self.sub_device.setEnabled(True)

            else:                       #(parameter == "Identify device"):
                command2send = RDM.GET_identify_device(destination_UID, source_UID, 0, port_id, sub_device)
                self.additional_parameter.setEnabled(False) 
                self.sub_device.setEnabled(True)
        
        else:   # Classe DISC
            if(parameter == "Unique Branch"):
                command2send = RDM.DISC_unique_branch(destination_UID, source_UID, 0, port_id, additional_parameter)
                self.additional_parameter.setEnabled(True) 
                self.sub_device.setEnabled(False)

            elif(parameter == "Mute"):
                command2send = RDM.DISC_mute(destination_UID, source_UID, 0, port_id)
                self.additional_parameter.setEnabled(False) 
                self.sub_device.setEnabled(False)

            else:                       # (parameter == "Unmute"):
                command2send = RDM.DISC_un_mute(destination_UID, source_UID, 0, port_id)
                self.additional_parameter.setEnabled(False) 
                self.sub_device.setEnabled(False)

        #self.slave_Response.setText(command2send)
        
        command_len = command2send[2] + 2 # Incluir caixa de texto para mostrar o tamanho do frame
        print(command_len)

        # Incluir caixa de texto extra para parametro adicional. O Disc unic branch precisa de dois

        # Separa cada byte do comando a ser enviado em cada caixa de texto correspondente
        self.command_1.setText(hex(command2send[0])[2:])
        self.command_2.setText(hex(command2send[1])[2:])
        self.command_3.setText(hex(command2send[2])[2:])
        self.command_4.setText(hex(command2send[3])[2:])
        self.command_5.setText(hex(command2send[4])[2:])
        self.command_6.setText(hex(command2send[5])[2:])
        self.command_7.setText(hex(command2send[6])[2:])
        self.command_8.setText(hex(command2send[7])[2:])
        self.command_9.setText(hex(command2send[8])[2:])
        self.command_10.setText(hex(command2send[9])[2:])
        self.command_11.setText(hex(command2send[10])[2:])
        self.command_12.setText(hex(command2send[11])[2:])
        self.command_13.setText(hex(command2send[12])[2:])
        self.command_14.setText(hex(command2send[13])[2:])
        self.command_15.setText(hex(command2send[14])[2:])
        self.command_16.setText(hex(command2send[15])[2:])
        self.command_17.setText(hex(command2send[16])[2:])
        self.command_18.setText(hex(command2send[17])[2:])
        self.command_19.setText(hex(command2send[18])[2:])
        self.command_20.setText(hex(command2send[19])[2:])
        self.command_21.setText(hex(command2send[20])[2:])
        self.command_22.setText(hex(command2send[21])[2:])
        self.command_23.setText(hex(command2send[22])[2:])
        self.command_24.setText(hex(command2send[23])[2:])
        if command_len > 24:
            self.command_25.setText(hex(command2send[24])[2:])
        if command_len > 25:
            self.command_26.setText(hex(command2send[25])[2:])
        if command_len > 26:
            self.command_27.setText(hex(command2send[26])[2:])
        if command_len > 27:
            self.command_28.setText(hex(command2send[27])[2:])
        if command_len > 28:
            self.command_29.setText(hex(command2send[28])[2:])
            self.command_30.setText(hex(command2send[29])[2:])
            self.command_31.setText(hex(command2send[30])[2:])
            self.command_32.setText(hex(command2send[31])[2:])
            self.command_33.setText(hex(command2send[32])[2:])
            self.command_34.setText(hex(command2send[33])[2:])
            self.command_35.setText(hex(command2send[34])[2:])
            self.command_36.setText(hex(command2send[35])[2:])
            self.command_37.setText(hex(command2send[36])[2:])
            self.command_38.setText(hex(command2send[37])[2:])

