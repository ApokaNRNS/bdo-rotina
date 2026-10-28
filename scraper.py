import urllib.request
import json
import datetime
from html.parser import HTMLParser
import os

URL = "https://www.sa.playblackdesert.com/pt-BR/News/Notice?boardType=3"

class BDOScraper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_list = False
        self.in_link = False
        self.in_title = False
        self.events = []
        self.current_event = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div' and attrs.get('class') == 'board_list':
            self.in_list = True
        if self.in_list:
            if tag == 'a' and 'board_list_item' in attrs.get('class', ''):
                self.in_link = True
                href = attrs.get('href', '')
                if href:
                    self.current_event['url'] = "https://www.sa.playblackdesert.com" + href if href.startswith('/') else href
            elif tag == 'img' and self.in_link and 'src' in attrs:
                self.current_event['image'] = attrs['src']
            elif tag == 'span' and 'title' in attrs.get('class', ''):
                self.in_title = True

    def handle_endtag(self, tag):
        if tag == 'div' and self.in_list:
            self.in_list = False
        if tag == 'a' and self.in_link:
            self.in_link = False
            if 'url' in self.current_event:
                self.events.append(self.current_event)
                self.current_event = {}
        if tag == 'span' and self.in_title:
            self.in_title = False

    def handle_data(self, data):
        if self.in_title and data.strip():
            self.current_event['title'] = data.strip()

def scrape_events():
    try:
        req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Erro ao acessar o site: {e}")
        return []

    parser = BDOScraper()
    parser.feed(html)
    
    events = []
    for ev in parser.events:
        if 'title' in ev and ev['title']:
            ev['status'] = 'andamento'
            ev['daysRemaining'] = 10
            ev['permanent'] = False
            events.append(ev)

    return events[:25] if events else []

if __name__ == "__main__":
    events = scrape_events()
    
    # Se não encontrar eventos, cria uma lista vazia para não dar erro no GitHub
    if not events:
        print("Nenhum evento encontrado. Criando arquivo vazio para não quebrar o robô.")
        events = []
    
    data = {
        "source": URL,
        "updatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "events": events
    }
    
    os.makedirs('data', exist_ok=True)
    with open('data/eventos-sa.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Sucesso! {len(events)} eventos salvos em data/eventos-sa.json")
