# Travel Diary Web Application

A modern web application for documenting your travel experiences with an interactive map interface. This application allows users to create, view, and manage travel diary entries with location-based features and image support.

## Features

### Core Functionality

- **Interactive Map Interface**

  - Google Maps integration for visual location tracking
  - Custom markers for each diary entry
  - Info windows with entry previews
  - "View All Locations" feature to see all entries on the map
  - Location picking functionality for new entries

- **Diary Entry Management**

  - Create new travel diary entries
  - Edit existing entries
  - View detailed entry information
  - Delete entries
  - Rich text content support

- **Location Features**

  - Automatic location detection
  - Manual location selection via map
  - City and country flag display
  - Geocoding support for location names

- **Image Management**
  - Multiple image upload support
  - Image preview functionality
  - Automatic image compression for large files
  - Support for JPEG, PNG, and GIF formats
  - Maximum file size limit of 25MB

### User Interface

- **Modern Design**

  - Clean and intuitive layout
  - Responsive design for all screen sizes
  - Smooth transitions and animations
  - Bootstrap-based components

- **Navigation**

  - Top navigation bar with options menu
  - Dropdown menu for quick actions
  - Modal-based entry editor
  - Easy access to map controls

- **Diary Cards**
  - Compact and informative design
  - Preview image support
  - Location and date information
  - Country flag indicators
  - Hover effects for better interaction

## Technical Stack

### Frontend

- **Framework**: Vue.js 3
- **UI Library**: Bootstrap 5
- **Maps**: Google Maps JavaScript API
- **HTTP Client**: Axios
- **Styling**: CSS3 with SCSS support

### Backend

- **Runtime**: Node.js
- **Framework**: Express.js
- **Database**: MongoDB
- **File Storage**: Local storage (configurable for cloud storage)

## Environment Setup

### Required Environment Variables

```env
# Frontend
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
VITE_API_BASE_URL=http://localhost:3000

# Backend
PORT=3000
MONGODB_URI=your_mongodb_connection_string
```

### Installation

1. Clone the repository:

```bash
git clone [repository-url]
cd travel-diary-app
```

2. Install dependencies:

```bash
# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
npm install
```

3. Set up environment variables:

```bash
# Frontend
cp frontend/.env.example frontend/.env

# Backend
cp backend/.env.example backend/.env
```

4. Start the development servers:

```bash
# Start backend server
cd backend
npm run dev

# Start frontend server (in a new terminal)
cd frontend
npm run dev
```

## API Endpoints

### Diary Entries

- `GET /api/diary/entries` - Get all diary entries
- `POST /api/diary/entries` - Create a new diary entry
- `PUT /api/diary/entries/:id` - Update an existing entry
- `DELETE /api/diary/entries/:id` - Delete an entry

### Image Upload

- `POST /api/diary/upload-image` - Upload images for diary entries

## Project Structure

```
travel-diary-app/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── TravelDiary.vue
│   │   │   └── DiaryEntryDisplay.vue
│   │   ├── utils/
│   │   │   ├── axios.js
│   │   │   └── mapLoader.js
│   │   └── App.vue
│   └── package.json
├── backend/
│   ├── src/
│   │   ├── routes/
│   │   ├── models/
│   │   └── controllers/
│   └── package.json
└── README.md
```

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
- Bootstrap team for the UI components
- Vue.js team for the frontend framework
- MongoDB team for the database solution
