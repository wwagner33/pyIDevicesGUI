from gui.main_window import MainWindow
from app.dependency_check import check_dependencies
from app import logger

if __name__ == "__main__":
    logger.info("Aplicação iniciada.")

    if check_dependencies():
        logger.info("Todas as dependências OK. Iniciando GUI...")
        app = MainWindow()
        app.mainloop()
    else:
        logger.error("Execução abortada por falta de dependências.")
