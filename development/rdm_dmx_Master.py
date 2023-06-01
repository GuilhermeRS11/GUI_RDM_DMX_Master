from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from RDM_DMX_Master_ui import Ui_MainWindow
from ast import literal_eval

import RDM_backend as RDM
import serial

Flag_just_once = True

# Inicializa parametro que sera compartilhado entre as funcoes
command2send = []
DMX_frame = []
serialComunication = serial.Serial(baudrate=250000, bytesize=8, timeout=2, stopbits=serial.STOPBITS_TWO)

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
            self.serialFindPorts()      # Faz a primeira busca pelas portas serial do sistema
            self.caixaCommand()         # Atualiza os campos de exibicao com os valores zerados
            self.rgbSlider()            # Atualiza os valores das cores atraves da posicao inicial do slider rgb
            self.assembleDMX()          # Atualiza o comando a ser enviado no DMX


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
        self.white_dmx_box.textChanged.connect(self.assembleDMX)
        self.red_dmx_box.textChanged.connect(self.assembleDMX)
        self.blue_dmx_box.textChanged.connect(self.assembleDMX)
        self.green_dmx_box.textChanged.connect(self.assembleDMX)
        self.send_command_dmx.clicked.connect(self.sendDMXcommand)
        self.autoSend_dmx_command.stateChanged.connect(self.autoDMXcommand) 

        self.DMX_address.setPlaceholderText("1 - FF")  
        self.DMX_address.setMaxLength(2) # Define o limite de caracteres a serem digitados
        
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
        global serialComunication
        
        serialComunication.close()
        serialComunication = serial.Serial(port = self.serialPort.currentText(), baudrate=250000,
                           bytesize=8, timeout=1, stopbits=serial.STOPBITS_TWO)

        # Envia os dados via serial byte a byte
       
        # MBB(MbB) - entre 0 a 1s (nível lógico 1)
        # Mark before Break. The period of time between the end if the second stop bit of the last slot and the high to low transition that signifies the start of break.

        # Space for break - 176us - (nível lógico 0)

        # MAB(MaB) - 12us a 1 s (nível lógico 1)
        # Mark afer Break. The period of time between the low to high transition that signifies the end of
        # break and the high to low transition which is the start bit of the START code (slot 0)

        #serialComunication.send_break((176+12)/10000000) # Envia os sinais de break e mark antes do primeiro slot
        

        completeComand = bytes.fromhex(f"{0xCC:0{2}X}")
        #for i in range(command2send[2] + 2):
        for i in range(command2send[2] + 1):
            # Start Time() ???
            #serialComunication.write(bytes.fromhex(f"{command2send[i]:0{2}X}"))
            # MARK time btw slots - 0 a 1s (nível lógico 1)
            completeComand = RDM.append_hex(completeComand, command2send[i+1])
        
        print(completeComand)
        serialComunication.write(completeComand) # Envia o comando completo

        #time.sleep(0.5)  # Wait for a short duration (adjust as needed)
        receive = serialComunication.read(20)
        print(receive)
        self.slave_Response.setText(str(receive))

        serialComunication.close()

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
            
    def whiteSlider(self):
        self.white_dmx_box.setValue(self.white_dmx_slider.value())

    def whiteBox(self):
        self.white_dmx_slider.setValue(self.white_dmx_box.value())

    def blueSlider(self):
        self.blue_dmx_box.setValue(self.blue_dmx_slider.value())

    def blueBox(self):
        self.blue_dmx_slider.setValue(self.blue_dmx_box.value())

    def redSlider(self):
        self.red_dmx_box.setValue(self.red_dmx_slider.value())

    def redBox(self):
        self.red_dmx_slider.setValue(self.red_dmx_box.value())

    def greenSlider(self):
        self.green_dmx_box.setValue(self.green_dmx_slider.value())

    def greenBox(self):
        self.green_dmx_slider.setValue(self.green_dmx_box.value())

    def rgbSlider(self):
        #blue = self.blue_dmx_box.value()
        #red = self.red_dmx_box.value()
        #green = self.green_dmx_box.value()
        rgb = self.RGB_dmx_slider.value()

        if rgb < 255:
            red = 255 - rgb 
            blue = 0
            green = rgb

        elif rgb < 511:
            red = 0
            blue = rgb - 255
            green = 511 - rgb

        else:
            red = rgb - 511
            blue = 767 - rgb
            green = 0

        self.red_dmx_slider.setValue(red)
        self.blue_dmx_slider.setValue(blue)
        self.green_dmx_slider.setValue(green)

    def assembleDMX(self):
        # Monta o quadro DMX 
        global DMX_frame
        global DMX_command 
       
        DMX_address = "0x" + self.DMX_address.displayText()
        if DMX_address == "0x":
            DMX_address = "0x0"

        white_value = self.white_dmx_box.value()
        blue_value = self.blue_dmx_box.value()
        green_value = self.green_dmx_box.value()
        red_value = self.red_dmx_box.value()

        DMX_frame.clear()     # Limpa o conteudo do frame antes de atribuir qualquer valor
        
        DMX_command = bytes.fromhex(f"{0x00:0{2}X}")
        
        for i in range(512):
        # Inicializa o frame de envio do DMX
            DMX_frame.append(0x0)
            DMX_command = RDM.append_hex(DMX_command, 0x00)
            
            #if literal_eval(DMX_address) < 508:
            # Adiciona o valor das cores no endereco solicitado
                #DMX_frame[literal_eval(DMX_address)] = white_value
                #DMX_frame[literal_eval(DMX_address) + 1] = blue_value
                #DMX_frame[literal_eval(DMX_address) + 2] = green_value
                #DMX_frame[literal_eval(DMX_address) + 3] = red_value
            if (i == literal_eval(DMX_address)): 
                DMX_command = RDM.append_hex(DMX_command, white_value)
                DMX_command = RDM.append_hex(DMX_command, blue_value)
                DMX_command = RDM.append_hex(DMX_command, green_value)
                DMX_command = RDM.append_hex(DMX_command, red_value)

        # Inicializa a label de comando a ser enciado
        self.DMX_command_label.clear()
        self.DMX_command_label.setText("")
        for i in range(512):
            # Mostra o frame DMX a ser enviado                
            self.DMX_command_label.setText(self.DMX_command_label.text() + " " + f"{DMX_frame[i]:0{2}X}")
            if (i % 32 == 0) and (i != 1) and (i != 0):
                # Separa a impressao em grupos de 30 bytes
                self.DMX_command_label.setText(self.DMX_command_label.text() + "\n")    

    def sendDMXcommand(self): 
        # Envia frame DMX por serial. Pode ser que seja necessáio despeitar os tempos
        global serialComunication

        serialComunication.close()
        serialComunication = serial.Serial(port = self.serialPort.currentText(), baudrate=250000,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_TWO)

        #for i in range(512):
            #serialComunication.write(bytes.fromhex(f"{DMX_frame[i]:0{2}X}"))
       
        print(DMX_command)
        serialComunication.write(DMX_command) # Envia o comando completo 
        serialComunication.close()

    def autoDMXcommand(self):
        # Aproveitar mesmo codigo do de cima, chamando equanto o chk for sim
        if self.autoSend_dmx_command.isChecked():
            # Se tiver marcado
            self.send_command_dmx.setEnabled(False)
        else:
            # Se nao tiver marcado
            self.send_command_dmx.setEnabled(True)