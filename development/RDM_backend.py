import rdm_define as rdm
import sys

def Calc_checksum(frame_size, frame):
    soma = 0
    for i in range(frame_size):
        soma = soma + frame[i]

    return soma

def Set_frame(UID_D, UID_S, TN, Message_Length, Port_ID, Message_Count, Sub_Device, CC, PID, PDL, LB_PD, UB_PD):
    # Organiza o frame de acordo com os parâmetros passados e no formato do RDM
    frame = []
    frame.append(rdm.E120_SC_RDM)                 # Start Code (SC)
    frame.append(rdm.E120_SC_SUB_MESSAGE)         # Sub-Start Code
    frame.append(Message_Length)                  # Message Length
    frame.append((UID_D >> 40) & 0xff)            # Destination UID bit 5
    frame.append((UID_D >> 32) & 0xff)            # Destination UID bit 4
    frame.append((UID_D >> 24) & 0xff)            # Destination UID bit 3
    frame.append((UID_D >> 16) & 0xff)            # Destination UID bit 2
    frame.append((UID_D >> 8) & 0xff)             # Destination UID bit 1
    frame.append(UID_D & 0xff)                    # Destination UID bit 0
    frame.append((UID_S >> 40) & 0xff)            # Source UID bit 5
    frame.append((UID_S >> 32) & 0xff)            # Source UID bit 4
    frame.append((UID_S >> 24) & 0xff)            # Source UID bit 3
    frame.append((UID_S >> 16) & 0xff)            # Source UID bit 2
    frame.append((UID_S >> 8) & 0xff)             # Source UID bit 1
    frame.append(UID_S & 0xff)                    # Source UID bit 0
    frame.append(TN)                              # Transaction Number
    frame.append(Port_ID)
    frame.append(Message_Count)
    frame.append((Sub_Device >> 8) & 0xff)        # Upper_Sub_Device
    frame.append(Sub_Device & 0xff)               # Lower_Sub_Device
    frame.append(CC)                              # Command Class
    frame.append((PID >> 8) & 0xff)               # Upper_PID
    frame.append(PID & 0xff)                      # Lower_PID
    frame.append(PDL)

    if (PDL == 12):                               # Frames que tem 12 bytes de UID (lower and upper bound) Disc_unique_branch
        frame.append((LB_PD >> 40) & 0xff)        # Lower Bound UID byte 5
        frame.append((LB_PD >> 32) & 0xff)        # Lower Bound UID byte 4
        frame.append((LB_PD >> 24) & 0xff)        # Lower Bound UID byte 3
        frame.append((LB_PD >> 16) & 0xff)        # Lower Bound UID byte 2
        frame.append((LB_PD >> 8) & 0xff)         # Lower Bound UID byte 1
        frame.append(LB_PD & 0xff)                # Lower Bound UID byte 0
        frame.append((UB_PD >> 40) & 0xff)        # Upper Bound UID byte 5
        frame.append((UB_PD >> 32) & 0xff)        # Upper Bound UID byte 4
        frame.append((UB_PD >> 24) & 0xff)        # Upper Bound UID byte 3
        frame.append((UB_PD >> 16) & 0xff)        # Upper Bound UID byte 2
        frame.append((UB_PD >> 8) & 0xff)         # Upper Bound UID byte 1
        frame.append(UB_PD & 0xff)                # Upper Bound UID byte 0

        checksum = Calc_checksum(36, frame)
        frame.append((checksum >> 8) & 0xff)      # Checksum high
        frame.append(checksum & 0xff)             # Checksum low

    elif (PDL == 2):                              # Para o Get_parameter_description
        frame.append((LB_PD >> 8) & 0xff)
        frame.append(LB_PD & 0xff)

        checksum = Calc_checksum(26, frame)
        frame.append((checksum >> 8) & 0xff)
        frame.append(checksum & 0xff)

    elif (PDL == 1):                              # Para SET_identify_device
        frame.append(LB_PD & 0xff)

        checksum = Calc_checksum(25, frame)
        frame.append((checksum >> 8) & 0xff)
        frame.append(checksum & 0xff)

    else:                                         # Para funcões sem PD (disc_mute, disc_un_mute etc.)
        checksum = Calc_checksum(24, frame)
        frame.append((checksum >> 8) & 0xff)
        frame.append(checksum & 0xff)

    return frame

def DISC_unique_branch(UID_D, UID_S, TN, Port_ID, LB_PD, UB_PD):

    Message_Length = 0x24  # 36 bytes
    Message_Count = 0x00
    Sub_Device = 0x0000
    CC = rdm.E120_DISCOVERY_COMMAND
    PID = rdm.E120_DISC_UNIQUE_BRANCH
    PDL = 0X0c

    data_set = Set_frame(UID_D, UID_S, TN, Message_Length, Port_ID, Message_Count, Sub_Device, CC, PID, PDL, LB_PD, UB_PD)
    return data_set

def DISC_mute(UID_D, UID_S, TN, Port_ID):

    Message_Length = 0x18 # 24 bytes
    Message_Count = 0x00
    Sub_Device = 0x0000
    CC = rdm.E120_DISCOVERY_COMMAND
    PID = rdm.E120_DISC_MUTE
    PDL = 0X00
    LB_PD = None
    UB_PD = None

    data_set = Set_frame(UID_D, UID_S, TN, Message_Length, Port_ID, Message_Count, Sub_Device, CC, PID, PDL, LB_PD, UB_PD)
    return data_set

