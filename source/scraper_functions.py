# En este archivo definimos las funciones que empleará nuestro sistema de web_scrapping

# Declaramos las librerías que usaremos
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm
import requests


# Nuestro dataset estará formado por una lista (documento) de listas (filas), que posteriormente
# transformaremos a formato CSV. Rellenamos la primera fila con los nombres de las cabeceras
# (los campos "*_upper" y "*_lower" se refieren a los márgenes de error superior e inferior, respectivamente)
dataset = [['name', 'version', 'release', 'gps', 'mass_1', 'mass_1_upper', 'mass_1_lower', 'mass_2', 'mass_2_upper',
            'mass_2_lower', 'network_snr', 'network_snr_upper', 'network_snr_lower', 'distance', 'distance_upper',
            'distance_lower', 'chi_eff', 'chi_eff_upper', 'chi_eff_lower', 'total_mass', 'total_mass_upper', 
            'total_mass_lower', 'chirp_mass', 'chirp_mass_upper', 'chirp_mass_lower', 'detector_frame_chirp_mass', 
            'detector_frame_chirp_mass_upper', 'detector_frame_chirp_mass_lower', 'redshift', 'redshift_upper', 
            'redshift_lower', 'false_alarm_rate', 'p_astro', 'final_mass', 'final_mass_upper', 'final_mass_lower']]


# Declaramos nuestro navegador
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)


def click_checkbox(checkbox_text):
    """Función para marcar una checkbox basada en el texto que contiene"""
    # Localizamos el checkbox
    checkbox = driver.find_element(By.XPATH, f"//label[text()='{checkbox_text}']/input")
    # Comprobamos si está checkeado
    if checkbox.get_attribute("checked") != "true":
        # Hacemos Click para marcar el checkbox
        driver.execute_script("arguments[0].click();", checkbox)


def get_value_upper_lower(field):
    """Función para tratar columnas numéricas que puedan tener valores de error superior e inferior"""
    # Tomamos el valor del campo, desechando el valor numérico "escondido" usado para ordenar,
    # y los demás posibles valores restantes (errores superior e inferior)
    if '--' in field.text:
        return None, None, None
    try:
        value = field.text.split(' ')[1].split('\n')[0]
    except:
        print(field.text)
        return None, None, None
    # Obtenemos el valor del error superior (si existe)
    try:
        upper = field.find_element(By.CSS_SELECTOR, "sup").text
    except NoSuchElementException:
        upper = None
    # Obtenemos el valor del error inferior (si existe)
    try:
        lower = field.find_element(By.CSS_SELECTOR, "sub").text
    except NoSuchElementException:
        lower = None
    # Retornamos los 3 valores
    return value, upper, lower


def get_value_potential_spaces(field):
    """Función para tratar campos que puedan tener valores que contengan espacios (ej.: '≥ 0.99')"""
    # Tomamos el valor del campo, desechando el valor numérico "escondido" usado por los desarrolladores 
    # de la web para favorecer la ordenación, y tomamos todo aquello que siga detrás
    if '--' in field.text:
        return None
    return ' '.join(field.text.split(' ')[1:])


