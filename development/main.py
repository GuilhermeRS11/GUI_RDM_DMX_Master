import sys
from PySide6 import QtWidgets
from rdm_dmx_Master import RDM_DMX_Master

app = QtWidgets.QApplication(sys.argv)

window = RDM_DMX_Master(app)
window.show()

app.exec()
window.SendCommand()

# Integrar envio e recebimento de frames

# Encontrar as portas serial disponiveis causa travamento. Pq sera?

# Descobrir se é necessário que uma luminaria com mais de uma cor tenha seu inicio em um slot especifico. Divisivel por 4 por exemplo
# Também descobrir se há uma sequencia de cores que deve ser seguida

# desenvolver timer para ativar a luminária periodicamnete