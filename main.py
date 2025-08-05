from classes.configurador import Configurador
from classes.executores.executor_de_comandos import ExecutorDeComandos
    
if __name__ == "__main__":
    executor = ExecutorDeComandos()

    configurador = Configurador(executor)
    configurador.iniciar()