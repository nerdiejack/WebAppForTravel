# Travel Web Application

A modern web application for travel planning built with Vue.js and Google Maps integration. This application provides an interactive mapping experience for travel planning and exploration.

## Features

- 🗺️ Interactive Google Maps integration
- 🎨 Modern, responsive design with Bootstrap
- 🔄 Dynamic map type switching (Road, Satellite, Terrain)
- 📱 Mobile-friendly interface
- 🎯 Centered map view on Thailand
- 🛡️ Secure configuration with proper CSP headers

## Tech Stack

- **Frontend Framework**: Vue.js 3
- **Build Tool**: Vite
- **Styling**: Bootstrap 5
- **Maps**: Google Maps JavaScript API
- **Container**: Docker
- **Server**: Nginx

## Prerequisites

Before running this application, make sure you have:

- Node.js (v16 or higher)
- Docker and Docker Compose
- A Google Maps API key

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

3. Create a development environment:

```bash
npm run dev
```

4. For production build with Docker:

```bash
docker-compose up --build
```

## Environment Configuration

The application requires the following environment variables:

- `GOOGLE_MAPS_API_KEY`: Your Google Maps API key

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Map.vue         # Main map component
│   ├── App.vue             # Root component
│   ├── main.js             # Application entry point
│   └── style.css           # Global styles
├── nginx.conf              # Nginx configuration
├── Dockerfile              # Frontend container configuration
├── vite.config.js         # Vite configuration
└── package.json           # Dependencies and scripts
```

## Features in Detail

### Google Maps Integration

- Custom layer switcher for different map views
- Responsive map container that adapts to viewport
- Optimized map controls placement
- Smooth transitions between map types

### Responsive Design

- Bootstrap-based grid system
- Mobile-first approach
- Consistent margins and padding
- Optimized for different screen sizes

### Security

- Content Security Policy (CSP) headers
- Secure resource loading
- Protected API endpoints
- CORS configuration

## Development

To start development:

1. Run the development server:

```bash
npm run dev
```

2. Access the application at `http://localhost:4200`

## Building for Production

1. Build the frontend:

```bash
npm run build
```

2. Build and run Docker containers:

```bash
docker-compose up --build
```

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
- Bootstrap team
- Docker community
