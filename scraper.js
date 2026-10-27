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

    // Pega os links, limpando títulos sujos
    const links = await page.$$eval('a[href*="Notice/Detail"]', anchors => {
      const unique = new Set();
      const items = [];
      anchors.forEach(a => {
        if (!a.href.includes('groupContentNo') || unique.has(a.href)) return;
        unique.add(a.href);
        
        // Pega o texto e remove "NOVO" e "POPULAR"
        let title = a.innerText.trim().replace(/NOVO/gi, '').replace(/POPULAR/gi, '').trim().split('\n')[0];
        if (!title) {
            const img = a.querySelector('img');
            if (img) title = img.alt;
        }
        
        // Limpa espaços extras e quebras
        title = title.replace(/\s+/g, ' ').trim();
        const imgEl = a.querySelector('img');
        
        if (title && title.length > 3 && !title.match(/^NOVO$|^POPULAR$/i)) {
          items.push({
            url: a.href,
            title: title,
            image: imgEl ? imgEl.src : null
          });
        }
      });
      return items;
    });

    console.log(`Encontrados ${links.length} eventos. Lendo detalhes...`);

    const eventos = [];
    const hoje = new Date(); hoje.setHours(0,0,0,0);

    for (const item of links) {
      try {
        const detailPage = await browser.newPage();
        await detailPage.goto(item.url, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await detailPage.waitForTimeout(1000);
        
        const bodyText = await detailPage.evaluate(() => document.body.innerText);
        let daysRemaining = null;
        let permanent = false;

        if (bodyText.includes('Permanente') || bodyText.includes('Sempre disponível')) {
          permanent = true;
        } else {
          // Tenta achar a data no formato: "até 14 de Maio de 2026"
          const match = bodyText.match(/até\s+(\d{1,2})\s+de\s+([a-zç]+)\s+de\s+(\d{4})/i);
          if (match) {
            const d = parseInt(match[1]);
            const mName = match[2].toLowerCase();
            const y = parseInt(match[3]);
            const meses = { 'janeiro':0, 'fevereiro':1, 'março':2, 'abril':3, 'maio':4, 'junho':5, 'julho':6, 'agosto':7, 'setembro':8, 'outubro':9, 'novembro':10, 'dezembro':11 };
            if (meses[mName] !== undefined) {
              const endDate = new Date(y, meses[mName], d);
              daysRemaining = Math.ceil((endDate - hoje) / (1000 * 60 * 60 * 24));
              if (daysRemaining < 0) daysRemaining = 0;
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
        await page.waitForTimeout(300);
      } catch (e) {
        eventos.push({ title: item.title, url: item.url, image: item.image, status: 'andamento', daysRemaining: null, permanent: false });
      }
    }

    if (!fs.existsSync('data')) fs.mkdirSync('data');
    fs.writeFileSync('data/eventos-sa.json', JSON.stringify({ source: url, updatedAt: new Date().toISOString(), events: eventos }, null, 2));
    console.log(`✅ Sucesso! ${eventos.length} eventos salvos.`);
    
  } catch (error) {
    console.error('❌ Erro:', error.message);
  } finally {
    await browser.close();
  }
})();