def DISC_un_mute(UID_D, UID_S, TN, Port_ID):

    Message_Length = 0x18  # 24 bytes
    Message_Count = 0x00
    Sub_Device = 0x0000
    CC = rdm.E120_DISCOVERY_COMMAND
    PID = rdm.E120_DISC_UN_MUTE
    PDL = 0X00
    LB_PD = None
    UB_PD = None

    data_set = Set_frame(UID_D, UID_S, TN, Message_Length, Port_ID, Message_Count, Sub_Device, CC, PID, PDL, LB_PD, UB_PD)
    return data_set

def GET_supported_parameters(UID_D, UID_S, TN, Port_ID, Sub_Device):

    Message_Length = 0x18      # 24 bytes
    Message_Count = 0x00
    CC = rdm.E120_GET_COMMAND
    PID = rdm.E120_SUPPORTED_PARAMETERS
    PDL = 0X00
    LB_PD = None
    UB_PD = None

    data_set = Set_frame(UID_D, UID_S, TN, Message_Length, Port_ID, Message_Count, Sub_Device, CC, PID, PDL, LB_PD, UB_PD)
    return data_set

def GET_parameter_description(UID_D, UID_S, TN, Port_ID, PID_Requested):

    Message_Length = 0x1A      # 26 bytes
    Message_Count = 0x00
    Sub_Device = 0x0000
    CC = rdm.E120_GET_COMMAND
    PID = rdm.E120_PARAMETER_DESCRIPTION
    PDL = 0X02
    LB_PD = PID_Requested
    UB_PD = None

    data_set = Set_frame(UID_D, UID_S, TN, Message_Length, Port_ID, Message_Count, Sub_Device, CC, PID, PDL, LB_PD, UB_PD)
    return data_set

def GET_device_info(UID_D, UID_S, TN, Port_ID, Sub_Device):

    Message_Length = 0x18              # 24 bytes
    Message_Count = 0x00
    CC = rdm.E120_GET_COMMAND
    PID = rdm.E120_DEVICE_INFO
    PDL = 0X00
    LB_PD = None
    UB_PD = None

    data_set = Set_frame(UID_D, UID_S, TN, Message_Length, Port_ID, Message_Count, Sub_Device, CC, PID, PDL, LB_PD, UB_PD)
    return data_set

def GET_software_version_label(UID_D, UID_S, TN, Port_ID, Sub_Device):

    Message_Length = 0x18     # 24 bytes
    Message_Count = 0x00
    CC = rdm.E120_GET_COMMAND
    PID = rdm.E120_SOFTWARE_VERSION_LABEL
    PDL = 0X00
    LB_PD = None
    UB_PD = None

    data_set = Set_frame(UID_D, UID_S, TN, Message_Length, Port_ID, Message_Count, Sub_Device, CC, PID, PDL, LB_PD, UB_PD)
    return data_set

def GET_dmx_start_address(UID_D, UID_S, TN, Port_ID, Sub_Device):

    Message_Length = 0x18      # 24 bytes
    Message_Count = 0x00
    CC = rdm.E120_GET_COMMAND
    PID = rdm.E120_DMX_START_ADDRESS
    PDL = 0X00
    LB_PD = None
    UB_PD = None

    data_set = Set_frame(UID_D, UID_S, TN, Message_Length, Port_ID, Message_Count, Sub_Device, CC, PID, PDL, LB_PD, UB_PD)
    return data_set

def GET_identify_device(UID_D, UID_S, TN,  Port_ID, Sub_Device):

    Message_Length = 0x18      # 24 bytes
    Message_Count = 0x00
    CC = rdm.E120_GET_COMMAND
    PID = rdm.E120_IDENTIFY_DEVICE
    PDL = 0X00
    LB_PD = None
    UB_PD = None

    data_set = Set_frame(UID_D, UID_S, TN, Message_Length, Port_ID, Message_Count, Sub_Device, CC, PID, PDL, LB_PD, UB_PD)
    return data_set

def SET_dmx_start_address(UID_D, UID_S, TN, Port_ID, Sub_Device, DMX_address):

    Message_Length = 0x1A          # 26 bytes
    Message_Count = 0x00
    CC = rdm.E120_SET_COMMAND
    PID = rdm.E120_DMX_START_ADDRESS
    PDL = 0X02
    LB_PD = DMX_address
    UB_PD = None

    data_set = Set_frame(UID_D, UID_S, TN, Message_Length, Port_ID, Message_Count, Sub_Device, CC, PID, PDL, LB_PD, UB_PD)
    return data_set

def SET_identify_device(UID_D, UID_S, TN, Port_ID, Sub_Device, Identify_start_stop):

    Message_Length = 0x19      # 25 bytes
    Message_Count = 0x00
    CC = rdm.E120_SET_COMMAND
    PID = rdm.E120_IDENTIFY_DEVICE
    PDL = 0X01
    LB_PD = Identify_start_stop
    UB_PD = None

    data_set = Set_frame(UID_D, UID_S, TN, Message_Length, Port_ID, Message_Count, Sub_Device, CC, PID, PDL, LB_PD, UB_PD)
    return data_set
