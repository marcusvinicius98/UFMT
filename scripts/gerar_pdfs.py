import asyncio
from playwright.async_api import async_playwright
import re
from pathlib import Path

links = [
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10924582&turma=FB&periodo=20161",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10827340&turma=FB&periodo=20161",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10829914&turma=FB&periodo=20161",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10530696&turma=FB&periodo=20161",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10829959&turma=FB&periodo=20162",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10827358&turma=FB&periodo=20162",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10827366&turma=FB&periodo=20162",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10829917&turma=FB&periodo=20171",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10827617&turma=FB&periodo=20171",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10827374&turma=FB&periodo=20171",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10829921&turma=FB&periodo=20172",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10827625&turma=FB&periodo=20172",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10827676&turma=FB&periodo=20172",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10827633&turma=FB&periodo=20181",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10829940&turma=FB&periodo=20181",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10829920&turma=FB&periodo=20181",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10230556&turma=CBA&periodo=20181",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10827684&turma=FB&periodo=20182",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10829960&turma=FB&periodo=20182",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10829916&turma=FB&periodo=20182",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10829918&turma=FB&periodo=20191",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10829934&turma=FB&periodo=20191",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10827730&turma=FB&periodo=20191",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10330448&turma=HIN&periodo=20191",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10829963&turma=FB&periodo=20192",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10516450&turma=FB&periodo=20192",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10829945&turma=FB&periodo=20192",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10827765&turma=FB&periodo=20192",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10829919&turma=FB&periodo=20201",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10827749&turma=FB&periodo=20201",
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10829922&turma=FB&periodo=20201"
]

async def main():
    output_dir = Path("pdfs_planos")
    output_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()

        for url in links:
            match = re.search(r'periodo=(\d{6})', url)
            if not match:
                continue
            periodo = match.group(1)
            semestre = f"{periodo[:4]}_{periodo[4:]}"
            folder = output_dir / semestre
            folder.mkdir(parents=True, exist_ok=True)
            codigo = url.split("codigo=")[-1].split("&")[0]
            file_path = folder / f"{codigo}.pdf"

            page = await context.new_page()
            await page.goto(url)
            await page.wait_for_timeout(5000)
            await page.pdf(path=str(file_path), format="A4", print_background=True)
            print(f"Salvo: {file_path}")
            await page.close()

        await browser.close()

asyncio.run(main())
