import csv
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager

class UltraRobustDemo:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--start-maximized")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        
        stealth(self.driver,
            languages=["es-AR", "es"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

    def run(self, query, target=30):
        url = f"https://www.google.com/maps/search/{urllib.parse.quote(query)}"
        self.driver.get(url)
        print(f"\n{'='*50}\n🚀 INICIANDO DEMO PROFESIONAL (Target: {target})\n{'='*50}")
        time.sleep(6)

        leads = []
        seen = set()

        while len(leads) < target:
            # 1. Intentar localizar el panel de resultados
            try:
                pane = self.driver.find_element(By.XPATH, "//div[@role='feed' or contains(@aria-label, 'Resultados')]")
            except:
                print("[!] Panel no detectado, reintentando...")
                self.driver.refresh()
                time.sleep(5)
                continue

            # 2. Scrollear para cargar más
            self.driver.execute_script("arguments[0].scrollTop += 2000", pane)
            time.sleep(2)

            cards = self.driver.find_elements(By.CLASS_NAME, "hfpxzc")
            print(f"[*] Elementos detectados en pantalla: {len(cards)}")

            for card in cards:
                if len(leads) >= target: break
                
                try:
                    name = card.get_attribute("aria-label")
                    if not name or name in seen: continue

                    # Click forzado con JS para evitar que se tilde si hay algo encima
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", card)
                    time.sleep(3) # Tiempo para que cargue la ficha lateral

                    data = {
                        "Empresa": name,
                        "Teléfono": self._extract_info("Teléfono"),
                        "Web": self._extract_info("Sitio web"),
                        "Rating": self._get_text("span.ceNzR"),
                        "Timestamp": time.strftime("%H:%M:%S")
                    }

                    leads.append(data)
                    seen.add(name)
                    print(f"   [✅] {len(leads)}/{target}: {name}")
                    
                    self._save(leads)

                except Exception as e:
                    continue

            # Si después de procesar todo no llegamos al target, hacemos scroll mas fuerte
            if len(leads) < target:
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pane)
                time.sleep(3)

        print(f"\n{'='*50}\n🎯 DEMO EXITOSA: 30 LEADS CAPTURADOS\n{'='*50}")
        self.driver.quit()

    def _extract_info(self, label):
        try:
            # Busqueda por XPATH flexible para el panel lateral
            xpath = f"//button[contains(@aria-label, '{label}')] | //div[contains(@aria-label, '{label}')]"
            el = self.driver.find_element(By.XPATH, xpath)
            text = el.get_attribute("aria-label")
            return text.split(":")[-1].strip()
        except:
            return "No disponible"

    def _get_text(self, sel):
        try: return self.driver.find_element(By.CSS_SELECTOR, sel).text
        except: return "N/A"

    def _save(self, data):
        with open("demo_30_leads.csv", "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=data[0].keys())
            w.writeheader()
            w.writerows(data)

if __name__ == "__main__":
    bot = UltraRobustDemo()
    # Usamos una búsqueda amplia para asegurar volumen
    bot.run("Inmobiliarias en Buenos Aires", target=30)
