import requests
from bs4 import BeautifulSoup

# URL dei siti da cui estrarre i dati (modifica con i tuoi URL)
URLS = [
    "https://hattrick.ws/",  # Sito 1
    "https://calcio.monster/streaming-gratis-calcio-1.php",  # Sito 2
]

# Funzione per fare scraping da un singolo sito
def estrai_dati_sito(url):
    # Fai una richiesta GET per scaricare la pagina
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    iptv_channels = []

    # Estrazione per il sito hattrick.ws
    if "hattrick.ws" in url:
        # Estrazione dei canali (match specifici)
        for item in soup.find_all("div", class_="row"):
            nome_canale = item.find("a", class_="game-name").text.strip() if item.find("a", class_="game-name") else "Nome sconosciuto"
            stream_link = item.find("a", href=True)["href"] if item.find("a", href=True) else "Link non disponibile"
            logo_link = item.find("img")["src"] if item.find("img") else "Logo non disponibile"

            iptv_channels.append((nome_canale, stream_link, logo_link))

    # Estrazione per il sito calcio.monster
    elif "calcio.monster" in url:
        # Estrazione dei canali (match specifici)
        for item in soup.find_all("li"):
            nome_canale = item.find("div", class_="kode_ticket_text").find("div", class_="ticket_title").text.strip() if item.find("div", class_="kode_ticket_text") else "Nome sconosciuto"
            stream_link = item.find("a", href=True)["href"] if item.find("a", href=True) else "Link non disponibile"
            logo_link = "Logo non disponibile"  # Questo sito non sembra avere un logo, quindi lo impostiamo su un valore di fallback

            iptv_channels.append((nome_canale, stream_link, logo_link))

    return iptv_channels

# Funzione per estrarre i dati da più siti
def estrai_dati_da_più_siti(urls):
    tutti_canali = []

    for url in urls:
        print(f"Estraendo dati da: {url}")
        canali_sito = estrai_dati_sito(url)
        tutti_canali.extend(canali_sito)

    return tutti_canali

# Estrai i dati da tutti i siti nella lista
canali_totali = estrai_dati_da_più_siti(URLS)

# Controlla i dati estratti
for nome, link, logo in canali_totali:
    print(f"Canale: {nome}")
    print(f"Link: {link}")
    print(f"Logo: {logo}")
    print("---------------")

# Creiamo il file M3U con loghi
m3u_content = "#EXTM3U\n"
for nome, stream, logo in canali_totali:
    m3u_content += f'#EXTINF:-1 tvg-logo="{logo}", {nome}\n{stream}\n'

# Salviamo il file M3U
with open("lista_iptv.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)

print("✅ Lista IPTV aggiornata con loghi e salvata come lista_iptv.m3u")
