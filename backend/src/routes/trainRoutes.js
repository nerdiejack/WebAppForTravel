const express = require('express');
const router = express.Router();
const TrainRoute = require('../models/TrainRoute');
const { scrapeSeat61 } = require('../utils/seat61Scraper');

// Get all train routes
router.get('/', async (req, res) => {
  try {
    const { search, minPrice, maxPrice, maxDuration } = req.query;
    let query = {};

    // Apply search filter
    if (search) {
      query.$text = { $search: search };
    }

    // Apply price filter
    if (minPrice || maxPrice) {
      query.price = {};
      if (minPrice) query.price.$gte = minPrice;
      if (maxPrice) query.price.$lte = maxPrice;
    }

    // Apply duration filter
    if (maxDuration) {
      query.duration = { $lte: maxDuration };
    }

    const routes = await TrainRoute.find(query);
    res.json(routes);
  } catch (error) {
    console.error('Error fetching train routes:', error);
    res.status(500).json({ error: 'Failed to fetch train routes' });
  }
});

// Get a specific train route
router.get('/:id', async (req, res) => {
  try {
    const route = await TrainRoute.findById(req.params.id);
    if (!route) {
      return res.status(404).json({ error: 'Train route not found' });
    }
    res.json(route);
  } catch (error) {
    console.error('Error fetching train route:', error);
    res.status(500).json({ error: 'Failed to fetch train route' });
  }
});

// Scrape and update train routes
router.post('/scrape', async (req, res) => {
  try {
    const scrapedRoutes = await scrapeSeat61();
    
    // Update or insert each route
    for (const route of scrapedRoutes) {
      await TrainRoute.findOneAndUpdate(
        { name: route.name },
        route,
        { upsert: true, new: true }
      );
    }

    res.json({ message: 'Train routes updated successfully' });
  } catch (error) {
    console.error('Error updating train routes:', error);
    res.status(500).json({ error: 'Failed to update train routes' });
  }
});

module.exports = router; 