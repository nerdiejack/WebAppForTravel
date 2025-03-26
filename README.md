# Travel Web Application

A comprehensive travel planning and hotel reservation system built with Vue.js, FastAPI, and MongoDB. This full-stack application provides an interactive mapping experience for travel planning, hotel bookings, and administrative management.

## Features

- 🏨 Complete hotel reservation system
- 🗺️ Interactive Google Maps integration
- 📊 Admin dashboard for managing reservations
  - Detailed booking information view
  - Edit hotel coordinates (latitude/longitude)
  - Quick access to map location
  - Status management (confirmed, cancelled, completed)
- 🚂 Travel planning and route search
  - Multi-modal transport options (flights, trains, buses)
  - Real-time route information using Google Maps
  - Interactive route visualization
  - Price comparison
  - Flight search via Skyscanner
  - Driving and transit directions
- 🎨 Modern, responsive design with Bootstrap
- 🔄 Dynamic map type switching (Road, Satellite, Terrain)
- 📱 Mobile-friendly interface
- 🎯 Centered map view on Thailand
- 🛡️ Secure configuration with proper CSP headers
- 🔍 Search and filter reservations
- 📅 Date-based booking management
- 🌤️ Real-time weather information for hotel locations

## Tech Stack

### Frontend

- **Framework**: Vue.js 3
- **Build Tool**: Vite
- **Styling**: Bootstrap 5
- **Maps**: Google Maps JavaScript API
  - Maps
  - Places
  - Distance Matrix
  - Directions
- **Travel APIs**:
  - Skyscanner API (for flights)
  - Google Maps Distance Matrix (for driving and transit)
- **HTTP Client**: Axios
- **Server**: Nginx

### Backend

- **Framework**: FastAPI
- **Database**: MongoDB
- **Async Driver**: Motor
- **Data Validation**: Pydantic
- **Container**: Docker

## Prerequisites

Before running this application, make sure you have:

- Node.js (v16 or higher)
- Python 3.8 or higher
- Docker and Docker Compose
- MongoDB
- A Google Maps API key with the following APIs enabled:
  - Maps JavaScript API
  - Places API
  - Distance Matrix API
  - Directions API
- A Skyscanner API key (for flight search)

## Setup and Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd WebAppForTravel
```

2. Install frontend dependencies:

```bash
cd frontend
npm install
```

3. Install backend dependencies:

```bash
cd backend
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
# Frontend (.env)
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
VITE_SKYSCANNER_API_KEY=your_skyscanner_api_key

# Backend (.env)
MONGODB_URL=your_mongodb_url
```

5. For development:

```bash
# Frontend
npm run dev

# Backend
uvicorn main:app --reload
```

6. For production with Docker:

```bash
docker-compose up --build
```

## Project Structure

```
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Map.vue              # Map component
│   │   │   ├── HotelMap.vue         # Hotel reservation map
│   │   │   └── AdminDashboard.vue   # Admin interface
│   │   ├── utils/
│   │   │   └── axios.js             # API client configuration
│   │   ├── App.vue                  # Root component
│   │   └── main.js                  # Application entry
│   ├── nginx.conf                   # Nginx configuration
│   └── Dockerfile                   # Frontend container
│
├── backend/
│   ├── routes/
│   │   ├── hotels.py                # Hotel endpoints
│   │   └── maps.py                  # Map endpoints
│   ├── models.py                    # Data models
│   ├── database.py                  # Database configuration
│   ├── main.py                      # FastAPI application
│   └── requirements.txt             # Python dependencies
│
└── docker-compose.yml               # Container orchestration
```

## Features in Detail

### Hotel Reservation System

- Complete CRUD operations for hotel bookings
- Real-time search and filtering
- Date-based availability management
- Status tracking (confirmed, cancelled, completed)
- Special requests handling
- Price calculation

### Admin Dashboard

- Comprehensive reservation management
- Quick search and filtering
- Bulk operations support
- Status updates
- Detailed booking information
- Responsive table view

### Google Maps Integration

- Custom layer switcher
- Hotel location plotting
- Interactive booking interface
- Responsive map container
- Optimized controls placement

### Travel Planning System

- Multi-modal transport search
  - Driving directions with real-time traffic
  - Public transit routes
  - Flight options via Skyscanner
- Real-time route information
  - Duration and distance
  - Price estimates
  - Traffic conditions
- Interactive route visualization
  - Detailed turn-by-turn directions
  - Route alternatives
  - Waypoints support
- Price comparison across different transport modes
- Location autocomplete
- Current location detection
- Booking integration with transport providers
- Detailed journey information including:
  - Duration and distance
  - Departure and arrival times
  - Number of stops
  - Price breakdown
  - Transport type

### API Endpoints

#### Hotels

- `GET /api/hotels` - List all reservations
- `GET /api/hotels/{city}` - Get hotels by city
- `POST /api/hotels` - Create reservation
- `PUT /api/hotels/{id}` - Update reservation
- `DELETE /api/hotels/{id}` - Delete reservation

## Development

### Frontend Development

```bash
cd frontend
npm run dev
```

### Backend Development

```bash
cd backend
uvicorn main:app --reload
```

### Working with Docker

```bash
# Build and start all services
docker-compose up --build

# Stop all services
docker-compose down

# View logs
docker-compose logs -f
```

## Security

- Content Security Policy (CSP) headers
- CORS configuration
- MongoDB security best practices
- Input validation
- Error handling
- API rate limiting

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Maps JavaScript API
- Vue.js team
- FastAPI team
- Bootstrap team
- MongoDB team
- Docker community
