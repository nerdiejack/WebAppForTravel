# Travel Web Application

A comprehensive travel planning and hotel reservation system built with Vue.js, FastAPI, and MongoDB. This full-stack application provides an interactive mapping experience for travel planning, hotel bookings, and administrative management.

## Features

### Core Functionality

- **Hotel Reservation System**

  - Complete CRUD operations for hotel bookings
  - Real-time search and filtering
  - Date-based availability management
  - Status tracking (confirmed, cancelled, completed)
  - Special requests handling
  - Price calculation and management

- **Travel Planning System**

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

- **Travel Diary System**

  - Interactive map interface for entry locations
  - Create, edit, and manage travel diary entries
  - Multiple image upload support
  - Location-based entry organization
  - Country flag indicators
  - Rich text content support
  - Preview images for entries

- **Admin Dashboard**
  - Comprehensive reservation management
  - Quick search and filtering
  - Bulk operations support
  - Status updates
  - Detailed booking information
  - Responsive table view
  - Hotel coordinate management
  - Map location verification

### User Interface

- **Modern Design**

  - Clean and intuitive layout
  - Responsive design for all screen sizes
  - Smooth transitions and animations
  - Bootstrap-based components
  - Dynamic map type switching (Road, Satellite, Terrain)

- **Navigation**

  - Top navigation bar with options menu
  - Dropdown menu for quick actions
  - Modal-based forms and editors
  - Easy access to map controls
  - Intuitive booking flow

- **Interactive Maps**
  - Google Maps integration
  - Custom markers for hotels and diary entries
  - Info windows with previews
  - Location picking functionality
  - Route visualization
  - Real-time traffic updates
  - Multi-layer support

## Technical Stack

### Frontend

- **Framework**: Vue.js 3
- **Build Tool**: Vite
- **UI Library**: Bootstrap 5
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

## Environment Setup

### Required Environment Variables

```env
# Frontend
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
VITE_SKYSCANNER_API_KEY=your_skyscanner_api_key
VITE_API_BASE_URL=http://localhost:3000

# Backend
MONGODB_URL=your_mongodb_url
```

### Installation

1. Clone the repository:

```bash
git clone [repository-url]
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

## API Endpoints

### Hotels

- `GET /api/hotels` - List all reservations
- `GET /api/hotels/{city}` - Get hotels by city
- `POST /api/hotels` - Create reservation
- `PUT /api/hotels/{id}` - Update reservation
- `DELETE /api/hotels/{id}` - Delete reservation

### Travel Planning

- `GET /api/routes` - Get route information
- `POST /api/routes/calculate` - Calculate route between points
- `GET /api/flights` - Search for flights
- `GET /api/transit` - Get public transit options

### Diary Entries

- `GET /api/diary/entries` - Get all diary entries
- `POST /api/diary/entries` - Create a new diary entry
- `PUT /api/diary/entries/:id` - Update an existing entry
- `DELETE /api/diary/entries/:id` - Delete an entry
- `POST /api/diary/upload-image` - Upload images for diary entries

## Project Structure

```
WebAppForTravel/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Map.vue              # Map component
│   │   │   ├── HotelMap.vue         # Hotel reservation map
│   │   │   ├── TravelDiary.vue      # Diary component
│   │   │   ├── DiaryEntryDisplay.vue # Diary entry display
│   │   │   └── AdminDashboard.vue   # Admin interface
│   │   ├── utils/
│   │   │   ├── axios.js             # API client configuration
│   │   │   └── mapLoader.js         # Google Maps loader
│   │   ├── App.vue                  # Root component
│   │   └── main.js                  # Application entry
│   ├── nginx.conf                   # Nginx configuration
│   └── Dockerfile                   # Frontend container
├── backend/
│   ├── routes/
│   │   ├── hotels.py                # Hotel endpoints
│   │   ├── maps.py                  # Map endpoints
│   │   └── diary.py                 # Diary endpoints
│   ├── models.py                    # Data models
│   ├── database.py                  # Database configuration
│   ├── main.py                      # FastAPI application
│   └── requirements.txt             # Python dependencies
└── docker-compose.yml               # Container orchestration
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
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Maps Platform for the mapping functionality
- Skyscanner for flight search capabilities
- Bootstrap team for the UI components
- Vue.js team for the frontend framework
- FastAPI team for the backend framework
- MongoDB team for the database solution
- Docker community for containerization support
