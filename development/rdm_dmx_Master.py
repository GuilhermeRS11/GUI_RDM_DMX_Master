from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QAction, QIcon
from RDM_DMX_Master_ui import Ui_MainWindow
from ast import literal_eval
import webbrowser

import RDM_backend as RDM
import serial
import time

Flag_just_once = True

# Initialize parameter to be shared between functions
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

        # Execute the commands below only at app initialization
        global Flag_just_once
        global Slots_per_link, command_len
        global Auto_DMX_send
        global elapsed_time, last_command_sent, startTime_for_tictoc

        if Flag_just_once:
            Flag_just_once = False
            Auto_DMX_send = False
            elapsed_time = 0
            last_command_sent = True
            startTime_for_tictoc = 0
    
            self.Slots_per_link.setValue(192)        # Initialize the number of slots per link with value 513
            self.serialFindPorts()                   # Perform the first search for system serial ports
            self.brightness_slider.setValue(255)     # Initialize brightness with value 100
            self.resolutionValues()                  # Initialize DMX data resolution
            self.brightnessSlider()                  # Initialize brightness 
            self.caixaCommand()                      # Update display fields with zeroed values
            self.rgbSlider()                         # Update color values through initial rgb slider position
            self.assembleDMX()                       # Update the command to be sent in DMX   
            self.red_dmx_box.setValue(255)           # Initialize the text box with the coherent value
            
            self.TBB_label.setToolTip("Time between bytes")
            self.TBF_label.setToolTip("Time between frames")
            self.break_time_label.setToolTip("Break time. Must be between 88us and 1s to work")
            self.slots_number_label.setToolTip("Number of addresses the frame sends")
            self.autoSend_dmx_command.setToolTip("Automatically sends the command with each new modification")
            self.continuousSend_dmx_command.setToolTip("Continuously sends the command, one after the other")

        # Set the window icon
        self.setWindowIcon(QIcon("images/masterDMX-Icon.png"))
        
        # Create actions for the menus
        self.actionAbout = QAction("About the Project", self)
        self.actionExit = QAction("Exit", self)

        # Add actions to the menus
        self.menuAjuda.addAction(self.actionAbout)
        self.menuSair.addAction(self.actionExit)

        # Connect actions to the corresponding methods
        self.actionAbout.triggered.connect(self.showAbout)
        self.actionExit.triggered.connect(self.quitApp)

        """ 
        #############################################################################################
                                   Frontend language dictionary area
        #############################################################################################
        """
        self.translations = {
            "Português": {
                "slots_number_label": "Slots por link",
                "Address_label": "Endereço da luminária",
                "format_label": "Formato",
                "white_label": "Branco",
                "blue_label": "Azul",
                "red_label": "Vermelho",
                "green_label": "Verde",
                "frameInfo_label": "Frame a ser enviado em exadecimal",
                "advParam_label": "Parametros avançados - apenas para testes",
                "autoSend_label": "Enviar automaticamente",
                "continuousSend_label": "Enviar continuamente",
                "language_label": "Idioma",
                "class_label": "Classe",
                "param_label": "Parâmetro",
                "command_label": "Comando",
                "UID_label": "UID de destino",
                "UIDSource_label": "UID da fonte",
                "FrameSize_label": "Tamanho do frame",
                "CommandInfo_label": "Comando a ser enviado byte a byte em hexadecimal",
                "SlaveRespose_label": "Resposta do slave",
                "send_command": "Enviar Comando",
                "menuAjuda": "Ajuda",
                "menuSair": "Sair",
                "about_title": "Sobre o RDM DMX Master",
                "about_text": "Este software é um controlador para dispositivos DMX e RDM.",
                "about_requirement": "Para funcionar corretamente, é necessário conectar a placa DMX-Master.",
                "about_links": "Links do projeto:",
                "hardware_link": "DMX-Master (Hardware)",
                "gui_link": "RDM DMX GUI",
                "actionAbout": "Sobre o Projeto",
                "actionExit": "Sair",
                "about_author": "Desenvolvido por: Guilherme Ribeiro Silveira",
                "about_contact": "Contato: guilhermeribeiro201342@gmail.com"
              
            },
            "English": {
                "slots_number_label": "Slots per link",
                "Address_label": "Luminaire Address",
                "format_label": "Format",
                "white_label": "White",
                "blue_label": "Blue",
                "red_label": "Red",
                "gree_label": "Green",  
                "frameInfo_label": "Frame to be sent in hexadecimal",
                "advParam_label": "Advanced parameters - for testing only",
                "autoSend_label": "Send automatically",
                "continuousSend_label": "Send continuously",
                "language_label": "Language",
                "serialPort_label": "Serial Port",
                "class_label": "Class",
                "param_label": "Parameter",
                "command_label": "Command",
                "UID_label": "Destination UID",
                "UIDSource_label": "Source UID",
                "FrameSize_label": "Frame Size",
                "CommandInfo_label": "Command to be sent byte by byte in hexadecimal",
                "SlaveRespose_label": "Slave Response",
                "send_command": "Send Command",
                "menuAjuda": "Help",
                "menuSair": "Exit",
                "about_title": "About RDM DMX Master",
                "about_text": "This software is a controller for DMX and RDM devices.",
                "about_requirement": "To work properly, the DMX-Master board must be connected.",
                "about_links": "Project links:",
                "hardware_link": "DMX-Master (Hardware)",
                "gui_link": "RDM DMX GUI",
                "actionAbout": "About the Project",
                "actionExit": "Exit",
                "about_author": "Developed by: Guilherme Ribeiro Silveira",
                "about_contact": "Contact: guilhermeribeiro201342@gmail.com"

            }   
        }

        # Connect the comboBox to change the language
        self.languageSelect.addItems(["Português", "English"])
        self.languageSelect.currentTextChanged.connect(self.changeLanguage)

        # Set the initial language
        self.current_language = "Português"
        self.changeLanguage(self.current_language)


   
        """ 
        #############################################################################################
                                    RDM_frontend sensitivity area
        #############################################################################################
        """

        # Identify the action of the main graphical elements
        self.classe.activated.connect(self.ChangeParameter)
        self.classe.activated.connect(self.caixaCommand)
        self.parametro.activated.connect(self.clearAddParam)
        self.parametro.activated.connect(self.caixaCommand)
        self.send_command.clicked.connect(self.SendCommand)
        self.menuSair.triggered.connect(self.quit)
        self.serialPort.activated.connect(self.changeSerialPort)

        # Update the bytes of the display boxes
        self.destination_UID.textEdited.connect(self.caixaCommand)
        self.source_UID.textEdited.connect(self.caixaCommand)
        self.sub_device.textEdited.connect(self.caixaCommand)
        self.port_ID.textEdited.connect(self.caixaCommand)
        self.add_param_1.textEdited.connect(self.caixaCommand)
        self.add_param_2.textEdited.connect(self.caixaCommand)

        # Define the maximum number of characters in each parameter
        self.source_UID.setMaxLength(12)
        self.destination_UID.setMaxLength(12)
        self.port_ID.setMaxLength(2)
        self.sub_device.setMaxLength(4) # It is necessary to specify the range of this in each command

        self.port_ID.setPlaceholderText("01 - FF")
        self.source_UID.setPlaceholderText("0 - FFFFFFFFFFFF")
        self.destination_UID.setPlaceholderText("0 - FFFFFFFFFFFF")

        self.alignement_labels() # Align the command boxes to the center

        self.refreshPorts.clicked.connect(self.serialFindPorts) # Update ports when clicking refresh



        """ 
        #############################################################################################
                                    DMX_frontend sensitivity area
        #############################################################################################
        """

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
        self.TBB_value.valueChanged.connect(self.assembleDMX)
        self.TBF_value.valueChanged.connect(self.assembleDMX)
        self.break_time_value.valueChanged.connect(self.assembleDMX)
        self.continuousSend_dmx_command.stateChanged.connect(self.assembleDMX)
        
        self.DMX_address.setPlaceholderText("1 - FF")  
        self.DMX_address.setMaxLength(2) # Define the character limit to be entered

        # Instantiate the timer to send DMX commands automatically, spaced by some time
        self.last_dmx_command_time = 0
        # Instantiate the flag that indicates if the command is via RGB slider. It serves to prevent multiple calls to assembleDMX()
        self.isRGB_slidder_command = False


    def changeLanguage(self, language):
            # Change the texts according to the selected language."""
            self.current_language = language
            self.setWindowTitle(self.translations[language].get("title", "RDM DMX Master"))

            # Updating the texts of QLabel
            self.slots_number_label.setText(self.translations[language].get("slots_number_label", "Slots per link"))
            self.Address_label.setText(self.translations[language].get("Address_label", "Fixture Address"))
            self.format_label.setText(self.translations[language].get("format_label", "Format"))
            self.white_label.setText(self.translations[language].get("white_label", "White"))
            self.blue_label.setText(self.translations[language].get("blue_label", "Blue"))
            self.red_label.setText(self.translations[language].get("red_label", "Red"))
            self.green_label.setText(self.translations[language].get("green_label", "Green"))
            self.frameInfo_label.setText(self.translations[language].get("frameInfo_label", "Frame to be sent in hexadecimal"))
            self.advParam_label.setText(self.translations[language].get("advParam_label", "Advanced parameters - for testing only"))
            self.autoSend_label.setText(self.translations[language].get("autoSend_label", "Send automatically"))
            self.continuousSend_label.setText(self.translations[language].get("continuousSend_label", "Send continuously"))
            self.language_label.setText(self.translations[language].get("language_label", "Language"))
            self.serialPort_label.setText(self.translations[language].get("serialPort_label", "Serial Port"))
            self.class_label.setText(self.translations[language].get("class_label", "Class"))
            self.param_label.setText(self.translations[language].get("param_label", "Parameter"))
            self.command_label.setText(self.translations[language].get("command_label", "Command"))
            self.UID_label.setText(self.translations[language].get("UID_label", "Destination UID"))
            self.UIDSource_label.setText(self.translations[language].get("UIDSource_label", "Source UID"))
            self.FrameSize_label.setText(self.translations[language].get("FrameSize_label", "Frame Size"))
            self.CommandInfo_label.setText(self.translations[language].get("CommandInfo_label", "Command to be sent byte by byte in hexadecimal"))
            self.SlaveRespose_label.setText(self.translations[language].get("SlaveRespose_label", "Slave Response"))

            # Update button texts
            self.send_command.setText(self.translations[language].get("send_command", "Send Command"))
            self.send_command_dmx.setText(self.translations[language].get("send_command", "Send Command"))

            # Update menu texts
            self.menuAjuda.setTitle(self.translations[language].get("menuAjuda", "Help"))
            self.menuSair.setTitle(self.translations[language].get("menuSair", "Exit"))
            self.actionAbout.setText(self.translations[language].get("actionAbout", "About the Project"))
            self.actionExit.setText(self.translations[language].get("actionExit", "Exit"))

            # Center texts in the desired labels
            self.frameInfo_label.setAlignment(Qt.AlignCenter)
            self.advParam_label.setAlignment(Qt.AlignCenter)
            self.white_label.setAlignment(Qt.AlignRight)
            self.blue_label.setAlignment(Qt.AlignRight)
            self.red_label.setAlignment(Qt.AlignRight)
            self.green_label.setAlignment(Qt.AlignRight)
            self.Address_label.setAlignment(Qt.AlignRight)
            self.UID_label.setAlignment(Qt.AlignRight)
            self.UIDSource_label.setAlignment(Qt.AlignRight)
            self.CommandInfo_label.setAlignment(Qt.AlignCenter)
            self.SlaveRespose_label.setAlignment(Qt.AlignCenter)
            self.command_label.setAlignment(Qt.AlignRight)
            self.FrameSize_label.setAlignment(Qt.AlignRight)
            self.autoSend_label.setAlignment(Qt.AlignRight)
            
            # Set font for advParam_label (size 7, bold)
            font_adv = QFont()
            font_adv.setPointSize(7)
            font_adv.setBold(True)
            self.advParam_label.setFont(font_adv)

            # Set font for color names (size 12)
            font_colors = QFont()
            font_colors.setPointSize(12)
        
            font_infos = QFont()
            font_infos.setPointSize(9)
            font_infos.setBold(True)
            self.CommandInfo_label.setFont(font_infos)
            self.FrameSize_label.setFont(font_infos)
            
            self.white_label.setFont(font_colors)
            self.blue_label.setFont(font_colors)
            self.red_label.setFont(font_colors)
            self.green_label.setFont(font_colors)




    """ 
    #############################################################################################
                                            RDM_frontend
    #############################################################################################
    """

    def ChangeParameter(self):
        classe = self.classe.currentText()
        self.clearAddParam() # Clear the extra parameter boxes
        
        # Update other fields that should or should not be activated
        if(classe == "DISC"):
            self.parametro.clear()
            self.parametro.addItems(["Unique Branch","Mute","Unmute"]) 
                                   
        elif(classe == "GET"):
            self.parametro.clear()
            self.parametro.addItems(["Supported parameters","Parameter description","Device info", "Software version label", "DMX start address", "Identify device"])

        else:   # Then it is a SET command
            self.parametro.clear()
            self.parametro.addItems(["DMX start address","Identify device"])

    def quit(self):
        global serialComunication
        serialComunication.close()
        self.app.quit()

    def caixaCommand(self):
        global command2send
        global command_len

        classe = self.classe.currentText()
        parameter = self.parametro.currentText()

        self.clearBoxes() # Clear the text boxes before writing anything

        # Append the value of the text boxes to 0x to convert later using "literal_eval"
        destination_UID = "0x" + self.destination_UID.displayText()
        source_UID = "0x" + self.source_UID.displayText()
        sub_device = "0x" + self.sub_device.displayText()
        port_id = "0x" + self.port_ID.displayText()
        # Additional parameters that are used only in some commands and vary depending on the command
        add_param_1 = "0x" + self.add_param_1.displayText()
        add_param_2 = "0x" + self.add_param_2.displayText()
        TN = 0 # So far it has not been implemented, so I set the default value to 0

        # Initialize the text boxes if their value is empty
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
            
        # Convert the value of the text boxes from str to int
        destination_UID = literal_eval(destination_UID)
        source_UID = literal_eval(source_UID)
        sub_device = literal_eval(sub_device)
        port_id = literal_eval(port_id)
        add_param_1 = literal_eval(add_param_1)
        add_param_2 = literal_eval(add_param_2)

        # Taking advantage of the call to update other fields that should or should not be activated
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
            
             # Then it is Identify device
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
                self.add_param_1.setMaxLength(12) # Sets the character limit for input
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
        
        command_len = command2send[2] + 2 # Include text box to show the frame size
        self.frame_size.setText(str(command_len))

        # Include extra text box for additional parameter. The Disc unique branch needs two
            
        # Separate each byte of the command to be sent into the corresponding text box
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

        # Set the tooltips for each text box
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

        # Adapt the data to send the communication parameters between the Windows GUI and the RDM-DMX Master module
        Module_header = [0x7E, 0x06, 0x3A]
        Module_tail = [0x7E, 0x06, 0x3B]

        frame_size = command_len + 3
        Module_frame_size = [frame_size >> 8, frame_size & 0xFF]  # Split the Module_frame_size into two bytes

        # Assemble the command to be sent to the RDM-DMX Master module
        command2send = Module_header + Module_frame_size + command2send + Module_tail

    

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
        global command_len

        # Print byte by byte the sent command:
        for i in range(len(command2send)):
            print(f"{command2send[i]:0{2}X}", end=" ")
        print("\n")

        serialComunication.write(bytes(command2send))
        # Print the sent RDM command:
        print("RDM command sent")

        # Receive RDM data
        receive = serialComunication.read(300)

        # Test receiving a response frame to a Disc_unique_branch
        #receive = [0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0xaa, 0xba, 0x57, 0xbe, 0x75, 0xfe, 0x57, 0xfa, 0x7d, 0xba, 0xdf, 0xbe, 0xfd, 0xaa, 0x5d, 0xee, 0x75]

        # Test receiving a response frame to a standard RDM
        #receive = [0xcc, 0x01, 0x19, 0x12, 0x34, 0x56, 0x78, 0x9a, 0xbc, 0xcb, 0xa9, 0x87, 0x65, 0x43, 0x21, 0x00, 0x01, 0x00, 0x00, 0x00, 0x20, 0x00, 0x30, 0x01, 0x04, 0x06, 0x6a]
        self.responseProcess(receive)
        
    def responseProcess(self, receive):
        # Adjust the received data to display on the screen
        self.slaveResponse.clear()

        if(len(receive) == 0):
        # Inform that nothing was received
            self.slaveResponse.addItem("No data received")
            return
        
        elif receive[0] == 0xFE:
        # Process response frame to a Disc_unique_branch
            checksum = 0
            # Display the received frame
            string_receive = "Frame received: "
            for i in range(len(receive)):
                string_receive = string_receive + f"{receive[i]:0{2}X}" + " "
                if i > 7 and i < 20:
                    checksum = checksum + receive[i]

            # Display the received frame
            self.slaveResponse.addItem(string_receive)

            # Display the number of bytes received
            string_receive = "Number of bytes received: " + str(len(receive))
            self.slaveResponse.addItem(string_receive)
            
            # Decode the data
            decodeData = [0, 0, 0, 0, 0, 0, 0, 0]
            decodeData[0] = receive[8] & receive[9]
            decodeData[1] = receive[10] & receive[11]
            decodeData[2] = receive[12] & receive[13]
            decodeData[3] = receive[14] & receive[15]
            decodeData[4] = receive[16] & receive[17]
            decodeData[5] = receive[18] & receive[19]
            decodeData[6] = receive[20] & receive[21]
            decodeData[7] = receive[22] & receive[23]

            string_receive = "Decoded data: "
            for i in range(8):
                string_receive = string_receive + f"{decodeData[i]:0{2}X}" + " "
            
            # Display the decoded data
            self.slaveResponse.addItem(string_receive)

            #print(checksum)
            #print(((decodeData[6] << 8) | decodeData[7]))
            if ((decodeData[6] << 8) | decodeData[7]) == checksum:
                string_receive = "Checksum: OK"
            else:
                string_receive = "Checksum: ERROR"
            
            # Display the checksum result
            self.slaveResponse.addItem(string_receive)

            string_receive = "Source UID: "
            for i in range(6):
                string_receive = string_receive + f"{decodeData[i]:0{2}X}" + " "

            # Display the UID   
            self.slaveResponse.addItem(string_receive)

        elif receive[0] == 0xCC:
            checksum = 0
            string_receive = "Frame received: "
            frameSize = len(receive)

            for i in range(frameSize):
                string_receive = string_receive + f"{receive[i]:0{2}X}" + " "
                if (i % 27 == 0) and (i != 0): 
                    # Separate the line when it has more than 27 elements
                    self.slaveResponse.addItem(string_receive)
                    string_receive = "                           "

                if i < frameSize - 2:
                    # Calculate the checksum
                    checksum = checksum + receive[i]

            # Display the received frame
            self.slaveResponse.addItem(string_receive)

            # Display the number of bytes received
            string_receive = "Number of bytes received: " + str(frameSize)
            self.slaveResponse.addItem(string_receive)

            # Display the result of the frame size
            if frameSize == receive[2] + 2:
                string_receive = "Frame size: OK"
            else:
                string_receive = "Frame size: ERROR"

            self.slaveResponse.addItem(string_receive)

            # Display the checksum result
            if ((receive[frameSize - 2] << 8) | receive[frameSize - 1]) == checksum:
                string_receive = "Checksum: OK"
            else:
                string_receive = "Checksum: ERROR"

            self.slaveResponse.addItem(string_receive)

            # Display the UID
            string_receive = "Source UID: "
            for i in range(6):
                string_receive = string_receive + f"{receive[i + 9]:0{2}X}" + " "

            self.slaveResponse.addItem(string_receive)

            # Display the response type
            if receive[16] == 0x00:
                string_receive = "Response type: ACK"
            elif receive[16] == 0x01:
                string_receive = "Response type: ACK_TIMER"
            elif receive[16] == 0x02:
                string_receive = "Response type: NACK_REASON"
            elif receive[16] == 0x03:
                string_receive = "Response type: ACK_OVERFLOW"

            self.slaveResponse.addItem(string_receive)

            # Display the size of the PD
            pdSize = receive[23]
            string_receive = "PD Size: " + str(pdSize)
            
            self.slaveResponse.addItem(string_receive)

            # Display the PD
            #if (receive[20] == 0x21) and (receive[21] == 0x00):
                #string_receive = "DMX Address: "
            #else:    
                #string_receive = "Parameter Data: "
            string_receive = "Parameter Data: "
            for i in range(pdSize):
                string_receive = string_receive + f"{receive[frameSize - 2 - pdSize + i]:0{2}X}" + " "
                if (i % 27 == 0) and (i != 0): 
                    # Separate the line when it has more than 27 elements
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
        # Align the command boxes to the center
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
        global serialComunication
        serialComunication.close()     # Close the current serial port, otherwise it won't appear in the list

        ports = ['COM%s' % (i + 1) for i in range(256)]
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port) # Add the found ports to a list
            except (OSError, serial.SerialException):
                pass
            
        self.serialPort.clear()
        self.serialPort.addItems(result) # Create the box items with the list  
        
        #self.changeSerialPort() # Automatically select the first serial port   
    """ 
    #############################################################################################
                                            DMX_backend
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
        #if(self.resolution_values.currentText() == "8 bits"):
        if(1):
            # Set all fields to have 8 bits
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
            # Set all fields to have 16 bits
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
        # Update the values of sliders and boxes after changing the resolution
        # Convert the value from 8 bits to 16 bits and vice versa, maintaining the proportion, storing the current value before changing the resolution
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

        self.isRGB_slidder_command = True # Activates the flag to not call the assembleDMX() function during slider adjustments
        self.red_dmx_slider.setValue(red)
        self.blue_dmx_slider.setValue(blue)
        self.green_dmx_slider.setValue(green)
        self.white_dmx_slider.setValue(0)
        self.assembleDMX()

    def brightnessSlider(self):
        global brightness
        brightness = self.brightness_slider.value() / maxValue_onResolution # Maximum value they can assume
        self.brightness_percentage_box.setText(str(round(brightness * 100)) + "%")
        # Update the values of sliders and boxes after changing the brightness
        self.rgbSlider()

    def assembleDMX(self):
        # Assembles the DMX frame
        global DMX_frame
        global Slots_per_link
        global Auto_DMX_send 
        global frame_size

        # Adds header and footer specific for this interface to communicate with the DMX module
        Module_header = [0x7E, 0x06, 0x3A]
        Module_tail = [0x7E, 0x06, 0x3B]
       
        DMX_address = "0x" + self.DMX_address.displayText()
        if DMX_address == "0x":
            DMX_address = "0x0"

        if self.continuousSend_dmx_command.isChecked():
            Countinuous_DMX_send = 1
        else:
            Countinuous_DMX_send = 0

        TBB = self.TBB_value.value()
        TBF = self.TBF_value.value()
        break_time = self.break_time_value.value()

        Slots_per_link = self.Slots_per_link.value()
        white_value = self.white_dmx_slider.value()
        blue_value = self.blue_dmx_slider.value()
        green_value = self.green_dmx_slider.value()
        red_value = self.red_dmx_slider.value()

        # Defines the frame size to be sent and adapts to fit in 2 bytes
        frame_size = Slots_per_link + 3
        Module_frame_size = [frame_size >> 8, frame_size & 0xFF]  # Splits the Module_frame_size into two bytes
       
        DMX_frame.clear()     # Clears the frame content before assigning any value

        # Adds the header and frame size to the module frame
        DMX_frame.append(Module_header[0])
        DMX_frame.append(Module_header[1])
        DMX_frame.append(Module_header[2])
        DMX_frame.append(Module_frame_size[0])
        DMX_frame.append(Module_frame_size[1])
        DMX_frame.append(TBB)
        DMX_frame.append(TBF)
        DMX_frame.append(break_time)
        DMX_frame.append(Countinuous_DMX_send)
   
        for i in range(Slots_per_link):
        # Initializes the DMX send frame
            DMX_frame.append(0x0)

        if (literal_eval(DMX_address)) and (literal_eval(DMX_address) < Slots_per_link - 2):
            # Adds the color values at the requested address (+5 to compensate for header and frame size)
            DMX_frame[literal_eval(DMX_address) + 9] = red_value
            DMX_frame[literal_eval(DMX_address) + 9 + 1] = green_value
            DMX_frame[literal_eval(DMX_address) + 9 + 2] = blue_value
            DMX_frame[literal_eval(DMX_address) + 9 + 3] = white_value  

        # Adds the tail to the module frame
        DMX_frame.append(Module_tail[0])
        DMX_frame.append(Module_tail[1])
        DMX_frame.append(Module_tail[2])

        # Initializes the command label to be started
        self.DMX_command_label.clear()
        DMX_frame_show = "000 - 00"
        
        for i in range(2, Slots_per_link + 1):
            # Shows the DMX frame to be sent                
            DMX_frame_show = DMX_frame_show + " " + f"{DMX_frame[i-1+9]:0{2}X}"
            if ((i % 32 == 0) and (i != 1) and (i != 0)) or (i == Slots_per_link):
                # Separates the print into groups of 30 bytes
                self.DMX_command_label.addItem(DMX_frame_show)
                DMX_frame_show = f"{i:0{3}}" + " -"

        if Auto_DMX_send:
            # Automatically sends commands if the box is checked and checks if it's time to send to the serial 
            global last_command_sent
                          
            #if elapsed_time > Time_operational_delay + 100: #If you need to enable a delay time between one command and another
            self.sendDMXcommand()
            last_command_sent = False
            
            #Resets the time.time
            self.timer.stop()
            self.timer.start(10) # Starts the timer that checks if the last command was sent
                                 # If there are still commands to be sent, it restarts the timer

            
    def sendLastCommand(self):
        # Sends the last DMX command after the waiting time, to ensure that the last command is the last one assembled
        if(Auto_DMX_send):
            global last_command_sent
            if (not(last_command_sent)):
                self.timer.stop()
                self.sendDMXcommand()
                last_command_sent = True
                #print("Last command sent")
                

    def sendDMXcommand(self): 
        # Send DMX frame via serial
        self.isRGB_slidder_command = False # Deactivate the flag to allow the call of the assembleDMX() function during slider adjustments
        serialComunication.write(bytes(DMX_frame))
        # print the size of DMX_frame
        #print("DMX command sent")

    def autoDMXcommand(self):
        global Auto_DMX_send
        # Automatically send commands
        if self.autoSend_dmx_command.isChecked():
            # If checked
            self.send_command_dmx.setEnabled(False)
            Auto_DMX_send = True
        else:
            # If not checked
            self.send_command_dmx.setEnabled(True)
            Auto_DMX_send = False

    def tic(self):    
        global startTime_for_tictoc
        startTime_for_tictoc = time.time()

    def toc(self):
        print("Elapsed time is ",(time.time() - startTime_for_tictoc)*1000," milliseconds.")

    def changeSerialPort(self):
        # Change the serial port according to the selected one
        global serialComunication
        serialComunication.close()
        serialComunication = serial.Serial(port=self.serialPort.currentText(), baudrate=500000,
                                        bytesize=8, timeout=2, stopbits=serial.STOPBITS_TWO)

    def showAbout(self):
        # Show information about the project
        msg = QMessageBox(self)
        msg.setWindowTitle(self.translations[self.current_language].get("about_title", "Sobre o RDM DMX Master"))

        msg.setText(self.translations[self.current_language].get("about_text", "Este software é um controlador para dispositivos DMX e RDM.") + "\n\n" +
                    self.translations[self.current_language].get("about_requirement", "Para funcionar corretamente, é necessário conectar a placa DMX-Master.") + "\n\n" +
                    self.translations[self.current_language].get("about_author", "Desenvolvido por: Guilherme Ribeiro Silveira") + "\n" +
                    self.translations[self.current_language].get("about_contact", "Contato: guilhermeribeiro201342@gmail.com"))

        msg.setInformativeText(
            f"{self.translations[self.current_language].get('about_links', 'Links do projeto:')}<br>"
            f'<a href="https://github.com/GuilhermeRS11/DMX_Master_STM32">{self.translations[self.current_language].get("hardware_link", "DMX-Master (Hardware)")}</a><br>'
            f'<a href="https://github.com/GuilhermeRS11/GUI_RDM_DMX_Master">{self.translations[self.current_language].get("gui_link", "RDM DMX GUI")}</a>'
        )

        msg.setTextInteractionFlags(Qt.TextBrowserInteraction)  # Allows interaction with links
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def quitApp(self):
        # Close the application
        self.close()