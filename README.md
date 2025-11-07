# Automação de Backup para Gravações CFTV

Este projeto contém um conjunto de scripts em Python que criei para automatizar o backup de gravações de um sistema de CFTV da Intelbras, garantindo a integridade e a retenção dos dados conforme exigido por contrato.

## Problemática

Na empresa JC Gestão de Riscos, utilizamos um sistema de CFTV da Intelbras para monitoramento de um cliente. As gravações são salvas em um disco local (`E:`), seguindo a estrutura de pastas `Ano/Mês/Dia`.

O grande problema que enfrentávamos era a instabilidade da plataforma: **em caso de erros, o sistema apagava automaticamente todas as gravações salvas**, nos deixando sem os registros. Isso era inaceitável, pois nosso contrato com o cliente exige que mantenhamos um histórico de **31 dias de gravações** ininterruptas. Perder esses dados representava um risco operacional e contratual enorme.

## Solução

Para resolver essa falha e garantir que nunca mais perdêssemos um arquivo, desenvolvi esta solução de backup automatizado. A ideia foi criar um processo robusto e independente da plataforma de CFTV.

Criei um segundo disco em nosso servidor (`D:`), conectado via iSCSI, para servir como um repositório seguro. Em seguida, desenvolvi os scripts em Python contidos neste repositório para realizar as seguintes tarefas:

1.  **Executar a cada 10 minutos** através de um Agendador de Tarefas.
2.  **Verificar a pasta de origem** (`E:\Intelbras\LocalRecording`) em busca de novos arquivos de gravação (`.dav`) dos últimos 31 dias.
3.  **Copiar apenas os arquivos novos** para o disco de backup, replicando a mesma estrutura de pastas `Ano/Mês/Dia`.
4.  **Realizar a limpeza do backup**, apagando automaticamente do disco de backup as gravações com mais de 31 dias para gerenciar o espaço.
5.  **Monitorar o espaço em disco** e registrar um alerta no log caso o espaço livre fique abaixo de um limite crítico.
6.  **Gerar um log único e detalhado para cada execução**, permitindo uma auditoria precisa e facilitando a análise de falhas.

Com essa automação, mesmo que a plataforma principal falhe e apague os arquivos originais, temos uma cópia segura e intacta em nosso disco de backup.

## Principais Funcionalidades

*   **Backup Incremental:** Copia apenas os arquivos que ainda não existem no destino, tornando o processo muito rápido.
*   **Política de Retenção:** Mantém um histórico de 31 dias no backup, apagando o que for mais antigo de forma automática.
*   **Logs Granulares por Execução:** Em vez de um único arquivo de log, o sistema cria um novo arquivo para cada execução, organizado em pastas por `Ano/Mês/Dia` e nomeado com `Hora-Minuto-Segundo`, facilitando a consulta.
*   **Execução Silenciosa:** Configurado para rodar em segundo plano (`background`) sem exibir nenhuma janela de console.
*   **Estrutura Modular:** O código é dividido em arquivos para facilitar a manutenção:
    *   `config.py`: Centraliza todas as configurações de pastas e regras.
    *   `backup.py`: Contém a lógica de cópia e sincronização.
    *   `cleanup.py`: Contém a lógica de limpeza dos arquivos antigos.
    *   `run_backup.py`: Orquestra todo o processo.
*   **Monitoramento de Espaço:** Alerta sobre baixo espaço em disco no log.
*   **Robustez:** Lida com erros (como arquivos em uso) sem interromper o processo e cria as pastas de destino (backup e logs) automaticamente.

## Como Utilizar

### Pré-requisitos
*   [Python](https://www.python.org/downloads/windows/) instalado.

### Configuração

1.  Clone este repositório para uma pasta no seu servidor (ex: `C:\Scripts\BackupCFTV`).
2.  Ajuste o arquivo `config.py` para corresponder ao seu ambiente:
    *   `SOURCE_DIR`: Pasta onde o sistema de CFTV salva as gravações.
    *   `BACKUP_DIR`: Pasta no disco de backup para onde as cópias serão enviadas.
    *   `LOG_DIR`: **Diretório raiz** onde as pastas de log (`AAAA\MM\DD`) serão criadas.
    *   `RETENTION_DAYS`: Número de dias que as gravações devem ser mantidas no backup.

## Conclusão

Este projeto foi uma solução simples e eficaz para um problema crítico, trazendo tranquilidade e garantindo a conformidade com nosso contrato. Sinta-se à vontade para utilizá-lo e adaptá-lo às suas necessidades.
