from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import base64
import json
import re
from pathlib import Path
from PyPDF2 import PdfMerger

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

output_dir = Path("pdfs_planos")
output_dir.mkdir(exist_ok=True)

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--print-to-pdf')
options.add_argument('--disable-dev-shm-usage')

for url in links:
    match = re.search(r'periodo=(\d{6})', url)
    if not match:
        continue
    periodo = match.group(1)
    semestre = f"{periodo[:4]}_{periodo[4:]}"
    folder = output_dir / semestre
    folder.mkdir(parents=True, exist_ok=True)

    filename = folder / (url.split("codigo=")[-1].split("&")[0] + ".pdf")

    pdf_path = "/tmp/output.pdf"
    prefs = {
        "printing.print_preview_sticky_settings.appState": json.dumps({
            "version": 2,
            "isHeaderFooterEnabled": False,
            "marginsType": 1,
            "mediaSize": {},
            "scalingType": 3,
            "scaling": "100",
            "isLandscapeEnabled": False,
            "isCssBackgroundEnabled": True
        }),
        "savefile.default_directory": str(folder.absolute())
    }

    options.add_experimental_option("prefs", prefs)
    options.add_argument('--kiosk-printing')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    driver.execute_script('window.print();')
    time.sleep(5)
    driver.quit()

    os.rename("/tmp/output.pdf", filename)

for semester_folder in output_dir.iterdir():
    if semester_folder.is_dir():
        pdfs = list(semester_folder.glob("*.pdf"))
        if not pdfs:
            continue
        merger = PdfMerger()
        for pdf in pdfs:
            merger.append(str(pdf))
        merged_pdf = output_dir / f"{semester_folder.name}.pdf"
        merger.write(str(merged_pdf))
        merger.close()
