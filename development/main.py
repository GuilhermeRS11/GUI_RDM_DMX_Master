import sys
from PySide6 import QtWidgets
from rdm_dmx_Master import RDM_DMX_Master

app = QtWidgets.QApplication(sys.argv)

window = RDM_DMX_Master(app)
window.show()

app.exec()

# Encontrar as portas serial disponiveis causa travamento. Pq sera?

# Descobrir se é necessário que uma luminaria com mais de uma cor tenha seu inicio em um slot especifico. Divisivel por 4 por exemplo
# Também descobrir se há uma sequencia de cores que deve ser seguida

# Fazer tratamento das outras respostas do RDM

# Ajustar Checksum. Não estou calculando do jeito certo
# Acho que o escravo da china que esta com defeito

# Ver se precisa decodificar os outros campos dos pacotes RDM. Ex: dados vindos do device_info

# Modificar o parameterData para dizer o que é. Tal como em GET DMX Address

# Verificar a causa no atraso do envio de dados seriais

# Implementar assemble dos dados de 16bits. Separar em dois bytes 