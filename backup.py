import os
import shutil
import logging
from datetime import datetime, timedelta
import config

# copia os arquivos/pastas que ainda não existem em backup
def sync_recordings():
    logging.info("====== INICIANDO PROCESSO DE BACKUP ======")
    logging.info(f"Origem: {config.SOURCE_DIR}")
    logging.info(f"Destino: {config.BACKUP_DIR}")
    
    copied_files_count = 0
    skipped_files_count = 0
    error_files_count = 0

    if not os.path.isdir(config.SOURCE_DIR):
        logging.error(f"ERRO: O diretório de origem '{config.SOURCE_DIR}' não foi encontrado.") 
        return

    today = datetime.now()

    for i in range(config.RETENTION_DAYS):
        target_date = today - timedelta(days=i)
        date_path = target_date.strftime(r"%Y\%m\%d")
        source_day_path = os.path.join(config.SOURCE_DIR, date_path)

        if os.path.isdir(source_day_path):
            for filename in os.listdir(source_day_path):
                if filename.endswith(".dav"):
                    source_file_path = os.path.join(source_day_path, filename)
                    destination_file_path = os.path.join(config.BACKUP_DIR, date_path, filename)
                    
                    if not os.path.exists(destination_file_path):
                        try:
                            destination_dir = os.path.dirname(destination_file_path)
                            os.makedirs(destination_dir, exist_ok=True)
                            shutil.copy2(source_file_path, destination_file_path)
                            logging.info(f"COPIADO: {filename}")
                            copied_files_count += 1
                        except Exception as e:
                            logging.error(f"FALHA AO COPIAR: {filename}. Motivo: {e}")
                            error_files_count += 1
                    else:
                        skipped_files_count += 1
    
    logging.info("--- Resumo da Execução ---")
    logging.info(f"Arquivos novos copiados: {copied_files_count}")
    logging.info(f"Arquivos já existentes (ignorados): {skipped_files_count}")
    logging.info(f"Arquivos com erro na cópia: {error_files_count}")
    logging.info("====== PROCESSO DE BACKUP FINALIZADO ======")