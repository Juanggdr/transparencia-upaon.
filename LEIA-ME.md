# Transparência Upaon Açu

Site do Portal Upaon Açu com **todos os contratos da Prefeitura de Raposa (2020 a 2026)**,
por ano, mês, área e tipo de gasto, com o documento oficial de cada contrato.

## O que tem em cada pasta

| Arquivo | Para que serve |
|---|---|
| `index.html` | O site inteiro |
| `data/raposa.json` | Contratos e aditivos lidos do Diário Oficial (1.405 edições) |
| `data/raposa_pncp.json` | Contratos do PNCP com o PDF do contrato assinado (o robô cria e atualiza) |
| `scripts/atualizar_pncp.py` | Robô que baixa os contratos novos do PNCP |
| `.github/workflows/atualizar.yml` | Faz o robô rodar sozinho todo dia às 06:17 |
| `INICIAR-SITE.bat` | Abre o site no seu notebook (duplo clique) |

## Como fica no ar 24h (GitHub Pages)

1. Crie uma conta grátis em github.com.
2. Conecte o GitHub ao Claude (Configurações → Conectores → GitHub).
3. Peça ao Claude: "publica o Transparência Upaon Açu". Ele cria o repositório, envia os arquivos e liga o GitHub Pages.
4. O link fica assim: `https://SEU-USUARIO.github.io/transparencia-upaon/`.

## Atualizações

- **PNCP (contratos novos):** automático, todo dia, pelo robô no GitHub.
- **Diário Oficial:** o site do diário bloqueia robôs. Para incluir as edições novas, peça ao Claude
  "atualiza o diário de Raposa". Ele lê as edições novas pelo seu navegador e atualiza `data/raposa.json`.

## Ver no notebook

Dê dois cliques em `INICIAR-SITE.bat`. Ele abre o site em http://localhost:8080
(precisa do Python instalado: python.org).
