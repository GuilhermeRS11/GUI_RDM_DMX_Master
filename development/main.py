import sys
from PySide6 import QtWidgets
from rdm_dmx_Master import RDM_DMX_Master

app = QtWidgets.QApplication(sys.argv)

window = RDM_DMX_Master(app)
window.show()

app.exec()
window.SendCommand()

# Trabalhar na interface DMX, pois a RDM está muito boa
# Integrar envio e recebimento de frames
# Adicionar funcioalidade que lista as portas COM disponiveis no PC e define por onde vai ser o envio
# Verificar a funcionalidade do chenck_sum. A exibição está mostrando apenas 1 ao invés de 10 no primeiro byte
# Deve ser enviado no formato inteiro e não em char ???????????
# Preciso descobrir. Parece que nosso código funciona assim. Mas talvez esteja errado

# COMENTAR AS PRINCIPAIS PARTES DO CODIGO