import os
import logging
from datetime import datetime, timedelta
import config

# apaga arquivos/pastas com mais de 'RETENTION_DAYS' (config.py)
def cleanup_old_backups():
    logging.info("====== INICIANDO PROCESSO DE LIMPEZA ======")
    
    deleted_files_count = 0
    now = datetime.now()
    cutoff_date = now - timedelta(days=config.RETENTION_DAYS)

    if not os.path.isdir(config.BACKUP_DIR):
        logging.warning(f"Diretório de backup não encontrado para limpeza: {config.BACKUP_DIR}")
        return

    for root, dirs, files in os.walk(config.BACKUP_DIR):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                if file_mod_time < cutoff_date:
                    os.remove(file_path)
                    logging.info(f"APAGADO (antigo): {filename}")
                    deleted_files_count += 1
            except Exception as e:
                logging.error(f"FALHA AO APAGAR ARQUIVO: {file_path}. Motivo: {e}")

    for root, dirs, files in os.walk(config.BACKUP_DIR, topdown=False):
        for name in dirs:
            dir_path = os.path.join(root, name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                logging.info(f"REMOVIDA PASTA VAZIA: {dir_path}")

    logging.info("--- Resumo da Execução ---")
    logging.info(f"Arquivos antigos apagados: {deleted_files_count}")
    logging.info("====== PROCESSO DE LIMPEZA FINALIZADO ======")