"""Robô diário: baixa do PNCP todos os contratos da Prefeitura de Raposa/MA
e os links dos documentos (PDF do contrato assinado).

Gera data/raposa_pncp.json. Roda no GitHub Actions todo dia, mas também
funciona no notebook:  python scripts/atualizar_pncp.py
Só usa a biblioteca padrão do Python.
"""
import json
import os
import time
import urllib.parse
import urllib.request

CNPJ = "01612325000198"
BUSCA = "https://pncp.gov.br/api/search/"
ARQ = "https://pncp.gov.br/api/pncp/v1/orgaos/{cnpj}/contratos/{ano}/{seq}/arquivos"
SAIDA = os.path.join(os.path.dirname(__file__), "..", "data", "raposa_pncp.json")
UA = {"User-Agent": "TransparenciaUpaonAcu/1.0 (+instagram.com/portal.upaon.acu)"}


def get_json(url, tentativas=4):
    for i in range(tentativas):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001
            if i == tentativas - 1:
                raise
            print("  tentando de novo:", e)
            time.sleep(3 * (i + 1))


def buscar_contratos():
    itens, pagina = [], 1
    while True:
        q = urllib.parse.urlencode({
            "q": CNPJ, "tipos_documento": "contrato", "ordenacao": "-data",
            "pagina": pagina, "tam_pagina": 500, "ufs": "MA",
        })
        j = get_json(f"{BUSCA}?{q}")
        lote = j.get("items") or []
        itens += lote
        print(f"PNCP: {len(itens)} de {j.get('total')}")
        if not lote or len(itens) >= (j.get("total") or 0):
            break
        pagina += 1
    return [i for i in itens if i.get("orgao_cnpj") == CNPJ and not i.get("cancelado")]


def main():
    antigo = {}
    if os.path.exists(SAIDA):
        with open(SAIDA, encoding="utf-8") as f:
            for c in json.load(f).get("contratos", []):
                antigo[c["controle"]] = c

    contratos = []
    for i in buscar_contratos():
        controle = i.get("numero_controle_pncp")
        url_item = i.get("item_url") or ""  # /contratos/<cnpj>/<ano>/<seq>
        partes = url_item.strip("/").split("/")
        ano, seq = (partes[2], partes[3]) if len(partes) >= 4 else (i.get("ano"), i.get("numero_sequencial"))
        c = {
            "controle": controle,
            "numero": i.get("numero_contrato_empenho") or i.get("title"),
            "titulo": i.get("title"),
            "ano": str(ano),
            "seq": str(seq),
            "data": i.get("data_assinatura"),
            "vigencia_fim": i.get("data_fim_vigencia"),
            "valor": i.get("valor_global"),
            "empresa": i.get("fornecedor_nome"),
            "cnpj": i.get("fornecedor_ni"),
            "modalidade": i.get("modalidade_licitacao_nome"),
            "tipo": i.get("tipo_contrato_nome"),
            "objeto": i.get("description"),
            "pagina": f"https://pncp.gov.br/app{url_item}" if url_item else None,
        }
        velho = antigo.get(controle)
        if velho and velho.get("arquivos") and velho.get("valor") == c["valor"]:
            c["arquivos"] = velho["arquivos"]
        else:
            try:
                arqs = get_json(ARQ.format(cnpj=CNPJ, ano=ano, seq=seq))
                c["arquivos"] = [{"titulo": a.get("titulo"), "tipo": a.get("tipoDocumentoNome"), "url": a.get("url")} for a in arqs]
                time.sleep(0.3)
            except Exception as e:  # noqa: BLE001
                print("  sem arquivos para", controle, e)
                c["arquivos"] = []
        contratos.append(c)

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8") as f:
        json.dump({
            "fonte": "PNCP - Portal Nacional de Contratações Públicas",
            "atualizado": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "contratos": contratos,
        }, f, ensure_ascii=False, separators=(",", ":"))
    print(f"OK: {len(contratos)} contratos salvos em {SAIDA}")


if __name__ == "__main__":
    main()
