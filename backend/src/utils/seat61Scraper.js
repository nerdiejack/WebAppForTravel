const puppeteer = require('puppeteer');

async function scrapeSeat61() {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();
    
    // Navigate to the main page
    await page.goto('https://www.seat61.com/train-routes.htm', {
      waitUntil: 'networkidle0',
      timeout: 30000
    });

    // Extract route information
    const routes = await page.evaluate(() => {
      const routeElements = document.querySelectorAll('.route-card, .route-item');
      return Array.from(routeElements).map(element => {
        const name = element.querySelector('h2, h3')?.textContent.trim() || '';
        const description = element.querySelector('.description, p')?.textContent.trim() || '';
        const duration = element.querySelector('.duration')?.textContent.trim() || '';
        const frequency = element.querySelector('.frequency')?.textContent.trim() || '';
        const price = element.querySelector('.price')?.textContent.trim() || '';
        
        // Extract route points if available
        const routePoints = Array.from(element.querySelectorAll('.route-point')).map(point => ({
          name: point.textContent.trim(),
          coordinates: point.dataset.coordinates ? JSON.parse(point.dataset.coordinates) : null
        }));

        // Extract facilities
        const facilities = Array.from(element.querySelectorAll('.facility')).map(f => f.textContent.trim());

        // Extract tips
        const tips = Array.from(element.querySelectorAll('.tip')).map(t => t.textContent.trim());

        return {
          name,
          description,
          duration,
          frequency,
          price,
          route: routePoints,
          facilities,
          tips,
          lastUpdated: new Date().toISOString()
        };
      });
    });

    return routes;
  } catch (error) {
    console.error('Error scraping Seat61:', error);
    throw error;
  } finally {
    await browser.close();
  }
}

module.exports = {
  scrapeSeat61
}; 