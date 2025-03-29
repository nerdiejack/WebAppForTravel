<template>
  <div class="travel-diary-container">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom">
      <div class="container-fluid">
        <span class="navbar-brand">Travel Diary</span>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarContent">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <div class="dropdown">
                <button class="nav-link dropdown-toggle" @click="toggleDropdown">
                  <i class="fas fa-cog"></i> Options
                </button>
                <div v-if="isDropdownOpen" class="dropdown-menu dropdown-menu-end show">
                  <a class="dropdown-item" href="#" @click.prevent="openEditor">
                    <i class="fas fa-plus me-2"></i>New Entry
                  </a>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="main-content">
      <div class="map-wrapper">
        <div class="map-container" ref="mapContainer">
          <!-- Loading overlay -->
          <div v-if="loading" class="map-overlay">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>

          <!-- Error overlay -->
          <div v-if="error" class="map-overlay error">
            <div class="alert alert-danger" role="alert">
              {{ error }}
              <button @click="retryLoading" class="btn btn-outline-danger btn-sm ms-2">
                Retry
              </button>
            </div>
          </div>

          <div ref="mapElement" style="width: 100%; height: 100%;"></div>
          <button v-if="!loading && !error" @click="viewAllLocations" class="view-all-btn">
            <i class="fas fa-globe-americas me-2"></i>View All Locations
          </button>
        </div>
        <diary-entry-display
          v-if="selectedEntry"
          :entry="selectedEntry"
          @back-to-map="closeSelectedEntry"
          @edit="editEntry"
          style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 2; background: white;"
        />
      </div>

      <div class="diary-list">
        <div v-if="loading" class="text-center py-4">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>

        <div v-else-if="error" class="alert alert-danger" role="alert">
          {{ error }}
          <button @click="retryLoading" class="btn btn-outline-danger btn-sm ms-2">
            Retry
          </button>
        </div>

        <div v-else-if="entries.length === 0" class="text-center py-4 text-muted">
          <i class="fas fa-book-open fa-3x mb-3"></i>
          <p>No diary entries yet. Start documenting your journey!</p>
        </div>

        <div v-else class="diary-entries">
          <div v-for="entry in entries" 
               :key="entry._id" 
               class="diary-card" 
               @click="handleDiaryEntryClick(entry)">
            <div class="diary-card-content">
              <div class="diary-card-left">
                <div v-if="entry.images.length > 0" class="preview-image">
                  <img :src="entry.images[0]" :alt="entry.title">
                </div>
                <div v-else class="preview-image no-image">
                  <i class="fas fa-image"></i>
                </div>
              </div>
              <div class="diary-card-middle">
                <h5>{{ entry.title }}</h5>
                <div class="text-muted">
                  <small>
                    <i class="fas fa-map-marker-alt me-1"></i>{{ entry.location.name }}
                    <span class="ms-2"><i class="fas fa-calendar me-1"></i>{{ formatDate(entry.created_at) }}</span>
                  </small>
                </div>
              </div>
              <div class="diary-card-right">
                <span class="country-flag">{{ getCountryFlag(entry.location.name) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Editor Modal -->
    <div class="modal fade" id="editorModal" tabindex="-1" ref="editorModal" aria-labelledby="editorModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-fullscreen">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editorModalLabel">{{ isEditing ? 'Edit Entry' : 'New Entry' }}</h5>
            <button type="button" class="btn-close" @click="closeEditor" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="editor-container">
              <div class="editor-main">
                <div class="form-group mb-4">
                  <input 
                    v-model="newEntry.title" 
                    class="form-control form-control-lg" 
                    placeholder="Enter your title..."
                    required
                  >
                </div>
                <div class="form-group mb-4">
                  <textarea 
                    v-model="newEntry.content" 
                    class="form-control" 
                    placeholder="Write your story..."
                    rows="12"
                    required
                  ></textarea>
                </div>
              </div>
              <div class="editor-sidebar">
                <div class="sidebar-section">
                  <h6><i class="fas fa-map-marker-alt me-2"></i>Location</h6>
                  <input 
                    v-model="newEntry.location.name" 
                    class="form-control mb-2" 
                    placeholder="Location name"
                    required
                  >
                  <div class="coordinates-inputs">
                    <input 
                      v-model.number="newEntry.location.lat" 
                      type="number" 
                      class="form-control" 
                      placeholder="Latitude"
                      step="any"
                      required
                    >
                    <input 
                      v-model.number="newEntry.location.lng" 
                      type="number" 
                      class="form-control" 
                      placeholder="Longitude"
                      step="any"
                      required
                    >
                  </div>
                  <button type="button" @click="pickLocationOnMap" class="btn btn-outline-primary w-100 mt-2">
                    <i class="fas fa-map-pin me-2"></i>Pick on Map
                  </button>
                </div>
                <div class="sidebar-section">
                  <h6><i class="fas fa-images me-2"></i>Images</h6>
                  <input 
                    type="file" 
                    @change="handleImageUpload" 
                    accept="image/*" 
                    multiple 
                    class="form-control mb-3"
                  >
                  <div class="image-preview-grid">
                    <div v-for="(image, index) in newEntry.images" 
                         :key="index" 
                         class="image-preview-item">
                      <img :src="image" :alt="'Preview ' + (index + 1)">
                      <button type="button" 
                              class="btn btn-danger btn-sm remove-image" 
                              @click="removeImage(index)">
                        <i class="fas fa-times"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeEditor">Cancel</button>
            <button type="button" class="btn btn-primary" @click="saveDiaryEntry">
              {{ isEditing ? 'Update Entry' : 'Save Entry' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, nextTick, reactive } from 'vue'
import api from '../utils/axios'
import { loadGoogleMaps, cleanupGoogleMaps } from '../utils/mapLoader'
import { Collapse, Modal, Dropdown } from 'bootstrap'
import DiaryEntryDisplay from './DiaryEntryDisplay.vue'

export default {
  name: 'TravelDiary',
  components: {
    DiaryEntryDisplay
  },
  setup() {
    const mapContainer = ref(null)
    const mapElement = ref(null)
    const entries = ref([])
    const map = ref(null)
    const markers = ref([])
    const isPickingLocation = ref(false)
    const selectedEntry = ref(null)
    const activeInfoWindow = ref(null)
    const loading = ref(false)
    const error = ref(null)
    const geocoder = ref(null)
    const google = ref(null)
    const isDropdownOpen = ref(false)

    let mapInitialized = false

    const newEntry = ref({
      title: '',
      content: '',
      location: {
        name: '',
        lat: null,
        lng: null
      },
      images: []
    })

    const editorModal = ref(null)
    const viewEntryModal = ref(null)
    const isEditing = ref(false)

    const initMap = async () => {
      try {
        if (!mapContainer.value || !mapElement.value) {
          console.error('Map container or element ref is null');
          throw new Error('Map container not found');
        }

        loading.value = true;
        error.value = null;

        // Load Google Maps API first
        google.value = await loadGoogleMaps();
        
        // Create the map instance directly on the mapElement
        map.value = new google.value.maps.Map(mapElement.value, {
          center: { lat: 13.7563, lng: 100.5018 },
          zoom: 6,
          mapTypeControl: true,
          streetViewControl: true,
          fullscreenControl: true,
          zoomControl: true,
          gestureHandling: 'greedy'
        });

        // Wait for the map to be fully loaded
        await new Promise((resolve) => {
          google.value.maps.event.addListenerOnce(map.value, 'idle', () => {
            console.log('Map fully loaded');
            resolve();
          });
        });

        geocoder.value = new google.value.maps.Geocoder();
        console.log('Map initialized successfully');
        mapInitialized = true;

        // Create markers for existing entries
        await displayEntriesOnMap();

      } catch (err) {
        console.error('Error initializing map:', err);
        error.value = 'Failed to initialize map. Please try again.';
        mapInitialized = false;
      } finally {
        loading.value = false;
      }
    };

    const loadEntries = async () => {
      try {
        loading.value = true
        error.value = null
        
        const response = await api.get('/api/diary/entries')
        entries.value = response.data
        await displayEntriesOnMap()
      } catch (error) {
        console.error('Error loading diary entries:', error)
        error.value = 'Failed to load diary entries. Please try again later.'
        entries.value = []
      } finally {
        loading.value = false
      }
    }

    const displayEntriesOnMap = async () => {
      console.log('displayEntriesOnMap called');
      if (!map.value || !google.value) {
        console.error('Map not initialized yet - map:', !!map.value, 'google:', !!google.value);
        return;
      }

      try {
        console.log('Clearing existing markers');
        // Clear existing markers
        markers.value.forEach(marker => marker.setMap(null));
        markers.value = [];

        if (!entries.value || entries.value.length === 0) {
          console.log('No entries to display');
          return;
        }

        console.log('Creating bounds and markers for', entries.value.length, 'entries');
        const bounds = new google.value.maps.LatLngBounds();
        
        for (const entry of entries.value) {
          const position = {
            lat: entry.location.lat,
            lng: entry.location.lng
          };

          bounds.extend(position);
          const marker = await createMarker(entry, position);
          if (marker) {
            markers.value.push(marker);
          }
        }

        console.log('Fitting bounds to map with', markers.value.length, 'markers');
        map.value.fitBounds(bounds);
        if (markers.value.length === 1) {
          map.value.setZoom(15);
        }
      } catch (error) {
        console.error('Error displaying entries on map:', error);
        error.value = 'Failed to display entries on map. Please try again later.';
      }
    }

    const createMarker = async (entry, position) => {
      if (!map.value || !google.value) return null;

      try {
        const marker = new google.value.maps.Marker({
          map: map.value,
          position,
          title: entry.title,
          animation: google.value.maps.Animation.DROP
        });

        // Create info window with enhanced content
        const infoWindow = new google.value.maps.InfoWindow({
          content: `
            <div class="info-window" style="padding: 10px; max-width: 300px;">
              <h5 style="margin: 0 0 8px 0; color: #007bff;">${entry.title}</h5>
              <div style="color: #666; margin-bottom: 8px;">
                <i class="fas fa-map-marker-alt"></i> ${entry.location.name}
              </div>
              ${entry.images.length > 0 ? 
                `<img src="${entry.images[0]}" alt="Location" style="width: 100%; height: 150px; object-fit: cover; border-radius: 4px; margin-bottom: 8px;">` 
                : ''}
              <div style="font-size: 0.9em; color: #333;">
                ${entry.content.substring(0, 100)}${entry.content.length > 100 ? '...' : ''}
              </div>
            </div>
          `
        });

        // Add click listener
        marker.addListener('click', () => {
          // Close any open info window
          if (activeInfoWindow.value) {
            activeInfoWindow.value.close();
          }
          
          // Open this info window
          infoWindow.open(map.value, marker);
          activeInfoWindow.value = infoWindow;
          
          // Update selected entry
          selectedEntry.value = entry;
        });

        return marker;
      } catch (err) {
        console.error('Error creating marker:', err);
        return null;
      }
    };

    const addDiaryEntry = async () => {
      try {
        const response = await api.post('/api/diary/entries', newEntry.value)
        if (response.data) {
          entries.value.push(response.data)
          await displayEntriesOnMap()
          alert('Diary entry added successfully!')

          // Reset form
          newEntry.value = {
            title: '',
            content: '',
            location: {
              name: '',
              lat: null,
              lng: null
            },
            images: []
          }
        }
      } catch (error) {
        console.error('Error adding diary entry:', error)
        alert('Failed to add diary entry. Please check the console for details.')
      }
    }

    const handleImageUpload = async (event) => {
      const files = event.target.files;
      if (!files || files.length === 0) return;

      const maxFileSize = 25 * 1024 * 1024; // 25MB limit
      const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];

      try {
        for (let i = 0; i < files.length; i++) {
          const file = files[i];
          
          // Validate file size
          if (file.size > maxFileSize) {
            throw new Error(`File "${file.name}" is too large. Maximum size is 25MB.`);
          }

          // Validate file type
          if (!allowedTypes.includes(file.type)) {
            throw new Error(`File "${file.name}" is not a supported image type. Please use JPEG, PNG, or GIF.`);
          }

          // Compress image before upload if it's larger than 5MB
          let fileToUpload = file;
          if (file.size > 5 * 1024 * 1024) {
            fileToUpload = await compressImage(file);
          }

          const formData = new FormData();
          formData.append('file', fileToUpload);

          const response = await api.post('/api/diary/upload-image', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            },
            // Add timeout and max content length configs
            timeout: 30000, // 30 seconds timeout
            maxContentLength: maxFileSize,
            maxBodyLength: maxFileSize
          });

          if (response.data.url) {
            newEntry.value.images.push(response.data.url);
          }
        }
      } catch (error) {
        console.error('Error uploading images:', error);
        alert(error.message || 'Failed to upload images. Please try again.');
      }
    };

    const compressImage = async (file) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = (event) => {
          const img = new Image();
          img.src = event.target.result;
          img.onload = () => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            // Calculate new dimensions while maintaining aspect ratio
            let width = img.width;
            let height = img.height;
            const maxDimension = 1920; // Max width or height

            if (width > height && width > maxDimension) {
              height = (height * maxDimension) / width;
              width = maxDimension;
            } else if (height > maxDimension) {
              width = (width * maxDimension) / height;
              height = maxDimension;
            }

            canvas.width = width;
            canvas.height = height;
            ctx.drawImage(img, 0, 0, width, height);

            canvas.toBlob(
              (blob) => {
                resolve(new File([blob], file.name, {
                  type: 'image/jpeg',
                  lastModified: Date.now()
                }));
              },
              'image/jpeg',
              0.8 // compression quality
            );
          };
          img.onerror = reject;
        };
        reader.onerror = reject;
      });
    };

    const removeImage = (index) => {
      newEntry.value.images.splice(index, 1)
    }

    const pickLocationOnMap = () => {
      if (!map.value || !google.value) {
        console.warn('Map not initialized yet')
        return
      }

      isPickingLocation.value = true
      alert('Click on the map to set the location')

      const clickListener = map.value.addListener('click', (event) => {
        newEntry.value.location.lat = event.latLng.lat()
        newEntry.value.location.lng = event.latLng.lng()
        isPickingLocation.value = false
        google.value.maps.event.removeListener(clickListener)
        alert('Location set!')
      })
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString()
    }

    const retryLoading = async () => {
      await loadEntries()
    }

    const cleanup = () => {
      console.log('Running cleanup');
      if (markers.value) {
        markers.value.forEach(marker => {
          if (marker) marker.setMap(null);
        });
        markers.value = [];
      }

      if (activeInfoWindow.value) {
        activeInfoWindow.value.close();
        activeInfoWindow.value = null;
      }

      if (map.value) {
        google.value?.maps.event.clearInstanceListeners(map.value);
      }

      mapInitialized = false;
    }

    const viewAllLocations = async () => {
      console.log('viewAllLocations called');
      console.log('map value:', map.value);
      console.log('markers length:', markers.value?.length);
      console.log('mapInitialized:', mapInitialized);

      if (!map.value || !markers.value.length) {
        console.log('Map or markers not ready, initializing map...');
        if (!mapInitialized) {
          await initMap();
        }
      }

      if (!map.value || !markers.value.length) {
        console.log('Still no map or markers, returning');
        return;
      }

      console.log('Creating bounds and fitting map');
      const bounds = new google.value.maps.LatLngBounds();
      markers.value.forEach(marker => {
        bounds.extend(marker.getPosition());
      });

      map.value.fitBounds(bounds);
      // Add some padding to the bounds
      map.value.setZoom(map.value.getZoom() - 0.5);
    }

    const handleDiaryEntryClick = async (entry) => {
      console.log('Opening diary entry:', entry.title);
      
      try {
        // Cleanup map resources before showing entry
        if (map.value) {
          // Clear all markers
          if (markers.value) {
            markers.value.forEach(marker => {
              if (marker) {
                google.value.maps.event.clearInstanceListeners(marker);
                marker.setMap(null);
              }
            });
            markers.value = [];
          }

          // Clear map listeners
          google.value?.maps.event.clearInstanceListeners(map.value);
          
          // Close any open info windows
          if (activeInfoWindow.value) {
            activeInfoWindow.value.close();
            activeInfoWindow.value = null;
          }

          // Hide map container to free up resources
          if (mapContainer.value) {
            mapContainer.value.style.visibility = 'hidden';
          }
        }

        // Set selected entry after cleanup
        selectedEntry.value = entry;

      } catch (error) {
        console.error('Error in handleDiaryEntryClick:', error);
      }
    }

    const closeSelectedEntry = async () => {
      console.log('Closing selected entry');
      selectedEntry.value = null;
      
      try {
        // Wait for the view to update
        await nextTick();
        
        // Check if map container exists
        if (!mapContainer.value || !mapElement.value) {
          console.error('Map container or element not found');
          return;
        }

        // Make map container visible again
        if (mapContainer.value) {
          mapContainer.value.style.visibility = 'visible';
        }

        // If map is not initialized or was cleaned up, initialize it
        if (!mapInitialized || !map.value) {
          console.log('Map not initialized, calling initMap');
          await initMap();
        } else {
          console.log('Map exists, restoring view');
          
          // Force a resize event to ensure map renders correctly
          if (map.value && google.value) {
            google.value.maps.event.trigger(map.value, 'resize');
          }

          // Display all entries on map
          await displayEntriesOnMap();
        }

      } catch (error) {
        console.error('Error in closeSelectedEntry:', error);
      }
    }

    const closeEntry = (index) => {
      const collapseElement = document.getElementById('collapse' + index);
      const collapse = Collapse.getInstance(collapseElement);
      if (collapse) {
        collapse.hide();
      }
    }

    const openEditor = () => {
      isEditing.value = false
      newEntry.value = {
        title: '',
        content: '',
        location: {
          name: '',
          lat: null,
          lng: null
        },
        images: []
      }
      new Modal(editorModal.value).show()
    }

    const closeEditor = () => {
      const modalInstance = Modal.getInstance(editorModal.value);
      if (modalInstance) {
        modalInstance.hide();
      } else {
        new Modal(editorModal.value).hide();
      }
      // Reset form after modal is hidden
      editorModal.value.addEventListener('hidden.bs.modal', () => {
        newEntry.value = {
          title: '',
          content: '',
          location: {
            name: '',
            lat: null,
            lng: null
          },
          images: []
        };
      }, { once: true });
    }

    const viewEntry = (entry) => {
      selectedEntry.value = entry
      new Modal(viewEntryModal.value).show()
      
      // Center map on entry location
      nextTick(() => {
        if (map.value && entry.location.lat && entry.location.lng) {
          map.value.setCenter({
            lat: entry.location.lat,
            lng: entry.location.lng
          })
          map.value.setZoom(15)

          // Find and trigger the marker's click event
          const marker = markers.value.find(m => 
            m.getPosition().lat() === entry.location.lat && 
            m.getPosition().lng() === entry.location.lng
          )
          if (marker) {
            google.value.maps.event.trigger(marker, 'click')
          }
        }
      })
    }

    const editEntry = (entry) => {
      // Set up the entry for editing
      newEntry.value = {
        ...entry,
        location: { ...entry.location }
      };
      isEditing.value = true;
      
      // Show the editor modal
      const modal = new Modal(editorModal.value);
      modal.show();
    }

    const saveDiaryEntry = async () => {
      try {
        let response
        if (isEditing.value) {
          response = await api.put(`/api/diary/entries/${newEntry.value._id}`, newEntry.value)
          const index = entries.value.findIndex(e => e._id === newEntry.value._id)
          if (index !== -1) {
            entries.value[index] = response.data
          }
        } else {
          response = await api.post('/api/diary/entries', newEntry.value)
          entries.value.push(response.data)
        }
        
        await displayEntriesOnMap()
        closeEditor()
        alert(isEditing.value ? 'Entry updated successfully!' : 'Entry added successfully!')
      } catch (error) {
        console.error('Error saving diary entry:', error)
        alert('Failed to save diary entry. Please try again.')
      }
    }

    const getCountryFlag = (location) => {
      // Common cities and their country flags
      const cityToFlag = {
        // Thailand
        'Bangkok': '🇹🇭',
        'Phuket': '🇹🇭',
        'Chiang Mai': '🇹🇭',
        // Germany
        'Berlin': '🇩🇪',
        'Munich': '🇩🇪',
        'Hamburg': '🇩🇪',
        // Netherlands
        'Amsterdam': '🇳🇱',
        'Rotterdam': '🇳🇱',
        'The Hague': '🇳🇱',
        // Add more cities as needed
      };

      // Try to find an exact match
      for (const [city, flag] of Object.entries(cityToFlag)) {
        if (location.includes(city)) {
          return flag;
        }
      }

      // If no match found, try to guess based on common country names
      const countryFlags = {
        'Thailand': '🇹🇭',
        'Germany': '🇩🇪',
        'Netherlands': '🇳🇱',
        'USA': '🇺🇸',
        'UK': '🇬🇧',
        'France': '🇫🇷',
        'Spain': '🇪🇸',
        'Italy': '🇮🇹',
        'Japan': '🇯🇵',
        'China': '🇨🇳',
        // Add more countries as needed
      };

      for (const [country, flag] of Object.entries(countryFlags)) {
        if (location.includes(country)) {
          return flag;
        }
      }

      // Default flag if no match found
      return '🌍';
    }

    const toggleDropdown = () => {
      isDropdownOpen.value = !isDropdownOpen.value
    }

    // Close dropdown when clicking outside
    onMounted(() => {
      document.addEventListener('click', (event) => {
        const dropdown = document.querySelector('.dropdown')
        if (dropdown && !dropdown.contains(event.target)) {
          isDropdownOpen.value = false
        }
      })
    })

    onMounted(async () => {
      try {
        console.log('Component mounted, initializing...');
        await loadEntries(); // Load entries first
        await nextTick(); // Wait for DOM update
        await initMap(); // Then initialize map
      } catch (err) {
        console.error('Error during component mount:', err);
        error.value = 'Failed to initialize the application. Please refresh the page.';
      }
    });

    onUnmounted(() => {
      cleanup()
    })

    // Initialize Bootstrap components
    onMounted(() => {
      // Initialize all collapse elements
      document.querySelectorAll('.accordion-collapse').forEach(collapseEl => {
        new Collapse(collapseEl, {
          toggle: false
        });
      });

      // Initialize modals
      editorModal.value = document.getElementById('editorModal');
      viewEntryModal.value = document.getElementById('viewEntryModal');

      // Initialize modal with options
      new Modal(editorModal.value, {
        keyboard: true,
        backdrop: true,
        focus: true
      });

      // Initialize dropdowns
      const dropdownElementList = document.querySelectorAll('[data-bs-toggle="dropdown"]');
      dropdownElementList.forEach(dropdownToggleEl => {
        new Dropdown(dropdownToggleEl);
      });

      // Add event listeners for modal focus management
      editorModal.value.addEventListener('shown.bs.modal', () => {
        // Focus the first input when modal opens
        const firstInput = editorModal.value.querySelector('input, textarea');
        if (firstInput) {
          firstInput.focus();
        }
      });

      editorModal.value.addEventListener('hidden.bs.modal', () => {
        // Reset form after modal is hidden
        newEntry.value = {
          title: '',
          content: '',
          location: {
            name: '',
            lat: null,
            lng: null
          },
          images: []
        };
      });

      // Add event listener for modal close button
      const closeButton = editorModal.value.querySelector('.btn-close');
      if (closeButton) {
        closeButton.addEventListener('click', closeEditor);
      }
    })

    return {
      mapContainer,
      mapElement,
      entries,
      newEntry,
      addDiaryEntry,
      handleImageUpload,
      removeImage,
      pickLocationOnMap,
      formatDate,
      selectedEntry,
      loading,
      error,
      retryLoading,
      handleDiaryEntryClick,
      viewAllLocations,
      closeSelectedEntry,
      editorModal,
      viewEntryModal,
      isEditing,
      openEditor,
      closeEditor,
      viewEntry,
      editEntry,
      saveDiaryEntry,
      closeEntry,
      getCountryFlag,
      isDropdownOpen,
      toggleDropdown,
    }
  }
}
</script>

