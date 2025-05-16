import os
import re
import asyncio
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright

# Lista de URLs dos planos
LINKS = [
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10924582&turma=FB&periodo=20161",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10827340&turma=FB&periodo=20161",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10829914&turma=FB&periodo=20161",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10530696&turma=FB&periodo=20161",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10829959&turma=FB&periodo=20162",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10827358&turma=FB&periodo=20162",
]

def extrair_periodo_da_url(url):
    qs = parse_qs(urlparse(url).query)
    return qs.get('periodo', ['Desconhecido'])[0]

async def gerar_pdfs():
    output_dir = Path("pdfs_planos")
    output_dir.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        for link in LINKS:
            print(f"Acessando: {link}")
            try:
                await page.goto(link, timeout=60000)
                await page.wait_for_selector("input[value='Imprimir']", timeout=15000)

                periodo = extrair_periodo_da_url(link)
                pdf_dir = output_dir / periodo
                pdf_dir.mkdir(parents=True, exist_ok=True)

                codigo_match = re.search(r"codigo=(\d+)", link)
                codigo = codigo_match.group(1) if codigo_match else "sem_codigo"

                await page.pdf(path=str(pdf_dir / f"{codigo}.pdf"), format="A4")
            except Exception as e:
                print(f"Erro ao processar {link}: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(gerar_pdfs())
