from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, QTimer
from RDM_DMX_Master_ui import Ui_MainWindow
from ast import literal_eval

import RDM_backend as RDM
import serial
import time

Flag_just_once = True

# Inicializa parametro que sera compartilhado entre as funcoes
command2send = []
DMX_frame = []
serialComunication = serial.Serial(baudrate=500000, bytesize=8, timeout=2, stopbits=serial.STOPBITS_TWO)

class RDM_DMX_Master(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.setWindowTitle("RDM DMX Master")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.sendLastCommand)

        # Executa os camandos abaixo apenas na inicialização do app
        global Flag_just_once
        global Slots_per_link
        global Auto_DMX_send
        global elapsed_time, last_command_sent, startTime_for_tictoc

        if Flag_just_once:
            Flag_just_once = False
            Auto_DMX_send = False
            elapsed_time = 0
            last_command_sent = True
            startTime_for_tictoc = 0
    
            self.Slots_per_link.setValue(256)        # Inicializa o numero de slots por link com o valor 513
            self.serialFindPorts()                   # Faz a primeira busca pelas portas serial do sistema
            self.brightness_slider.setValue(255)     # Inicializa o brilho com o valor 100
            self.resolutionValues()                  # Inicializa a resolucao dos dados DMX
            self.brightnessSlider()                  # Inicializa o brilho 
            self.caixaCommand()                      # Atualiza os campos de exibicao com os valores zerados
            self.rgbSlider()                         # Atualiza os valores das cores atraves da posicao inicial do slider rgb
            self.assembleDMX()                       # Atualiza o comando a ser enviado no DMX   
            self.red_dmx_box.setValue(255)           # Inicializa a caixa de texto com o valor coerente


        """ 
        #############################################################################################
                                    Area de sensitividade do RDM_frontend
        #############################################################################################
        """

        # Identifica a ação dos principais elementos graficos
        self.classe.activated.connect(self.ChangeParameter)
        self.classe.activated.connect(self.caixaCommand)
        self.parametro.activated.connect(self.clearAddParam)
        self.parametro.activated.connect(self.caixaCommand)
        self.send_command.clicked.connect(self.SendCommand)
        self.menuSair.triggered.connect(self.quit)
        self.serialPort.activated.connect(self.changeSerialPort)

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

        self.refreshPorts.clicked.connect(self.serialFindPorts) # Atualiza as portar quando clicar no refresh

        """ 
        #############################################################################################
                                    Area de sensitividade do DMX_frontend
        #############################################################################################
        """

        self.resolution_values.activated.connect(self.reloadValuesAfterResolution)
        self.format_values.activated.connect(self.formatValues)
        self.brightness_slider.valueChanged.connect(self.brightnessSlider)

        self.white_dmx_box.valueChanged.connect(self.whiteBox)
        self.white_dmx_slider.valueChanged.connect(self.whiteSlider)
        self.blue_dmx_box.valueChanged.connect(self.blueBox)
        self.blue_dmx_slider.valueChanged.connect(self.blueSlider)
        self.red_dmx_box.valueChanged.connect(self.redBox)
        self.red_dmx_slider.valueChanged.connect(self.redSlider)
        self.green_dmx_box.valueChanged.connect(self.greenBox)
        self.green_dmx_slider.valueChanged.connect(self.greenSlider)
        self.RGB_dmx_slider.valueChanged.connect(self.rgbSlider)

        self.DMX_address.textChanged.connect(self.assembleDMX)
        self.Slots_per_link.valueChanged.connect(self.assembleDMX)
        #self.white_dmx_slider.valueChanged.connect(self.assembleDMX)
        #self.red_dmx_slider.valueChanged.connect(self.assembleDMX)
        #self.blue_dmx_slider.valueChanged.connect(self.assembleDMX)
        #self.green_dmx_slider.valueChanged.connect(self.assembleDMX)
        self.send_command_dmx.clicked.connect(self.sendDMXcommand)
        self.autoSend_dmx_command.stateChanged.connect(self.autoDMXcommand) 
        
        self.DMX_address.setPlaceholderText("1 - FF")  
        self.DMX_address.setMaxLength(2) # Define o limite de caracteres a serem digitados

        # Instanciação do timer para enviar comandando DMX automaticamente, espaçados de algum tempo
        self.last_dmx_command_time = 0
        # Instanciação da flag que indica se o commando é via RGB slidder. Serve para impedir que multiplas chamadas do assembleDMX()
        self.isRGB_slidder_command = False
        
    """ 
    #############################################################################################
                                            RDM_frontend
    #############################################################################################
    """

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
        global serialComunication
        serialComunication.close()
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
        self.command_1.setText(f"{command2send[0]:0{2}X}")
        self.command_2.setText(f"{command2send[1]:0{2}X}")
        self.command_3.setText(f"{command2send[2]:0{2}X}")
        self.command_4.setText(f"{command2send[3]:0{2}X}")
        self.command_5.setText(f"{command2send[4]:0{2}X}")
        self.command_6.setText(f"{command2send[5]:0{2}X}")
        self.command_7.setText(f"{command2send[6]:0{2}X}")
        self.command_8.setText(f"{command2send[7]:0{2}X}")
        self.command_9.setText(f"{command2send[8]:0{2}X}")
        self.command_10.setText(f"{command2send[9]:0{2}X}")
        self.command_11.setText(f"{command2send[10]:0{2}X}")
        self.command_12.setText(f"{command2send[11]:0{2}X}")
        self.command_13.setText(f"{command2send[12]:0{2}X}")
        self.command_14.setText(f"{command2send[13]:0{2}X}")
        self.command_15.setText(f"{command2send[14]:0{2}X}")
        self.command_16.setText(f"{command2send[15]:0{2}X}")
        self.command_17.setText(f"{command2send[16]:0{2}X}")
        self.command_18.setText(f"{command2send[17]:0{2}X}")
        self.command_19.setText(f"{command2send[18]:0{2}X}")
        self.command_20.setText(f"{command2send[19]:0{2}X}")
        self.command_21.setText(f"{command2send[20]:0{2}X}")
        self.command_22.setText(f"{command2send[21]:0{2}X}")
        self.command_23.setText(f"{command2send[22]:0{2}X}")
        self.command_24.setText(f"{command2send[23]:0{2}X}")
        if command_len > 24:
            self.command_25.setText(f"{command2send[24]:0{2}X}")
        if command_len > 25:
            self.command_26.setText(f"{command2send[25]:0{2}X}")
        if command_len > 26:
            self.command_27.setText(f"{command2send[26]:0{2}X}")
        if command_len > 27:
            self.command_28.setText(f"{command2send[27]:0{2}X}")
        if command_len > 28:
            self.command_29.setText(f"{command2send[28]:0{2}X}")
            self.command_30.setText(f"{command2send[29]:0{2}X}")
            self.command_31.setText(f"{command2send[30]:0{2}X}")
            self.command_32.setText(f"{command2send[31]:0{2}X}")
            self.command_33.setText(f"{command2send[32]:0{2}X}")
            self.command_34.setText(f"{command2send[33]:0{2}X}")
            self.command_35.setText(f"{command2send[34]:0{2}X}")
            self.command_36.setText(f"{command2send[35]:0{2}X}")
            self.command_37.setText(f"{command2send[36]:0{2}X}")
            self.command_38.setText(f"{command2send[37]:0{2}X}")

        # Define as tooltips de cada caixa de texto
        self.command_1.setToolTip("Start code")
        self.command_2.setToolTip("Sub Start code")
        self.command_3.setToolTip("Message Length")
        self.command_4.setToolTip("Destination UID byte 5")
        self.command_5.setToolTip("Destination UID byte 4")
        self.command_6.setToolTip("Destination UID byte 3")
        self.command_7.setToolTip("Destination UID byte 2")
        self.command_8.setToolTip("Destination UID byte 1")
        self.command_9.setToolTip("Destination UID byte 0")
        self.command_10.setToolTip("Source UID byte 5")
        self.command_11.setToolTip("Source UID byte 4")
        self.command_12.setToolTip("Source UID byte 3")
        self.command_13.setToolTip("Source UID byte 2")
        self.command_14.setToolTip("Source UID byte 1")
        self.command_15.setToolTip("Source UID byte 0")
        self.command_16.setToolTip("Transaction Number")
        self.command_17.setToolTip("Port ID / Response Type")
        self.command_18.setToolTip("Message Count")
        self.command_19.setToolTip("Sub Device byte 1")
        self.command_20.setToolTip("Sub Device byte 0")
        self.command_21.setToolTip("Command Class")
        self.command_22.setToolTip("Parameter ID byte 1")
        self.command_23.setToolTip("Parameter ID byte 0")
        self.command_24.setToolTip("Parameter Data Length")
                
        if command_len == 26:
            self.command_25.setToolTip("Checksum High")
            self.command_26.setToolTip("Checksum Low")
        
        if command_len == 27:
            self.command_25.setToolTip("Parameter Data")
            self.command_26.setToolTip("Checksum High")
            self.command_27.setToolTip("Checksum Low")

        if command_len == 28:
            self.command_25.setToolTip("Parameter Data byte 1")
            self.command_26.setToolTip("Parameter Data byte 0")
            self.command_27.setToolTip("Checksum High")
            self.command_28.setToolTip("Checksum Low")

        if command_len == 38:
            self.command_25.setToolTip("Parameter Data byte 11")
            self.command_26.setToolTip("Parameter Data byte 10")
            self.command_27.setToolTip("Parameter Data byte 9")
            self.command_28.setToolTip("Parameter Data byte 8")
            self.command_29.setToolTip("Parameter Data byte 7")
            self.command_30.setToolTip("Parameter Data byte 6")
            self.command_31.setToolTip("Parameter Data byte 5")
            self.command_32.setToolTip("Parameter Data byte 4")
            self.command_33.setToolTip("Parameter Data byte 3")
            self.command_34.setToolTip("Parameter Data byte 2")
            self.command_35.setToolTip("Parameter Data byte 1")
            self.command_36.setToolTip("Parameter Data byte 0")
            self.command_37.setToolTip("Checksum High")
            self.command_38.setToolTip("Checksum Low")

    

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

        self.command_24.setToolTip(" ")
        self.command_25.setToolTip(" ")
        self.command_26.setToolTip(" ")
        self.command_27.setToolTip(" ")
        self.command_28.setToolTip(" ")
        self.command_29.setToolTip(" ")
        self.command_30.setToolTip(" ")
        self.command_31.setToolTip(" ")
        self.command_32.setToolTip(" ")
        self.command_33.setToolTip(" ")
        self.command_34.setToolTip(" ")
        self.command_35.setToolTip(" ")
        self.command_36.setToolTip(" ")
        self.command_37.setToolTip(" ")
        self.command_38.setToolTip(" ")
        
    def SendCommand(self):
        global command2send
        global serialComunication
        
        # Faz o envio dos dados RDM
        serialComunication.write(bytes(command2send))
        print("Comando RDM enviado")

        # Faz o recebimento dos dados RDM
        receive = serialComunication.read(300)

        # Testa o recebimento de um frame de resposta a um Disc_unique_branch
        #receive = [0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0xaa, 0xba, 0x57, 0xbe, 0x75, 0xfe, 0x57, 0xfa, 0x7d, 0xba, 0xdf, 0xbe, 0xfd, 0xaa, 0x5d, 0xee, 0x75]

        # Testa o recebimento de um frame de resposta a um RDM padrao
        #receive = [0xcc, 0x01, 0x19, 0x12, 0x34, 0x56, 0x78, 0x9a, 0xbc, 0xcb, 0xa9, 0x87, 0x65, 0x43, 0x21, 0x00, 0x01, 0x00, 0x00, 0x00, 0x20, 0x00, 0x30, 0x01, 0x04, 0x06, 0x6a]
        self.responseProcess(receive)
        
    def responseProcess(self, receive):
        # Ajusta os dados recebidos para exibir na tela 
        self.slaveResponse.clear()

        if(len(receive) == 0):
        # Informa que nada foi recebido
            self.slaveResponse.addItem("Nenhum dado recebido")
            return
        
        elif receive[0] == 0xFE:
        # Processa frame de resposta a um Disc_unique_branch
            checksum = 0
            string_receive = "Frame recebido: "
            for i in range(len(receive)):
                string_receive = string_receive + f"{receive[i]:0{2}X}" + " "
                if i > 7 and i < 20:
                    checksum = checksum + receive[i]

            # Exibe o frame recebido
            self.slaveResponse.addItem(string_receive)

            # Exibe o numero de bytes recebidos
            string_receive = "Numero de bytes recebidos: " + str(len(receive))
            self.slaveResponse.addItem(string_receive)
            
            # Faz a decodificacao dos dados
            decodeData = [0, 0, 0, 0, 0, 0, 0, 0]
            decodeData[0] = receive[8] & receive[9]
            decodeData[1] = receive[10] & receive[11]
            decodeData[2] = receive[12] & receive[13]
            decodeData[3] = receive[14] & receive[15]
            decodeData[4] = receive[16] & receive[17]
            decodeData[5] = receive[18] & receive[19]
            decodeData[6] = receive[20] & receive[21]
            decodeData[7] = receive[22] & receive[23]

            string_receive = "Dados decodificados: "
            for i in range(8):
                string_receive = string_receive + f"{decodeData[i]:0{2}X}" + " "
            
            # Exibe os dados decodificados
            self.slaveResponse.addItem(string_receive)

            #print(checksum)
            #print(((decodeData[6] << 8) | decodeData[7]))
            if ((decodeData[6] << 8) | decodeData[7]) == checksum:
                string_receive = "Checksum: OK"
            else:
                string_receive = "Checksum: ERROR"
            
            # Exibe o resultado do checksum
            self.slaveResponse.addItem(string_receive)

            string_receive = "Source UID: "
            for i in range(6):
                string_receive = string_receive + f"{decodeData[i]:0{2}X}" + " "

            # Exibe o UID   
            self.slaveResponse.addItem(string_receive)

        elif receive[0] == 0xCC:
            checksum = 0
            string_receive = "Frame recebido: "
            frameSize = len(receive)

            for i in range(frameSize):
                string_receive = string_receive + f"{receive[i]:0{2}X}" + " "
                if (i % 27 == 0) and (i != 0): 
                    # Separa a linha quando tem mais de 27 elementos
                    self.slaveResponse.addItem(string_receive)
                    string_receive = "                           "

                if i < frameSize - 2:
                    # Calcula o checksum
                    checksum = checksum + receive[i]

            # Exibe o frame recebido
            self.slaveResponse.addItem(string_receive)

            # Exibe o numero de bytes recebidos
            string_receive = "Numero de bytes recebidos: " + str(frameSize)
            self.slaveResponse.addItem(string_receive)

            # Exibe o resultado do tamanho do frame
            if frameSize == receive[2] + 2:
                string_receive = "Tamanho do frame: OK"
            else:
                string_receive = "Tamanho do frame: ERROR"

            self.slaveResponse.addItem(string_receive)

            # Exibe o resultado do checksum
            if ((receive[frameSize - 2] << 8) | receive[frameSize - 1]) == checksum:
                string_receive = "Checksum: OK"
            else:
                string_receive = "Checksum: ERROR"

            self.slaveResponse.addItem(string_receive)

            # Exibe o UID
            string_receive = "Source UID: "
            for i in range(6):
                string_receive = string_receive + f"{receive[i + 9]:0{2}X}" + " "

            self.slaveResponse.addItem(string_receive)

            # Exibe o tipo de resposta
            if receive[16] == 0x00:
                string_receive = "Tipo de resposta: ACK"
            elif receive[16] == 0x01:
                string_receive = "Tipo de resposta: ACK_TIMER"
            elif receive[16] == 0x02:
                string_receive = "Tipo de resposta: NACK_REASON"
            elif receive[16] == 0x03:
                string_receive = "Tipo de resposta: ACK_OVERFLOW"

            self.slaveResponse.addItem(string_receive)

            # Exibe o tamanho do PD
            pdSize = receive[23]
            string_receive = "Tamanho do PD: " + str(pdSize)
            
            self.slaveResponse.addItem(string_receive)

            # Exibe o PD
            #if (receive[20] == 0x21) and (receive[21] == 0x00):
                #string_receive = "Endereço DMX: "
            #else:    
                #string_receive = "Parameter Data: "
            string_receive = "Parameter Data: "
            for i in range(pdSize):
                string_receive = string_receive + f"{receive[frameSize - 2 - pdSize + i]:0{2}X}" + " "
                if (i % 27 == 0) and (i != 0): 
                    # Separa a linha quando tem mais de 27 elementos
                    self.slaveResponse.addItem(string_receive)
                    string_receive = "                           "

            self.slaveResponse.addItem(string_receive)                        

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

    def serialFindPorts(self):
        ports = ['COM%s' % (i + 1) for i in range(256)]
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)                 # Coloca as portas encontradas em uma lista
            except (OSError, serial.SerialException):
                pass
            
        self.serialPort.clear()
        self.serialPort.addItems(result)    # Cria os itens da box com a lista      
                
    """ 
    #############################################################################################
                                            DMX_frontend
    #############################################################################################
    """
    
    def formatValues(self):
        if(self.format_values.currentText() == "Decimal"):
            self.resolutionValues()
            self.white_dmx_box.setValue(self.white_dmx_slider.value())
            self.blue_dmx_box.setValue(self.blue_dmx_slider.value())
            self.red_dmx_box.setValue(self.red_dmx_slider.value())
            self.green_dmx_box.setValue(self.green_dmx_slider.value())
        else: # Percentual
            self.white_dmx_box.setValue(round(100 * self.white_dmx_slider.value() / maxValue_onResolution))
            self.blue_dmx_box.setValue(round(100 * self.blue_dmx_slider.value() / maxValue_onResolution))
            self.red_dmx_box.setValue(round(100 * self.red_dmx_slider.value() / maxValue_onResolution))
            self.green_dmx_box.setValue(round(100 * self.green_dmx_slider.value() / maxValue_onResolution))
            self.resolutionValues() 
        
    def resolutionValues(self):
        global maxValue_onResolution
        if(self.resolution_values.currentText() == "8 bits"):
            # Seta todos os campos para terem 8 bits
            maxValue_onResolution = 255
            self.white_dmx_slider.setMaximum(255)
            self.blue_dmx_slider.setMaximum(255)
            self.green_dmx_slider.setMaximum(255)
            self.RGB_dmx_slider.setMaximum(256*3)
            self.red_dmx_slider.setMaximum(255)
            self.brightness_slider.setMaximum(255)

            if(self.format_values.currentText() == "Decimal"):
                self.white_dmx_box.setMaximum(255)
                self.blue_dmx_box.setMaximum(255)
                self.red_dmx_box.setMaximum(255)
                self.green_dmx_box.setMaximum(255)
            
            else: # Percentual
                self.white_dmx_box.setMaximum(100)
                self.blue_dmx_box.setMaximum(100)
                self.red_dmx_box.setMaximum(100)
                self.green_dmx_box.setMaximum(100)
                        
        else:
            # Seta todos os campos para terem 16 bits
            maxValue_onResolution = 65535
            self.white_dmx_box.setMaximum(65535)
            self.white_dmx_slider.setMaximum(65535)
            self.blue_dmx_box.setMaximum(65535)
            self.blue_dmx_slider.setMaximum(65535)
            self.red_dmx_box.setMaximum(65535)
            self.red_dmx_slider.setMaximum(65535)
            self.green_dmx_box.setMaximum(65535)
            self.green_dmx_slider.setMaximum(65535)
            self.brightness_slider.setMaximum(65535)
            self.RGB_dmx_slider.setMaximum(65536*3) 
            
            if(self.format_values.currentText() == "Decimal"):
                self.white_dmx_box.setMaximum(65535)
                self.blue_dmx_box.setMaximum(65535)
                self.red_dmx_box.setMaximum(65535)
                self.green_dmx_box.setMaximum(65535)
            
            else: # Percentual
                self.white_dmx_box.setMaximum(100)
                self.blue_dmx_box.setMaximum(100)
                self.red_dmx_box.setMaximum(100)
                self.green_dmx_box.setMaximum(100)

    def reloadValuesAfterResolution(self):
        # Atualiza os valores dos sliders e boxes apos alteração da resolução
        # Converte o valor de 8bits para 16bits e vice versa, mantendo a proporção, armazenando o valor atual antes de alterar a resolução
        RGBAtual = self.RGB_dmx_slider.value()
        brightnessAtual = self.brightness_slider.value()
     
        self.resolutionValues()
        if(self.resolution_values.currentText() == "8 bits"):
            maxValueOldResolution = 65535
                    
        else:
            maxValueOldResolution = 255

        self.brightness_slider.setValue(round(brightnessAtual * maxValue_onResolution / maxValueOldResolution))
        self.RGB_dmx_slider.setValue(round(RGBAtual * maxValue_onResolution / (maxValueOldResolution)))
           
    def whiteSlider(self):
        if(self.format_values.currentText() == "Percentual"):
            self.white_dmx_box.setValue(round(100 * self.white_dmx_slider.value() / maxValue_onResolution))

        else:
            self.white_dmx_box.setValue(self.white_dmx_slider.value())

        if(self.isRGB_slidder_command == False):
            self.assembleDMX()

    def whiteBox(self):
        if(self.format_values.currentText() == "Percentual"):
            self.white_dmx_slider.setValue(round(maxValue_onResolution * self.white_dmx_box.value() / 100))
        else:
            self.white_dmx_slider.setValue(self.white_dmx_box.value())
        

    def blueSlider(self):
        if(self.format_values.currentText() == "Percentual"):
            self.blue_dmx_box.setValue(round(100 * self.blue_dmx_slider.value() / maxValue_onResolution))  
        else:
            self.blue_dmx_box.setValue(self.blue_dmx_slider.value())
        if(self.isRGB_slidder_command == False):
            self.assembleDMX()

    def blueBox(self):
        if(self.format_values.currentText() == "Percentual"):
            self.blue_dmx_slider.setValue(round(maxValue_onResolution * self.blue_dmx_box.value() / 100))
        else:
            self.blue_dmx_slider.setValue(self.blue_dmx_box.value())

    def redSlider(self):
        if(self.format_values.currentText() == "Percentual"):
            self.red_dmx_box.setValue(round(100 * self.red_dmx_slider.value() / maxValue_onResolution))
        else:
            self.red_dmx_box.setValue(self.red_dmx_slider.value())
        if(self.isRGB_slidder_command == False):
            self.assembleDMX()

    def redBox(self):
        if(self.format_values.currentText() == "Percentual"):
            self.red_dmx_slider.setValue(round(maxValue_onResolution * self.red_dmx_box.value() / 100))
        else:
            self.red_dmx_slider.setValue(self.red_dmx_box.value())

    def greenSlider(self):
        if(self.format_values.currentText() == "Percentual"):
            self.green_dmx_box.setValue(round(100 * self.green_dmx_slider.value() / maxValue_onResolution))  
        else:
            self.green_dmx_box.setValue(self.green_dmx_slider.value())
        if(self.isRGB_slidder_command == False):
            self.assembleDMX()

    def greenBox(self):
        if(self.format_values.currentText() == "Percentual"):
            self.green_dmx_slider.setValue(round(maxValue_onResolution * self.green_dmx_box.value() / 100))
        else:
            self.green_dmx_slider.setValue(self.green_dmx_box.value())

    def rgbSlider(self):
        rgb = self.RGB_dmx_slider.value()

        if rgb < maxValue_onResolution:
            red = round((maxValue_onResolution - rgb) * brightness)
            blue = 0
            green = round((rgb) * brightness)

        elif rgb < maxValue_onResolution * 2 + 1:
            red = 0
            blue = round((rgb - maxValue_onResolution) * brightness)
            green = round((maxValue_onResolution * 2 + 1 - rgb) * brightness)

        else:
            red = round((rgb - maxValue_onResolution * 2 + 1) * brightness)
            blue = round((maxValue_onResolution * 3 + 2 - rgb) * brightness)
            green = 0

        self.isRGB_slidder_command = True # Ativa a flag para não chamar a função assembleDMX() durante a alteração dos sliders
        self.red_dmx_slider.setValue(red)
        self.blue_dmx_slider.setValue(blue)
        self.green_dmx_slider.setValue(green)
        self.white_dmx_slider.setValue(0)
        self.assembleDMX()

    def brightnessSlider(self):
        global brightness
        brightness = self.brightness_slider.value() / maxValue_onResolution # Valor máximo que podem assumir
        self.brightness_percentage_box.setText(str(round(brightness * 100)) + "%")
        # Atualiza os valores dos sliders e boxes apos alteração do brilho
        self.rgbSlider()

    def assembleDMX(self):
        # Monta o quadro DMX 
        global DMX_frame
        global Slots_per_link
        global Auto_DMX_send 

        # Adiciona cabeçalho e rodapé que são especificos para essa interface se comunicar com módulo DMX
        Module_header = [0x7E, 0x06, 0x3A]
        Module_tail = [0x7E, 0x06, 0x3B]
       
        DMX_address = "0x" + self.DMX_address.displayText()
        if DMX_address == "0x":
            DMX_address = "0x0"

        Slots_per_link = self.Slots_per_link.value()
        white_value = self.white_dmx_slider.value()
        blue_value = self.blue_dmx_slider.value()
        green_value = self.green_dmx_slider.value()
        red_value = self.red_dmx_slider.value()

        # Define o tamanho do frame a ser enviado e adapta para caber um 2 bytes
        frame_size = Slots_per_link + 3
        Module_frame_size = [frame_size >> 8, frame_size & 0xFF]  # Separa o Module_frame_size em dois bytes
       
        DMX_frame.clear()     # Limpa o conteudo do frame antes de atribuir qualquer valor

        # Adiciona o header e o tamanho do frame ao module frame
        DMX_frame.append(Module_header[0])
        DMX_frame.append(Module_header[1])
        DMX_frame.append(Module_header[2])
        DMX_frame.append(Module_frame_size[0])
        DMX_frame.append(Module_frame_size[1])

        for i in range(Slots_per_link):
        # Inicializa o frame de envio do DMX
            DMX_frame.append(0x0)

        if (literal_eval(DMX_address)) and (literal_eval(DMX_address) < Slots_per_link - 2):
            # Adiciona o valor das cores no endereco solicitado (+5 para compensar header e o tamanho de frame)
            DMX_frame[literal_eval(DMX_address) + 5] = white_value
            DMX_frame[literal_eval(DMX_address) + 5 + 1] = green_value
            DMX_frame[literal_eval(DMX_address) + 5 + 2] = blue_value
            DMX_frame[literal_eval(DMX_address) + 5 + 3] = red_value  

        # Adiciona o tail ao module frame
        DMX_frame.append(Module_tail[0])
        DMX_frame.append(Module_tail[1])
        DMX_frame.append(Module_tail[2])

        # Inicializa a label de comando a ser iniciado
        self.DMX_command_label.clear()
        DMX_frame_show = "000 - 00"
        
        for i in range(2, Slots_per_link + 1):
            # Mostra o frame DMX a ser enviado                
            DMX_frame_show = DMX_frame_show + " " + f"{DMX_frame[i-1+5]:0{2}X}"
            if ((i % 32 == 0) and (i != 1) and (i != 0)) or (i == Slots_per_link):
                # Separa a impressao em grupos de 30 bytes
                self.DMX_command_label.addItem(DMX_frame_show)
                DMX_frame_show = f"{i:0{3}}" + " -"

        if Auto_DMX_send:
            # Envia automaticamente os comandos se a caixa estiver marcada e verifica se já é tempo de enviar para a serial 
            global elapsed_time, last_command_sent
            current_time = time.time() * 1000  # Get the current time in milliseconds
            elapsed_time = current_time - self.last_dmx_command_time

            #if elapsed_time > 1: Caso precise habilitar um tempo de delay entre um comando e outro
            self.sendDMXcommand()
            self.last_dmx_command_time = current_time
            last_command_sent = False
            self.timer.stop()
            self.timer.start(1) # Inicia o timer que verifica se o ultimo comando foi enviado
                                    # Se ainda há comando a serem enviados ele reinicia o timer
                
            
    def sendLastCommand(self):
        # Envia o ultimo comando DMX enviado após passar o tempo de espera, para garantir que o ultimo comando seja o ultimo montado
        if(Auto_DMX_send):
            global elapsed_time, last_command_sent
            current_time = time.time() * 1000
            if (current_time - elapsed_time > 40 and not(last_command_sent)):
                self.sendDMXcommand()
                last_command_sent = True
                print("Ultimo comando enviado")
                self.timer.stop()

    def sendDMXcommand(self): 
        # Envia frame DMX por serial
        self.isRGB_slidder_command = False # Desativa a flag para permitir a chamada da função assembleDMX() durante a alteração dos sliders
        serialComunication.write(bytes(DMX_frame))
        print("Comando DMX enviado")

    def autoDMXcommand(self):
        global Auto_DMX_send
        # Envia automaticamente os comandos 
        if self.autoSend_dmx_command.isChecked():
            # Se estiver marcado 
            self.send_command_dmx.setEnabled(False)
            Auto_DMX_send = True
        else:
            # Se nao estiver marcado
            self.send_command_dmx.setEnabled(True)
            Auto_DMX_send = False

    def tic(self):    
        global startTime_for_tictoc
        startTime_for_tictoc = time.time()

    def toc(self):
        print("Elapsed time is ",(time.time() - startTime_for_tictoc)*1000," miliseconds.")

    def changeSerialPort(self):
    # Altera a porta serial de acordo com a selecionada
        global serialComunication
        serialComunication.close()
        serialComunication = serial.Serial(port=self.serialPort.currentText(), baudrate=500000,
                                        bytesize=8, timeout=2, stopbits=serial.STOPBITS_TWO)
        