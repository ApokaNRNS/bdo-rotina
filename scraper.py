import urllib.request
import json
import datetime
import os

URL_API = "https://www.sa.playblackdesert.com/pt-BR/News/Notice?boardType=3"

def fetch_events():
    try:
        # Tenta buscar o HTML da página principal
        req = urllib.request.Request(URL_API, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return []

    events = []
    
    # Vamos procurar por URLs de notícias no HTML
    import re
    # Busca strings que começam com /News/Notice/Detail?groupContentNo=
    matches = re.finditer(r'/News/Notice/Detail\?groupContentNo=(\d+)', html)
    seen_ids = set()
    
    for match in matches:
        group_id = match.group(1)
        if group_id in seen_ids:
            continue
        seen_ids.add(group_id)
        
        # Constrói a URL completa
        url = f"https://www.sa.playblackdesert.com/News/Notice/Detail?groupContentNo={group_id}&countryType=pt-BR"
        
        events.append({
            "title": f"Evento do Black Desert SA (ID: {group_id})",
            "url": url,
            "image": "https://s1.pearlcdn.com/SA/Upload/thumbnail/2026/W0CJO31M7OPFROB820260901160712450.400x225.jpg",
            "status": "andamento",
            "daysRemaining": 10,
            "permanent": False
        })
        
        if len(events) >= 20:
            break

    return events

if __name__ == "__main__":
    events = fetch_events()
    
    if not events:
        print("Aviso: Nenhum evento encontrado. O site pode estar bloqueando o robô.")
        # Se falhar, mantém os eventos antigos (se existirem)
        if os.path.exists('data/eventos-sa.json'):
            print("Mantendo o arquivo antigo para não quebrar o site.")
            exit(0)
    
    data = {
        "source": URL_API,
        "updatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "events": events
    }
    
    os.makedirs('data', exist_ok=True)
    with open('data/eventos-sa.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Sucesso! {len(events)} eventos salvos.")
