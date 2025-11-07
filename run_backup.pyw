# retire o 'w' de 'run_python.pyw', caso queria ver a janela de execução

import backup
import cleanup
import logging
import shutil
import config
import os
from datetime import datetime

def setup_logging():
    now = datetime.now()
    log_folder = os.path.join(config.LOG_DIR, now.strftime('%Y\\%m\\%d'))
    
    os.makedirs(log_folder, exist_ok=True)
    
    log_filename = now.strftime('backup-log-%Hh%M.log')
    log_file_path = os.path.join(log_folder, log_filename)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    logging.info(f"====== LOG DESTA EXECUÇÃO SALVO EM: {log_file_path} ======")

def check_disk_space():
    try:
        total, used, free = shutil.disk_usage(config.BACKUP_DIR)
        free_gb = free / (1024**3)
        
        if free_gb < 20:
            logging.warning(f"====== ATENÇÃO: POUCO ESPAÇO EM DISCO! RESTAM: {free_gb:.2f} GB ======")
        else:
            logging.info(f"====== ESPAÇO LIVRE EM DISCO: {free_gb:.2f} GB ======")
    except FileNotFoundError:
        logging.error(f"ERRO: O diretório de backup '{config.BACKUP_DIR}' não foi encontrado.")
        return False
    return True

if __name__ == "__main__":
    setup_logging()

    if check_disk_space():
        backup.sync_recordings()
        cleanup.cleanup_old_backups()
    
    logging.info("====== CICLO DE BACKUP COMPLETO ======\n")

