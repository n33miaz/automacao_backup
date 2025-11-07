import backup
import cleanup
import logging
import shutil
import config
import os 

def setup_logging():
    log_dir = os.path.dirname(config.LOG_FILE)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Pasta de log criada em: {log_dir}")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ],
    )

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