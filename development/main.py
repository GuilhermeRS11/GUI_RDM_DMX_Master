import sys

from PySide6 import QtWidgets
from rdm_dmx_Master import RDM_DMX_Master

app = QtWidgets.QApplication(sys.argv)

window = RDM_DMX_Master(app)
window.show()

app.exec()
window.SendCommand()

# Definir os limites de cada campo. Ex: start/stop deve ser 0 - 1
# Tirar a marca do spliter
# Trabalhar na interface DMX, pois a RDM está muito boa
# Pesquisar como enviar dados via USB com python
# Integrar envio e recebimento de frames
