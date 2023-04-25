import sys
from PySide6 import QtWidgets
from rdm_dmx_Master import RDM_DMX_Master

app = QtWidgets.QApplication(sys.argv)

window = RDM_DMX_Master(app)
window.show()

app.exec()
window.SendCommand()

# Trabalhar na interface DMX, pois a RDM está muito boa
# Pesquisar como enviar dados via USB com python
# Integrar envio e recebimento de frames

# Verificar a funcionalidade do chenck_sum. A exibição está mostrando apenas 1 ao invés de 10 no primeiro byte
# O envio dos dados deve ser 01 e não 1. Mudar isso no envio.
# Deve ser enviado no formato inteiro e não em char