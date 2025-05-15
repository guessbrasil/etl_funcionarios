import time
import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from main import process_file
from config import settings

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.xls'):
            logging.info(f"Novo arquivo detectado: {event.src_path}")
            time.sleep(1)  
            process_file(event.src_path)

def process_old_files():

    for arquivo in os.listdir(settings.ENTRADA_DIR):
        if arquivo.lower().endswith('.xls'):
            caminho = os.path.join(settings.ENTRADA_DIR, arquivo)
            logging.info(f"Processando arquivo antigo: {caminho}")
            process_file(caminho)

def check_stop_condition():

    return os.path.exists('stop.txt')

if __name__ == "__main__":
    logging.basicConfig(
        filename=settings.LOGFILE,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )

    path = settings.ENTRADA_DIR
    event_handler = NewFileHandler()
    observer = Observer()

    # Processar arquivos antigos ao iniciar
    process_old_files()

    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    logging.info(f"Monitorando a pasta: {path}")

    try:
        while True:
            if check_stop_condition():
                logging.info("Arquivo de stop detectado. Parando o monitoramento.")
                observer.stop()
                break
            print("Aguardando...")    
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
