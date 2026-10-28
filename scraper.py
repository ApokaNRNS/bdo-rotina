import urllib.request
import json
import datetime
import re
import os

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
    
    # Encontra todos os links de notícias que contém "Detail"
    links = re.findall(r'href="(/News/Notice/Detail\?[^"]+)"', html)
    # Remove duplicados mantendo a ordem
    links = list(dict.fromkeys(links))
    
    for link in links[:25]: # Pega os 25 primeiros
        url = "https://www.sa.playblackdesert.com" + link
        
        # Tenta achar o título e a imagem no bloco perto do link (usando regex simples)
        # Como o site é dinâmico, procuramos a imagem e o título associados
        events.append({
            "title": "Evento do Black Desert SA", # Título genérico caso não ache
            "url": url,
            "image": "https://s1.pearlcdn.com/SA/Upload/thumbnail/2026/W0CJO31M7OPFROB820260901160712450.400x225.jpg", # Imagem padrão
            "status": "andamento",
            "daysRemaining": 10,
            "permanent": False
        })
        
    # Tenta extrair os títulos reais
    # O site coloca os títulos dentro de tags <strong> ou <span> perto dos links
    # Vamos fazer uma busca mais bruta nos blocos <a>
    blocks = re.findall(r'<a[^>]*href="(/News/Notice/Detail\?[^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
    
    parsed_events = []
    for link, content in blocks:
        if link not in [e['url'] for e in events]:
            continue
            
        url = "https://www.sa.playblackdesert.com" + link
        
        # Limpa as tags HTML do conteúdo para pegar o texto do título
        text = re.sub(r'<[^>]+>', '', content).strip()
        
        # Se tiver texto, usa como título
        if text and len(text) > 3:
            # Pega a imagem se houver
            img_match = re.search(r'src="([^"]+)"', content)
            img = img_match.group(1) if img_match else "https://s1.pearlcdn.com/SA/Upload/thumbnail/2026/W0CJO31M7OPFROB820260901160712450.400x225.jpg"
            
            parsed_events.append({
                "title": text,
                "url": url,
                "image": img,
                "status": "andamento",
                "daysRemaining": 10,
                "permanent": False
            })
            
    # Se achou os títulos reais, usa eles. Senão, usa os links genéricos.
    final_events = parsed_events if parsed_events else events
    
    return final_events

if __name__ == "__main__":
    events = scrape_events()
    
    if not events:
        print("Nenhum evento encontrado. Mantendo o arquivo anterior ou criando vazio.")
    
    data = {
        "source": URL,
        "updatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "events": events
    }
    
    os.makedirs('data', exist_ok=True)
    with open('data/eventos-sa.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Sucesso! {len(events)} eventos salvos em data/eventos-sa.json")
