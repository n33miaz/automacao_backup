# Automação de Backup para Gravações CFTV

Este projeto contém um conjunto de scripts em Python que criei para automatizar o backup de gravações de um sistema de CFTV da Intelbras, garantindo a integridade e a retenção dos dados conforme exigido por contrato.

## Problemática

Na empresa JC Gestão de Riscos, utilizamos um sistema de CFTV da Intelbras para monitoramento de um cliente. As gravações são salvas em um disco local (`E:`), seguindo a estrutura de pastas `Ano/Mês/Dia`.

O grande problema que enfrentávamos era a instabilidade da plataforma: **em caso de erros, o sistema apagava automaticamente todas as gravações salvas**, nos deixando sem os registros. Isso era inaceitável, pois nosso contrato com o cliente exige que mantenhamos um histórico de **30 dias de gravações** ininterruptas. Perder esses dados representava um risco operacional e contratual enorme.

## Solução

Para resolver essa falha e garantir que nunca mais perdêssemos um arquivo, desenvolvi esta solução de backup automatizado. A ideia foi criar um processo robusto e independente da plataforma de CFTV.

Criei um segundo disco em nosso servidor (`D:`), conectado via iSCSI, para servir como um repositório seguro. Em seguida, desenvolvi os scripts em Python contidos neste repositório para realizar as seguintes tarefas:

1.  **Executar a cada 10 minutos** através de um Agendador de Tarefas.
2.  **Verificar a pasta de origem** (`E:\Intelbras\LocalRecording`) em busca de novos arquivos de gravação (`.dav`) dos últimos 30 dias.
3.  **Copiar apenas os arquivos novos** para o disco de backup, replicando a mesma estrutura de pastas `Ano/Mês/Dia`. Isso torna o processo extremamente rápido e eficiente.
4.  **Realizar a limpeza do backup**, apagando automaticamente do disco de backup (`D:`) as gravações com mais de 30 dias para gerenciar o espaço de armazenamento.
5.  **Monitorar o espaço em disco** e registrar um alerta no log caso o espaço livre fique abaixo de um limite crítico.
6.  **Gerar um log detalhado** de todas as operações (arquivos copiados, arquivos apagados, erros, alertas), permitindo uma auditoria completa do processo.

Com essa automação, mesmo que a plataforma principal falhe e apague os arquivos originais, temos uma cópia segura e intacta em nosso disco de backup.

## Principais Funcionalidades

*   **Backup Incremental:** Copia apenas os arquivos que ainda não existem no destino.
*   **Política de Retenção:** Mantém um histórico de 30 dias no backup, apagando o que for mais antigo.
*   **Logging Completo:** Todas as ações são registradas em `backup_log.log`.
*   **Estrutura Modular:** O código é dividido em arquivos para facilitar a manutenção:
    *   `config.py`: Centraliza todas as configurações de pastas e regras.
    *   `backup.py`: Contém a lógica de cópia e sincronização.
    *   `cleanup.py`: Contém a lógica de limpeza dos arquivos antigos.
    *   `run_backup.py`: Orquestra todo o processo.
*   **Monitoramento de Espaço:** Alerta sobre baixo espaço em disco no log.
*   **Robustez:** Lida com erros (como arquivos em uso) sem interromper o processo e cria pastas necessárias automaticamente.

## Como Utilizar

### Pré-requisitos
*   [Python](https://www.python.org/downloads/) instalado.

### Configuração

*  Ajuste o arquivo `config.py` para corresponder ao seu ambiente:
    *   `SOURCE_DIR`: Pasta onde o sistema salva as gravações.
    *   `BACKUP_DIR`: Pasta onde as cópias serão enviadas.
    *   `LOG_FILE`: Caminho onde o arquivo de log será salvo.
    *   `RETENTION_DAYS`: Número de dias que as gravações devem ser mantidas.

## Conclusão

Este projeto foi uma solução simples e eficaz para um problema crítico, trazendo tranquilidade e garantindo a conformidade com nosso contrato. Sinta-se à vontade para utilizá-lo e adaptá-lo às suas necessidades.