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

    const eventos = await page.evaluate(() => {
      const items = [];
      const links = document.querySelectorAll('a[href*="Notice/Detail"]');
      
      links.forEach(link => {
        let title = link.innerText.trim().split('\n')[0]; 
        if (!title) {
            const img = link.querySelector('img');
            if (img) title = img.alt;
        }
        
        const imgEl = link.querySelector('img');
        
        if (title && title.length > 3) {
          items.push({
            title: title,
            url: link.href,
            image: imgEl ? imgEl.src : null,
            status: 'andamento', 
            daysRemaining: null, 
            permanent: false
          });
        }
      });
      return items;
    });

    const data = {
      source: url,
      updatedAt: new Date().toISOString(),
      events: eventos
    };

    if (!fs.existsSync('data')) fs.mkdirSync('data');
    
    fs.writeFileSync('data/eventos-sa.json', JSON.stringify(data, null, 2));
    console.log(`✅ Sucesso! ${eventos.length} eventos salvos.`);
    
  } catch (error) {
    console.error('❌ Erro ao raspar:', error.message);
  } finally {
    await browser.close();
  }
})();
