import sys
from PySide6 import QtWidgets
from rdm_dmx_Master import RDM_DMX_Master

app = QtWidgets.QApplication(sys.argv)

window = RDM_DMX_Master(app)
window.show()

app.exec()
window.SendCommand()

# Encontrar as portas serial disponiveis causa travamento. Pq sera?

# Descobrir se é necessário que uma luminaria com mais de uma cor tenha seu inicio em um slot especifico. Divisivel por 4 por exemplo
# Também descobrir se há uma sequencia de cores que deve ser seguida

# Colocar dicas quando passar o mouse por cima dos campos RDM

# Fazer tratamento das outras respostas do RDM

# Adaptar exibição de resposta. Criar elemento visual que altera cor ou texto
# Com isso, se cliar ou passar mouse por cima ele diz pq deu errado ou certo

# Ajustar Checksum. Não estou calculando do jeito certo

# Ver se precisa decodificar os outros campos dos pacotes RDM. Ex: dados vindos do device_info