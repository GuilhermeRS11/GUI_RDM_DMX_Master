from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from RDM_DMX_Master_ui import Ui_MainWindow
from ast import literal_eval

import RDM
import serial

Flag_just_once = True
serialPort = serial.Serial(port = "COM7", baudrate=9600,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_TWO)

# Inicializa parametro que sera compartilhado entre as funcoes
command2send = []

class RDM_DMX_Master(QWidget, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.setWindowTitle("RDM DMX Master")

        # Executa os camandos abaixo apenas na inicialização do app
        global Flag_just_once
        if Flag_just_once:
            Flag_just_once = False
            self.caixaCommand()

        self.classe.activated.connect(self.ChangeParameter)
        self.classe.activated.connect(self.caixaCommand)
        self.parametro.activated.connect(self.clearAddParam)
        self.parametro.activated.connect(self.caixaCommand)
        self.send_command.clicked.connect(self.SendCommand)
        self.menuSair.triggered.connect(self.quit)

        # Atualização dos bytes das caixas de exibição
        self.destination_UID.textEdited.connect(self.caixaCommand)
        self.source_UID.textEdited.connect(self.caixaCommand)
        self.sub_device.textEdited.connect(self.caixaCommand)
        self.port_ID.textEdited.connect(self.caixaCommand)
        self.add_param_1.textEdited.connect(self.caixaCommand)
        self.add_param_2.textEdited.connect(self.caixaCommand)

        # Definição do numero maximo de caracteres em cada parametro
        self.source_UID.setMaxLength(12)
        self.destination_UID.setMaxLength(12)
        self.port_ID.setMaxLength(2)
        self.sub_device.setMaxLength(4) # É preciso especificar o range deste em cada comando

        self.port_ID.setPlaceholderText("01 - FF")
        self.source_UID.setPlaceholderText("0 - FFFFFFFFFFFF")
        self.destination_UID.setPlaceholderText("0 - FFFFFFFFFFFF")

        self.alignement_labels() # Alinha as caixas de comando ao centro

        
    def ChangeParameter(self):
        classe = self.classe.currentText()
        self.clearAddParam() # Zera as caixas dos parametros extras
        
        # Aproveitando a chamada para atualizar os demais campos que devem ou não ser ativados
        if(classe == "DISC"):
            self.parametro.clear()
            self.parametro.addItems(["Unique Branch","Mute","Unmute"]) 
                                   
        elif(classe == "GET"):
            self.parametro.clear()
            self.parametro.addItems(["Supported parameters","Parameter description","Device info", "Software version label", "DMX start address", "Identify device"])

        else:   # Então é comando SET
            self.parametro.clear()
            self.parametro.addItems(["DMX start address","Identify device"])

    def quit(self):
        serialPort.close()
        self.app.quit()

    def caixaCommand(self):
        global command2send

        classe = self.classe.currentText()
        parameter = self.parametro.currentText()

        self.clearBoxes() # Zera as caixas de texto antes de escrever qualquer coisa

        # Anexa o valor das caixas de texto a 0x para poder converter posteriormente usando o "literal_eval"
        destination_UID = "0x" + self.destination_UID.displayText()
        source_UID = "0x" + self.source_UID.displayText()
        sub_device = "0x" + self.sub_device.displayText()
        port_id = "0x" + self.port_ID.displayText()
        # Parametro adicionais que são usados apenas em alguns comandos, e variam dependendo do comando
        add_param_1 = "0x" + self.add_param_1.displayText()
        add_param_2 = "0x" + self.add_param_2.displayText()
        TN = 0 # Até o momento não foi implementado, então coloquei o valor padrão como 0

        # Inicializa as caixas de texto caso o valor delas esteja vazio
        if destination_UID == "0x":
            destination_UID = "0x0"
        if source_UID == "0x":
            source_UID = "0x0"
        if sub_device == "0x":
            sub_device = "0x0"
        if port_id == "0x":
            port_id = "0x0"
        if add_param_1 == "0x":
            add_param_1 = "0x0"
        if add_param_2 == "0x":
            add_param_2 = "0x0"
            
        # Converte o valor das caixes de texto de str para int
        destination_UID = literal_eval(destination_UID)
        source_UID = literal_eval(source_UID)
        sub_device = literal_eval(sub_device)
        port_id = literal_eval(port_id)
        add_param_1 = literal_eval(add_param_1)
        add_param_2 = literal_eval(add_param_2)

        # Aproveitando a chamada para atualizar os demais campos que devem ou não ser ativados
        if(classe == "SET"):
            if(parameter == "DMX start address"):
                command2send = RDM.SET_dmx_start_address(destination_UID, source_UID, TN, port_id, sub_device, add_param_1)
                self.add_param_1.setEnabled(True) 
                self.add_param_2.setEnabled(False)
                self.add_param_1_label.setText("Endereço DMX")
                self.add_param_1.setPlaceholderText("1 - 200")
                self.sub_device.setPlaceholderText("0 - 0200 ou FFFF")

                self.add_param_1.setMaxLength(4)
                self.sub_device.setEnabled(True)
            
            else: # Então é Identify device
                command2send = RDM.SET_identify_device(destination_UID, source_UID, TN, port_id, sub_device, add_param_1)
                self.add_param_1.setEnabled(True)
                self.add_param_2.setEnabled(False)  
                self.add_param_1_label.setText("Stop/Start (0/1)")
                self.add_param_1.setMaxLength(1)
                self.add_param_1.setPlaceholderText("0 ou 1")
                self.sub_device.setPlaceholderText("0 - 0200 ou FFFF")

                self.sub_device.setEnabled(True)
        
        elif(classe == "GET"):
            if(parameter == "Supported parameters"):
                command2send = RDM.GET_supported_parameters(destination_UID, source_UID, TN, port_id, sub_device)
                self.add_param_1.setEnabled(False) 
                self.add_param_2.setEnabled(False)
                self.clearAddParam()
                self.sub_device.setPlaceholderText("0 - 0200")
                self.sub_device.setEnabled(True)

            elif(parameter == "Parameter description"):
                command2send = RDM.GET_parameter_description(destination_UID, source_UID, TN, port_id, add_param_1)
                self.add_param_1.setEnabled(True) 
                self.add_param_2.setEnabled(False)
                self.add_param_1_label.setText("PID")
                self.add_param_1.setPlaceholderText("8000 - FFDF")
                self.add_param_1.setMaxLength(4)
                self.sub_device.setEnabled(False)
                self.sub_device.setPlaceholderText("")
                self.sub_device.setText("")

            elif(parameter == "Device info"):
                command2send = RDM.GET_device_info(destination_UID, source_UID, TN, port_id, sub_device)
                self.add_param_1.setEnabled(False)
                self.add_param_2.setEnabled(False)
                self.clearAddParam() 
                self.sub_device.setPlaceholderText("0 - 0200")
                self.sub_device.setEnabled(True)

            elif(parameter == "Software version label"):
                command2send = RDM.GET_software_version_label(destination_UID, source_UID, TN, port_id, sub_device)
                self.add_param_1.setEnabled(False)
                self.add_param_2.setEnabled(False)
                self.clearAddParam()   
                self.sub_device.setPlaceholderText("0 - 0200")
                self.sub_device.setEnabled(True)

            elif(parameter == "DMX start address"):
                command2send = RDM.GET_dmx_start_address(destination_UID, source_UID, TN, port_id, sub_device)
                self.add_param_1.setEnabled(False) 
                self.add_param_2.setEnabled(False)
                self.clearAddParam()  
                self.sub_device.setPlaceholderText("0 - 0200")
                self.sub_device.setEnabled(True)

            else:                       #(parameter == "Identify device"):
                command2send = RDM.GET_identify_device(destination_UID, source_UID, TN, port_id, sub_device)
                self.add_param_1.setEnabled(False)
                self.add_param_2.setEnabled(False) 
                self.clearAddParam()  
                self.sub_device.setPlaceholderText("0 - 0200")
                self.sub_device.setEnabled(True)
        
        else:   # Classe DISC
            if(parameter == "Unique Branch"):
                command2send = RDM.DISC_unique_branch(destination_UID, source_UID, TN, port_id, add_param_1, add_param_2)
                self.add_param_1.setEnabled(True) 
                self.add_param_2.setEnabled(True)
                self.add_param_1_label.setText("LB ID")
                self.add_param_2_label.setText("UB ID")
                self.add_param_1.setPlaceholderText("0 - FFFFFFFFFFFF")
                self.add_param_2.setPlaceholderText("0 - FFFFFFFFFFFF")  
                self.add_param_1.setMaxLength(12) # Define o limite de caracteres a serem digitados
                self.add_param_2.setMaxLength(12)
                self.sub_device.setEnabled(False)
                self.sub_device.setText("")
                self.sub_device.setPlaceholderText("")

            elif(parameter == "Mute"):
                command2send = RDM.DISC_mute(destination_UID, source_UID, TN, port_id)
                self.add_param_1.setEnabled(False)
                self.add_param_2.setEnabled(False)
                self.clearAddParam()   
                self.sub_device.setEnabled(False)
                self.sub_device.setText("")
                self.sub_device.setPlaceholderText("")

            else:                       # (parameter == "Unmute"):
                command2send = RDM.DISC_un_mute(destination_UID, source_UID, TN, port_id)
                self.add_param_1.setEnabled(False) 
                self.add_param_2.setEnabled(False)
                self.clearAddParam()
                self.sub_device.setEnabled(False)
                self.sub_device.setText("")
                self.sub_device.setPlaceholderText("")

        #self.slave_Response.setText(command2send)
        
        command_len = command2send[2] + 2 # Incluir caixa de texto para mostrar o tamanho do frame
        self.frame_size.setText(str(command_len))

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

    def clearBoxes(self):
        self.command_25.setText(" ")
        self.command_26.setText(" ")
        self.command_27.setText(" ")
        self.command_28.setText(" ")
        self.command_29.setText(" ")
        self.command_30.setText(" ")
        self.command_31.setText(" ")
        self.command_32.setText(" ")
        self.command_33.setText(" ")
        self.command_34.setText(" ")
        self.command_35.setText(" ")
        self.command_36.setText(" ")
        self.command_37.setText(" ")
        self.command_38.setText(" ")

    def SendCommand(self):
        global command2send

        # Envia os dados via serial byte a byte
        for i in range(command2send[2] + 2):
            serialPort.write(hex(command2send[i])[2:].encode('Ascii'))
            
        receive = serialPort.read()
        print(receive.decode('Ascii'))
        #serialPort.close()

    def clearAddParam(self):
        self.add_param_1.setText("")
        self.add_param_2.setText("")
        self.add_param_1_label.setText(" ")
        self.add_param_2_label.setText(" ")
        self.add_param_1.setPlaceholderText("")
        self.add_param_2.setPlaceholderText("")
    
    def alignement_labels(self):
        # Alinha as caixas de comando ao centro
        self.add_param_1_label.setAlignment(Qt.AlignRight)
        self.add_param_2_label.setAlignment(Qt.AlignRight)

        self.command_1.setAlignment(Qt.AlignCenter)
        self.command_2.setAlignment(Qt.AlignCenter)
        self.command_3.setAlignment(Qt.AlignCenter)
        self.command_4.setAlignment(Qt.AlignCenter)
        self.command_5.setAlignment(Qt.AlignCenter)
        self.command_6.setAlignment(Qt.AlignCenter)
        self.command_7.setAlignment(Qt.AlignCenter)
        self.command_8.setAlignment(Qt.AlignCenter)
        self.command_9.setAlignment(Qt.AlignCenter)
        self.command_10.setAlignment(Qt.AlignCenter)
        self.command_11.setAlignment(Qt.AlignCenter)
        self.command_12.setAlignment(Qt.AlignCenter)
        self.command_13.setAlignment(Qt.AlignCenter)
        self.command_14.setAlignment(Qt.AlignCenter)
        self.command_15.setAlignment(Qt.AlignCenter)
        self.command_16.setAlignment(Qt.AlignCenter)
        self.command_17.setAlignment(Qt.AlignCenter)
        self.command_18.setAlignment(Qt.AlignCenter)
        self.command_19.setAlignment(Qt.AlignCenter)
        self.command_20.setAlignment(Qt.AlignCenter)
        self.command_21.setAlignment(Qt.AlignCenter)
        self.command_22.setAlignment(Qt.AlignCenter)
        self.command_23.setAlignment(Qt.AlignCenter)
        self.command_24.setAlignment(Qt.AlignCenter)
        self.command_25.setAlignment(Qt.AlignCenter)
        self.command_26.setAlignment(Qt.AlignCenter)
        self.command_27.setAlignment(Qt.AlignCenter)
        self.command_28.setAlignment(Qt.AlignCenter)
        self.command_29.setAlignment(Qt.AlignCenter)
        self.command_30.setAlignment(Qt.AlignCenter)
        self.command_31.setAlignment(Qt.AlignCenter)
        self.command_32.setAlignment(Qt.AlignCenter)
        self.command_33.setAlignment(Qt.AlignCenter)
        self.command_34.setAlignment(Qt.AlignCenter)
        self.command_35.setAlignment(Qt.AlignCenter)
        self.command_36.setAlignment(Qt.AlignCenter)
        self.command_37.setAlignment(Qt.AlignCenter)
        self.command_38.setAlignment(Qt.AlignCenter)
        self.command_39.setAlignment(Qt.AlignCenter)
        self.command_40.setAlignment(Qt.AlignCenter)