<style scoped>
.travel-diary-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #f8f9fa;
}

.navbar {
  padding: 0.5rem 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.main-content {
  display: grid;
  grid-template-columns: minmax(600px, 1fr) 300px;
  gap: 1rem;
  padding: 1rem;
  height: calc(100vh - 56px); /* Subtract navbar height */
  overflow: hidden;
}

.map-wrapper {
  position: relative;
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  background: white;
}

.map-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

#map {
  width: 100%;
  height: 100%;
}

.diary-list {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow-y: auto;
  height: 100%;
}

.diary-entries {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.diary-card {
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.diary-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.diary-card-content {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  gap: 0.75rem;
}

.preview-image {
  width: 45px;
  height: 45px;
  border-radius: 4px;
  overflow: hidden;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.diary-card-middle {
  flex-grow: 1;
  min-width: 0;
  padding-right: 0.5rem;
}

.diary-card-middle h5 {
  margin: 0;
  font-size: 1rem;
  color: #333;
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.diary-card-middle .text-muted {
  font-size: 0.85rem;
  margin-top: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.map-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.8);
  z-index: 1000;
}

.map-overlay.error {
  background: rgba(255, 255, 255, 0.95);
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

.alert {
  margin: 1rem;
  text-align: center;
}

.ms-2 {
  margin-left: 0.5rem;
}

.text-center {
  text-align: center;
}

.py-4 {
  padding-top: 1.5rem;
  padding-bottom: 1.5rem;
}

.text-muted {
  color: #6c757d;
}

.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
  background: none;
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
  border-radius: 0.2rem;
  cursor: pointer;
}

.btn-outline-danger:hover {
  color: #fff;
  background-color: #dc3545;
}

.view-all-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 2;
  background: white;
  color: #007bff;
  border: 1px solid #007bff;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.view-all-btn:hover {
  background: #007bff;
  color: white;
}

.entry-details {
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.entry-details p {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.entry-details h6 {
  color: #495057;
  margin: 1rem 0 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #dee2e6;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.content-section, .images-section, .coordinates-section {
  margin-top: 1rem;
}

.diary-content {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  margin: 0.5rem 0;
  white-space: pre-wrap;
}

.country-flag {
  font-size: 1.1rem;
  flex-shrink: 0;
}

.btn-outline-primary {
  padding: 0.375rem;
  line-height: 1;
  border-radius: 4px;
}

.btn-outline-primary:hover {
  transform: scale(1.05);
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  z-index: 1000;
  min-width: 10rem;
  padding: 0.5rem 0;
  margin: 0;
  font-size: 1rem;
  color: #212529;
  text-align: left;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid rgba(0,0,0,.15);
  border-radius: 0.25rem;
  box-shadow: 0 0.5rem 1rem rgba(0,0,0,.15);
}

.dropdown-menu.show {
  display: block;
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 0.25rem 1.5rem;
  clear: both;
  font-weight: 400;
  color: #212529;
  text-align: inherit;
  white-space: nowrap;
  background-color: transparent;
  border: 0;
  cursor: pointer;
}

.dropdown-item:hover {
  color: #1e2125;
  background-color: #f8f9fa;
}

.dropdown-toggle {
  cursor: pointer;
  background: none;
  border: none;
  padding: 0.5rem 1rem;
  color: #212529;
}

.dropdown-toggle:hover {
  color: #0d6efd;
}
</style> 