def execute_form(fecha_inicio, fecha_fin):
    """Función que rellena y ejecuta el formulario"""
    # Comprobamos el user-Agent para evitar problemas   
    url = 'https://www.gw-openscience.org'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'}
    #response = requests.get(url, headers=headers)
    
    
    # Abrimos nuestra web
    driver.get(url, headers=headers)

    # Seleccionamos en el menú eventos y catálogos
    elem = driver.find_element(By.XPATH, "//a[contains(text(), 'Events and Catalogs')]")   

    # Hacemos Click
    driver.execute_script("arguments[0].click();", elem)
    # Esperamos a que cargue
    driver.implicitly_wait(10)

    # Pulsamos el botón query de la ventana que acaba de cargar
    elem2 = driver.find_element(By.XPATH, "//button[text()='Query']").click() 
    # Esperamos a que se cargue el formulario
    driver.implicitly_wait(10)

    # Vamos a rellenar el formulario
    # Comenzamos por los selectores
    select = Select(driver.find_element(By.ID,'mul-release-sel'))

    # Vamos a seleccionar elementos por su nombre, son las diferentes releases
    select.select_by_visible_text('GWTC-1-marginal')
    select.select_by_visible_text('GWTC-1-confident')
    select.select_by_visible_text('O3_IMBH_marginal')
    select.select_by_visible_text('GWTC-2')
    select.select_by_visible_text('GWTC-2.1-marginal')
    select.select_by_visible_text('GWTC-2.1-confident')
    select.select_by_visible_text('GWTC-3-marginal')
    select.select_by_visible_text('GWTC-3-confident')
    select.select_by_visible_text('Initial_LIGO_Virgo')
    
    # Ahora metemos las fechas "desde" y "hasta"
    imputFecha1 = driver.find_element(By.XPATH,"//div[@id='min-datetime-tbox']/input")
    imputFecha1.send_keys(fecha_inicio+'T00:00:00')  
    imputFecha2 = driver.find_element(By.XPATH,"//div[@id='max-datetime-tbox']/input")
    imputFecha2.send_keys(fecha_fin+'T00:00:00')  
    
    # Ahora marcamos el checkbox para que nos den la última versión de las detecciones
    # De este modo no tendremos repetidos
    checkbox = driver.find_element(By.XPATH,"//label[@id='version-tbox']/input")
    # Hacemos Click para marcar el checkbox
    driver.execute_script("arguments[0].click();", checkbox)
    
    # Ya tenemos todo, pulsamos el botón submit para generar la tabla con los datos
    # Localizamos el botón
    boton = driver.find_element(By.ID, 'submit-query-btn')
    # Lo pulsamos
    driver.execute_script("arguments[0].click();", boton)
    # Esperamos a que se cargue la tabla
    driver.implicitly_wait(10)
    
    # Cuidado que no selecciona todas las columnas, debemos seleccionar lo que deseamos ver
    # Pulsamos el botón para desplegar el selector de columnas
    desplegable = driver.find_element(By.CLASS_NAME ,'tablesaw-columntoggle-btnwrap').click()
    
    # Ahora ya vemos los selectores de columnas, comprobaremos que estén todos seleccionados,
    # pulsando aquellos que no lo estén.
    # Utilizamos función "click_checkbox" para marcar todas las casillas (columnas) deseadas:
    casillas = ['Version', 'Release', 'GPS', 'Mass 1 (M☉)', 'Mass 2 (M☉)', 'Network SNR',
                'Distance (Mpc)', 'χeff', 'Total Mass (M☉)', 'Chirp Mass (M☉)', 
                'Detector Frame Chirp Mass (M☉)', 'Redshift', 'False Alarm Rate (yr-1)', 
                'Pastro', 'Final Mass (M☉)']
    for casilla in casillas:
        click_checkbox(casilla)
        
    # Pulsamos el botón para ocultar el desplegable y poder trabajar cómodamente
    desplegable = driver.find_element(By.CLASS_NAME ,'tablesaw-columntoggle-btnwrap').click()
    
    # Ya tenemos la tabla en pantalla, ahora la recorreremos para obtener los datos
    # Primeramente, obtenemos cada una de sus filas (excluyendo la primera, las cabeceras)
    detecciones = driver.find_elements(By.CSS_SELECTOR, "tr")[1:]

    # Y con esto obtenemos el dataset. Antes de procesarlo preparamos la barra de progreso
    for d in tqdm(detecciones, desc ="Procesando la tabla"):
       
        # Dividimos la fila en sus columnas
        d = d.find_elements(By.CSS_SELECTOR, "td")
        
        # Tratamos los valores numéricos con posibles medidas de error
        mass1, mass2, network, distance, hi_eff, total_mass, chirp_mass, detector_frame_chirp_mass, \
        redshift, final_mass = map(get_value_upper_lower, [d[4], d[5], d[6], d[7], d[8], d[9], d[10],
        d[11], d[12], d[15]])
        # Tratamos los valores con posibles espacios en ellos
        false_alarm_rate, p_astro = map(get_value_potential_spaces, [d[13], d[14]])
        # Añadimos la línea correspondiente al dataset, tratando todos sus campos adecuadamente
        # (aplicamos "get_value_upper_lower", "get_value_potential_spaces" y también cuidamos
        # de convertir todos los valores "--" a empty string (""))
        dataset.append(list(map(lambda valor: valor.replace('--', '') if valor else '',
            [d[0].text, d[1].text, d[2].text, d[3].text, 
            mass1[0], mass1[1], mass1[2], 
            mass2[0], mass2[1], mass2[2],
            network[0], network[1], network[2],
            distance[0], distance[1], distance[2],
            hi_eff[0], hi_eff[1], hi_eff[2],
            total_mass[0], total_mass[1], total_mass[2],
            chirp_mass[0], chirp_mass[1], chirp_mass[2],
            detector_frame_chirp_mass[0], detector_frame_chirp_mass[1], detector_frame_chirp_mass[2],
            redshift[0], redshift[1], redshift[2],
            false_alarm_rate, p_astro,
            final_mass[0], final_mass[1], final_mass[2]]
        )))

    return dataset
