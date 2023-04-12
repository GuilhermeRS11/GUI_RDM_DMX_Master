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
    frame.append(rdm.E120_SC_RDM)                  # Start Code (SC)
    frame.append(rdm.E120_SC_SUB_MESSAGE)         # Sub-Start Code
    frame.append(Message_Length)                  # Message Length
    frame.append((UID_D >> 40) & 0xff)             # Destination UID bit 5
    frame.append((UID_D >> 32) & 0xff)             # Destination UID bit 4
    frame.append((UID_D >> 24) & 0xff)            # Destination UID bit 3
    frame.append((UID_D >> 16) & 0xff)             # Destination UID bit 2
    frame.append((UID_D >> 8) & 0xff)              # Destination UID bit 1
    frame.append(UID_D & 0xff)                     # Destination UID bit 0
    frame.append((UID_S >> 40) & 0xff)             # Source UID bit 5
    frame.append((UID_S >> 32) & 0xff)            # Source UID bit 4
    frame.append((UID_S >> 24) & 0xff)            # Source UID bit 3
    frame.append((UID_S >> 16) & 0xff)           # Source UID bit 2
    frame.append((UID_S >> 8) & 0xff)             # Source UID bit 1
    frame.append(UID_S & 0xff)                   # Source UID bit 0
    frame.append(TN)                              # Transaction Number
    frame.append(Port_ID)
    frame.append(Message_Count)
    frame.append((Sub_Device >> 8) & 0xff)        # Upper_Sub_Device
    frame.append(Sub_Device & 0xff)               # Lower_Sub_Device
    frame.append(CC)                              # Command Class
    frame.append((PID >> 8) & 0xff)               # Upper_PID
    frame.append(PID & 0xff)                      # Lower_PID
    frame.append(PDL)

    return frame

data = Set_frame(0x01AC34DC1134,0x02ACDF436576,0x03,0x04,0x05,0x06,0x07AB,0x08,0x09AB,0x10,0x11,0x12)

sys.stdout.write("0x")
for i in range(23):
    sys.stdout.write(hex(data[i])[2:])