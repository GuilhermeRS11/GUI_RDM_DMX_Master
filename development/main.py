import sys
from PySide6 import QtWidgets
from rdm_dmx_Master import RDM_DMX_Master

app = QtWidgets.QApplication(sys.argv)

window = RDM_DMX_Master(app)
window.show()

app.exec()
window.SendCommand()

# Integrar envio e recebimento de frames
# Deve ser enviado no formato inteiro e não em char. Ver como o receptor e transmissor em C se comunicam
# Encontrar as portas serial disponiveis causa travamento. Pq sera?

# Segundo o protocolo, todos os frames de DMX devem conter 512 slots de dados e 1 slot de inicio
# Porem a gente programou pra um numero de canais. O que é isso? Precisa? Será que canais sao o numero de cores de led em uma mesma luminaria?