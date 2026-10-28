import urllib.request
import json
import datetime
import os
import re
from html.parser import HTMLParser

URL = "https://www.sa.playblackdesert.com/pt-BR/News/Notice?boardType=3"

def scrape_events():
    try:
        req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Erro ao acessar o site: {e}")
        return []

    events = []
    # O site do BDO coloca os links e imagens dentro de blocos com a classe "board_list_item"
    # Vamos usar Regex para achar esses blocos
    blocks = re.findall(r'<li[^>]*class="[^"]*board_list_item[^"]*"[^>]*>(.*?)</li>', html, re.DOTALL)
    
    # Se não achar com <li>, tenta com <div>
    if not blocks:
        blocks = re.findall(r'<div[^>]*class="[^"]*board_list_item[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)

    for block in blocks:
        # Extrai o link (URL)
        link_match = re.search(r'href="([^"]+)"', block)
        if not link_match: continue
        
        link = link_match.group(1)
        if link.startswith('/'):
            link = "https://www.sa.playblackdesert.com" + link
            
        # Extrai o Título (geralmente está em um <span class="title"> ou <strong>)
        title_match = re.search(r'<span[^>]*class="[^"]*title[^"]*"[^>]*>(.*?)</span>', block, re.DOTALL)
        if not title_match:
            # Se não achar a classe, pega o texto de qualquer tag dentro do link
            title_match = re.search(r'>([^<]{10,})<', block)
            
        title = title_match.group(1).strip() if title_match else "Evento do BDO"
        title = re.sub(r'<[^>]+>', '', title) # Limpa tags HTML do título
        
        # Extrai a Imagem
        img_match = re.search(r'src="([^"]+)"', block)
        image = img_match.group(1) if img_match else ""
        if image.startswith('//'):
            image = "https:" + image

        events.append({
            "title": title,
            "url": link,
            "image": image,
            "status": "andamento",
            "daysRemaining": 10, # Valor fixo só para o site não bugar o tamanho da barra
            "permanent": False
        })

    # Se o site mudou muito e o regex falhou, vamos pegar qualquer link que tenha "Detail"
    if not events:
        print("Regex principal falhou. Tentando método de fallback...")
        links = re.findall(r'href="(/News/Notice/Detail\?[^"]+)"', html)
        links = list(dict.fromkeys(links))
        
        for link in links[:20]: # Pega os 20 primeiros
            url = "https://www.sa.playblackdesert.com" + link
            # Tenta achar uma imagem perto do link
            events.append({
                "title": "Confira o novo evento no site oficial",
                "url": url,
                "image": "https://s1.pearlcdn.com/SA/Upload/thumbnail/2026/W0CJO31M7OPFROB820260901160712450.400x225.jpg",
                "status": "andamento",
                "daysRemaining": 10,
                "permanent": False
            })

    # Remove eventos duplicados (mesma URL)
    unique_events = []
    seen_urls = set()
    for ev in events:
        if ev['url'] not in seen_urls:
            unique_events.append(ev)
            seen_urls.add(ev['url'])

    return unique_events[:25]

if __name__ == "__main__":
    events = scrape_events()
    print(f"Encontrados {len(events)} eventos.")
    
    data = {
        "source": URL,
        "updatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "events": events
    }
    
    os.makedirs('data', exist_ok=True)
    with open('data/eventos-sa.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("Arquivo data/eventos-sa.json salvo com sucesso!")
