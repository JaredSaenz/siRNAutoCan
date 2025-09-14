import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
from bs4 import BeautifulSoup
from quality_nopage_v2 import get_quality

base_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_path)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver_path = os.path.expanduser("~/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def read_fasta(file_path):
    with open(file_path, 'r') as f:
        return f.read()

# Reemplaza 'tu_archivo.fa' con la ruta real de tu archivo FASTA
fasta_file_path = input('Nombre del archivo (.fasta,.fa): ')  # Cambia esto por tu archivo
fasta_file_path = os.path.join(base_path, fasta_file_path)
if not os.path.isfile(fasta_file_path):
    raise FileNotFoundError(f"El archivo {fasta_file_path} no existe.")
fasta_content = read_fasta(fasta_file_path)

try:
    driver = setup_driver()
    driver.get("https://sidirect2.rnai.jp")
    
    # Esperar a que el textarea esté presente y sea interactuable
    wait = WebDriverWait(driver, 10)
    textarea = wait.until(EC.element_to_be_clickable((By.ID, "useq")))
    
    # Limpiar el contenido predeterminado y llenar con el FASTA
    textarea.clear()
    textarea.send_keys(fasta_content)
    
    # Esperar al botón submit y hacer clic
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='design siRNA']")))
    submit_button.click()
    
    # Esperar a que se redirija y cargue la nueva página
    wait.until(lambda d: d.current_url != "https://sidirect2.rnai.jp" or "results" in d.page_source.lower())
    
    # Obtener el HTML de la página redirigida
    redirected_html = driver.page_source
    
    # Parsear el HTML con BeautifulSoup
    soup = BeautifulSoup(redirected_html, 'html.parser')
    
    # Encontrar la tabla objetivo
    table = soup.find('table')  # Asumiendo que es la primera tabla, ajusta si hay varias
    rows = table.find_all('tr')[3:]  # Saltar las primeras 3 filas de encabezado
    
    # Preparar los datos para el CSV
    csv_data = []
    headers = [
        'Target Start', 'Target End', 'Target Sequence', 'Guide Sequence', 
        'Passenger Sequence', 'Ui-Tei', 'Effective siRNA candidates', 
        'Guide Tm (°C)', 'Passenger Tm (°C)', 'Guide Mismatches', 
        'Passenger Mismatches', 'Guide 0(+)', 'Guide 1(+)', 'Guide 2(+)', 
        'Guide 3(+)', 'Passenger 0(-)', 'Passenger 1(-)', 'Passenger 2(-)', 
        'Passenger 3(-)'
    ]
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 17:  # Asegurarse de que la fila tiene suficientes columnas
            continue
            
        # Separar target position
        target_pos = cols[0].text.strip()
        start, end = target_pos.split('-') if '-' in target_pos else ('', '')
        
        # Separar guide y passenger
        seqs = cols[2].text.strip().split('\n')
        guide_seq = seqs[0].strip()[:21] if len(seqs) > 0 else ''
        passenger_seq = seqs[0].strip()[21:] if len(seqs) > 0 else ''
        
        # Determinar Effective siRNA candidates según color
        font = cols[4].find('font')
        if font and 'color3' in font.get('class', []):
            effective = 4
        elif font and 'color2' in font.get('class', []):
            effective = 3
        elif font and 'color1' in font.get('class', []):
            effective = 2
        else:
            effective = 1
        
        # Extraer los datos de las columnas
        row_data = [
            start,
            end,
            cols[1].text.strip(),  # Target Sequence
            guide_seq,
            passenger_seq,
            cols[3].text.strip(),  # Ui-Tei
            effective,
            cols[5].text.strip().replace(' °C', ''),  # Guide Tm
            cols[6].text.strip().replace(' °C', ''),  # Passenger Tm
            cols[7].text.strip().split()[0],  # Guide Mismatches
            cols[8].text.strip().split()[0],  # Passenger Mismatches
            cols[9].text.strip(),  # Guide 0(+)
            cols[10].text.strip(),  # Guide 1(+)
            cols[11].text.strip(),  # Guide 2(+)
            cols[12].text.strip(),  # Guide 3(+)
            cols[13].text.strip(),  # Passenger 0(-)
            cols[14].text.strip(),  # Passenger 1(-)
            cols[15].text.strip(),  # Passenger 2(-)
            cols[16].text.strip()   # Passenger 3(-)
        ]
        csv_data.append(row_data)
    
    # Escribir los datos en siRNA_results.csv con delimitador ';'
    with open('siRNA_results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(headers)
        writer.writerows(csv_data)
    print("Archivo CSV generado: siRNA_results.csv")

    # Leer siRNA_results.csv
    with open('siRNA_results.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        data = list(reader)

    # Procesar cada fila
    results = []
    for row in data:
        seqs = {
            'passenger': row['Passenger Sequence'],
            'guide': row['Guide Sequence']
        }
        qual_dict = get_quality(seqs)
        new_row = row.copy()
        new_row.update(qual_dict)
        results.append(new_row)
    
    # Ordenar por quality descendente
    results.sort(key=lambda x: int(x['quality']), reverse=True)

    # Preparar headers para el nuevo CSV
    quality_headers = ['quality', '#6', '#7', '#8', '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18']
    important_headers = [
        'Target Start', 'Target End', 'Target Sequence', 'Guide Sequence', 
        'Passenger Sequence', 'Effective siRNA candidates'
    ]
    new_headers = important_headers + quality_headers

    # Crear un diccionario que seleccione solo las columnas necesarias
    selected_data = []
    for row in results:
        selected_row = {key: row[key] for key in new_headers}
        selected_data.append(selected_row)

    # Escribir el nuevo CSV con delimitador ';'
    with open('quality_results.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=new_headers, delimiter=';')
        writer.writeheader()
        writer.writerows(selected_data)

    print("Archivo CSV con calificaciones generado: quality_results.csv")

    driver.quit()

except Exception as e:
    print(f"Error durante la ejecución: {e}")
finally:
    if 'driver' in locals():
        driver.quit()