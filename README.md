# Travel Journal Web Application

A modern web application for documenting and sharing your travel experiences. This application allows you to create detailed travel diary entries with photos, locations, and descriptions, all visualized on an interactive map.

## Features

- **Interactive Map**: View all your travel locations on a Google Maps interface
- **Travel Diary**: Create and manage detailed diary entries for your travels
  - Rich text descriptions
  - Photo gallery with optimized image display
  - Location tagging
  - Date tracking
- **Hotel Management**: Keep track of your hotel bookings and stays
- **Modern UI/UX**:
  - Responsive design for mobile and desktop
  - Smooth transitions and animations
  - Sticky navigation for better usability
  - Image gallery with consistent sizing
- **Admin Interface**: Manage your travel content through an admin panel

## Technology Stack

- **Frontend**:

  - Vue.js 3
  - Google Maps API
  - Font Awesome icons
  - Modern CSS with CSS Variables
  - Responsive design principles

- **Backend**:

  - Python FastAPI
  - SQLAlchemy ORM
  - PostgreSQL database

- **Development & Deployment**:
  - Docker & Docker Compose
  - Environment variable configuration
  - Development tools integration

## Setup & Installation

1. **Clone the repository**

   ```bash
   git clone [repository-url]
   cd WebAppForTravel
   ```

2. **Environment Setup**

   - Create a `.env` file in the frontend directory:
     ```
     VUE_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
     VUE_APP_API_URL=http://localhost:8000
     ```
   - Create a `.env` file in the root directory for backend configuration

3. **Start the Application**

   ```bash
   docker-compose up -d
   ```

4. **Access the Application**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Development

### Frontend Development

- Located in the `frontend` directory
- Built with Vue.js 3 and modern web technologies
- Uses Vue Router for navigation
- Implements responsive design principles

### Backend Development

- Located in the `backend` directory
- FastAPI framework for high-performance API
- SQLAlchemy for database operations
- RESTful API design

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Maps API for location services
- Vue.js team for the excellent framework
- FastAPI team for the backend framework
- All contributors who have helped shape this project
