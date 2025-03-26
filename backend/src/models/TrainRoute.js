const mongoose = require('mongoose');

const routePointSchema = new mongoose.Schema({
  name: String,
  coordinates: {
    lat: Number,
    lng: Number
  }
});

const trainRouteSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    unique: true
  },
  description: String,
  duration: String,
  frequency: String,
  price: String,
  route: [routePointSchema],
  facilities: [String],
  tips: [String],
  lastUpdated: {
    type: Date,
    default: Date.now
  }
});

// Add text index for search functionality
trainRouteSchema.index({ name: 'text', description: 'text' });

module.exports = mongoose.model('TrainRoute', trainRouteSchema); 