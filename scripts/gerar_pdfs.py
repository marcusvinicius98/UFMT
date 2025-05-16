import os
import asyncio
from playwright.async_api import async_playwright

# Lista de URLs dos planos de ensino
urls = [
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
    "https://academico-siga.ufmt.br/ufmt.portalacademico/PlanoEnsino/Details?codigo=10829922&turma=FB&periodo=20202"
]


async def salvar_planos():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        for url in urls:
            print(f"Acessando: {url}")
            await page.goto(url)

            # Extrair período do parâmetro da URL
            try:
                periodo = url.split("periodo=")[-1]
                semestre = f"{periodo[:4]}_{periodo[-1]}"
            except Exception:
                print(f"Não foi possível extrair o período de {url}")
                continue

            # Esperar nome da disciplina carregar
            try:
                await page.wait_for_selector("span.card-title", timeout=5000)
                titulo_element = await page.query_selector("span.card-title")
                titulo_texto = await titulo_element.inner_text()
                nome_disciplina = titulo_texto.split("#")[0].strip()
                nome_disciplina_limpo = "".join(c for c in nome_disciplina if c.isalnum() or c in (" ", "-")).replace(" ", "_")
            except Exception:
                print(f"Não foi possível extrair o nome da disciplina de {url}")
                continue

            # Criar diretório do semestre
            pasta_semestre = f"pdfs_planos/{semestre}"
            os.makedirs(pasta_semestre, exist_ok=True)

            # Caminho final do PDF
            path_pdf = os.path.join(pasta_semestre, f"{nome_disciplina_limpo}.pdf")

            # Gerar PDF
            await page.pdf(path=path_pdf, format="A4")
            print(f"Salvo em: {path_pdf}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(salvar_planos())
