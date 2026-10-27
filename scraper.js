const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  const url = 'https://www.sa.playblackdesert.com/pt-BR/News/Notice?boardType=3';
  console.log(`Acessando: ${url}`);
  
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(5000);

    // 1. Pega todos os links dos eventos na página principal
    const links = await page.$$eval('a[href*="Notice/Detail"]', anchors => {
      const unique = new Set();
      const items = [];
      anchors.forEach(a => {
        if (!a.href.includes('groupContentNo')) return;
        if (unique.has(a.href)) return;
        unique.add(a.href);
        
        // Tenta pegar o título e a imagem do card
        let title = a.innerText.trim().split('\n')[0];
        if (!title) {
            const img = a.querySelector('img');
            if (img) title = img.alt;
        }
        const imgEl = a.querySelector('img');
        
        if (title && title.length > 3) {
          items.push({
            url: a.href,
            title: title.replace(/\s+/g, ' ').trim(),
            image: imgEl ? imgEl.src : null
          });
        }
      });
      return items;
    });

    console.log(`Encontrados ${links.length} links. Abrindo cada um para ler os detalhes...`);

    const eventos = [];

    // 2. Para cada link, abre a página e tenta ler a data
    for (const item of links) {
      console.log(`Verificando: ${item.title}`);
      
      try {
        const detailPage = await browser.newPage();
        await detailPage.goto(item.url, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await detailPage.waitForTimeout(2000); // Espera o JS carregar

        // Pega o texto da página para procurar a data
        const bodyText = await detailPage.evaluate(() => document.body.innerText);

        let daysRemaining = null;
        let permanent = false;

        // Procura por "Permanente" ou "Sempre disponível"
        if (bodyText.includes('Permanente') || bodyText.includes('Sempre disponível')) {
          permanent = true;
        } else {
          // Tenta achar padrões de data: "até 14 de Maio de 2026" ou "2026-05-14"
          // O site da SA geralmente usa "até DD de Mês de AAAA"
          const dateRegex = /até\s+(\d{1,2})\s+de\s+([A-Za-zç]+)\s+de\s+(\d{4})/i;
          const match = bodyText.match(dateRegex);
          
          if (match) {
            const day = parseInt(match[1]);
            const monthName = match[2].toLowerCase();
            const year = parseInt(match[3]);
            
            const months = {
              'janeiro': 0, 'fevereiro': 1, 'março': 2, 'abril': 3, 'maio': 4, 'junho': 5,
              'julho': 6, 'agosto': 7, 'setembro': 8, 'outubro': 9, 'novembro': 10, 'dezembro': 11
            };
            
            const month = months[monthName] !== undefined ? months[monthName] : null;
            
            if (month !== null) {
              const endDate = new Date(year, month, day);
              const today = new Date();
              today.setHours(0,0,0,0);
              const diffTime = endDate - today;
              daysRemaining = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
              
              if (daysRemaining < 0) daysRemaining = 0; // Já expirou
            }
          }
        }

        eventos.push({
          title: item.title,
          url: item.url,
          image: item.image,
          status: 'andamento',
          daysRemaining: daysRemaining,
          permanent: permanent
        });

        await detailPage.close();
        
        // Pequena pausa para não sobrecarregar o site
        await page.waitForTimeout(500);
        
      } catch (e) {
        console.log(`Erro ao ler ${item.title}: ${e.message}`);
        // Se der erro, salva com os dados básicos
        eventos.push({
          title: item.title,
          url: item.url,
          image: item.image,
          status: 'andamento',
          daysRemaining: null,
          permanent: false
        });
      }
    }

    const data = {
      source: url,
      updatedAt: new Date().toISOString(),
      events: eventos
    };

    if (!fs.existsSync('data')) fs.mkdirSync('data');
    fs.writeFileSync('data/eventos-sa.json', JSON.stringify(data, null, 2));
    console.log(`✅ Sucesso! ${eventos.length} eventos salvos com detalhes.`);
    
  } catch (error) {
    console.error('❌ Erro geral:', error.message);
  } finally {
    await browser.close();
  }
})();
