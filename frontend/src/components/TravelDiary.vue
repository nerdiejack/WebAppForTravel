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
            <li class="nav-item dropdown position-relative">
              <button class="nav-link" @click="toggleDiaryList">
                Diary Entries <i class="fas fa-chevron-down" :class="{ 'rotate-180': !isDiaryListCollapsed }"></i>
              </button>
              <div v-show="!isDiaryListCollapsed" class="diary-list">
                <div v-if="entriesLoading" class="text-center py-4">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading entries...</span>
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
                       @click="selectedEntry = entry">
                    <div class="diary-card-content">
                      <div class="diary-card-left">
                        <div v-if="entry.images.length > 0" class="preview-image">
                          <img :src="entry.images[0].replace('/uploads/', '/uploads/thumbnails/')" :alt="entry.title">
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
            </li>
            <li class="nav-item dropdown">
              <button type="button" class="nav-link" @click="toggleDropdown">
                <i class="fas fa-cog"></i> Options <i class="fas fa-chevron-down ms-1" :class="{ 'rotate-180': isDropdownOpen }"></i>
              </button>
              <div class="dropdown-menu dropdown-menu-end" :class="{ 'show': isDropdownOpen }">
                <a class="dropdown-item" href="#" @click.prevent="openEditor">
                  <i class="fas fa-plus me-2"></i>New Entry
                </a>
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
          <div v-if="mapLoading" class="map-overlay">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading map...</span>
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
          <button v-if="!mapLoading && !error" @click="viewAllLocations" class="view-all-btn">
            <i class="fas fa-globe-americas me-2"></i>View All Locations
          </button>
        </div>
        <diary-entry-display
          v-if="selectedEntry"
          :entry="selectedEntry"
          @back-to-map="closeSelectedEntry"
          @edit="editEntry"
          @entry-deleted="loadEntries"
          class="diary-entry-display"
        />
      </div>

      <div class="diary-list" :class="{ collapsed: isDiaryListCollapsed }">
        <div 
          class="diary-list-handle" 
          data-bs-toggle="tooltip"
          data-bs-placement="top"
          title="Hover to see diary entries"
        >
          <span class="handle-text">Diary Entries</span>
        </div>
        <div v-if="entriesLoading" class="text-center py-4">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading entries...</span>
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
               @click="selectedEntry = entry">
            <div class="diary-card-content">
              <div class="diary-card-left">
                <div v-if="entry.images.length > 0" class="preview-image">
                  <img :src="entry.images[0].replace('/uploads/', '/uploads/thumbnails/')" :alt="entry.title">
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
      <div class="modal-dialog modal-lg modal-dialog-centered" style="max-width: 85%; width: 85%;">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editorModalLabel">{{ isEditing ? 'Edit Entry' : 'New Entry' }}</h5>
            <button type="button" class="btn-close" @click="closeEditor" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveDiaryEntry">
              <!-- Title Section -->
              <div class="form-floating mb-3">
                <input 
                  id="title"
                  v-model="newEntry.title" 
                  class="form-control form-control-lg" 
                  placeholder="Enter your title..."
                  required
                >
                <label for="title">Title</label>
              </div>
              
              <div class="entry-grid">
                <!-- Main Content Column -->
                <div class="entry-main">
                  <!-- Content Section -->
                  <div class="form-floating mb-3">
                    <textarea 
                      id="content"
                      v-model="newEntry.content" 
                      class="form-control content-area" 
                      placeholder="Write your story..."
                      required
                    ></textarea>
                    <label for="content">Write your story...</label>
                  </div>

                  <!-- Images Section -->
                  <div class="images-section">
                    <label class="form-label d-block mb-2">Images</label>
                    <div class="image-preview-grid">
                      <div v-for="(image, index) in imagePreviewUrls" 
                           :key="index" 
                           class="image-preview-item">
                        <div class="image-number">{{ index + 1 }}</div>
                        <img :src="image.thumbnail" 
                             :alt="'Preview ' + (index + 1)" 
                             class="preview-image"
                             @click="openImagePreview(image.original)">
                        <button type="button" @click="removeImage(index)" class="btn btn-danger btn-sm remove-image">
                          <i class="fas fa-times"></i>
                        </button>
                      </div>
                      <!-- Add Image Upload Box -->
                      <div class="image-upload-box" @click="triggerImageUpload">
                        <input 
                          type="file" 
                          @change="handleImageUpload" 
                          accept="image/*" 
                          multiple 
                          class="d-none"
                          ref="imageInput"
                          :disabled="uploadLoading || loading"
                        >
                        <div class="upload-content">
                          <i class="fas fa-plus-circle fa-2x mb-2"></i>
                          <p class="mb-0">Add Image</p>
                        </div>
                      </div>
                    </div>
                    <div v-if="uploadStatus" class="upload-status alert alert-info mt-3">
                      <div class="d-flex align-items-center">
                        <div class="spinner-border spinner-border-sm me-2" role="status">
                          <span class="visually-hidden">Loading...</span>
                        </div>
                        <span>{{ uploadStatus }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Sidebar -->
                <div class="entry-sidebar">
                  <div class="location-card">
                    <h6 class="location-card-title">Location Details</h6>
                    <div class="form-floating mb-3">
                      <input 
                        v-model="newEntry.location.name" 
                        class="form-control" 
                        id="locationName"
                        placeholder="Location name"
                        required
                      >
                      <label for="locationName">Location name</label>
                    </div>
                    <div class="form-floating mb-3">
                      <input 
                        v-model.number="newEntry.location.lat" 
                        type="number" 
                        class="form-control" 
                        id="latitude"
                        placeholder="Latitude"
                        step="any"
                        required
                      >
                      <label for="latitude">Latitude</label>
                    </div>
                    <div class="form-floating">
                      <input 
                        v-model.number="newEntry.location.lng" 
                        type="number" 
                        class="form-control" 
                        id="longitude"
                        placeholder="Longitude"
                        step="any"
                        required
                      >
                      <label for="longitude">Longitude</label>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-light" @click="closeEditor" :disabled="loading || uploadLoading">Cancel</button>
            <button type="submit" class="btn btn-primary" @click="saveDiaryEntry" :disabled="loading || uploadLoading">
              <span v-if="loading || uploadLoading" class="spinner-border spinner-border-sm me-2" role="status">
                <span class="visually-hidden">Loading...</span>
              </span>
              {{ isEditing ? 'Update Entry' : 'Save Entry' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add image preview modal -->
    <div class="modal fade" id="imagePreviewModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body text-center p-0">
            <img :src="selectedImage" class="img-fluid" alt="Full size preview">
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
import { Collapse, Modal, Dropdown, Tooltip } from 'bootstrap'
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
    const uploadLoading = ref(false)
    const mapLoading = ref(false)
    const entriesLoading = ref(false)
    const error = ref(null)
    const geocoder = ref(null)
    const google = ref(null)
    const isDropdownOpen = ref(false)
    const imageInput = ref(null)
    const isDiaryListCollapsed = ref(true)

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
    const isEditing = ref(false)

    const imageFiles = ref([])
    const imagePreviewUrls = ref([])
    const uploadStatus = ref('')

    const selectedImage = ref(null)
    const imagePreviewModal = ref(null)

    const initMap = async () => {
      try {
        if (!mapContainer.value || !mapElement.value) {
          console.error('Map container or element ref is null');
          throw new Error('Map container not found');
        }

        mapLoading.value = true;
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
        mapLoading.value = false;
      }
    };

    const loadEntries = async () => {
      try {
        entriesLoading.value = true
        error.value = null
        
        const response = await api.get('/api/diary/entries')
        entries.value = response.data
        await displayEntriesOnMap()
      } catch (error) {
        console.error('Error loading diary entries:', error)
        error.value = 'Failed to load diary entries. Please try again later.'
        entries.value = []
      } finally {
        entriesLoading.value = false
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

    const resizeImage = (file) => {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.src = URL.createObjectURL(file);
        
        img.onload = () => {
          // Max dimensions for 4K
          const MAX_WIDTH = 3840;
          const MAX_HEIGHT = 2160;
          
          let width = img.width;
          let height = img.height;
          
          // Calculate new dimensions while maintaining aspect ratio
          if (width > MAX_WIDTH || height > MAX_HEIGHT) {
            const ratio = Math.min(MAX_WIDTH / width, MAX_HEIGHT / height);
            width = Math.floor(width * ratio);
            height = Math.floor(height * ratio);
          }
          
          // Only resize if the image is larger than 4K
          if (width === img.width && height === img.height) {
            URL.revokeObjectURL(img.src);
            resolve(file);
            return;
          }
          
          const canvas = document.createElement('canvas');
          canvas.width = width;
          canvas.height = height;
          
          const ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0, width, height);
          
          // Convert to blob with high quality
          canvas.toBlob((blob) => {
            URL.revokeObjectURL(img.src);
            resolve(new File([blob], file.name, {
              type: 'image/jpeg',
              lastModified: Date.now()
            }));
          }, 'image/jpeg', 0.92); // Use JPEG with 92% quality
        };
        
        img.onerror = (error) => {
          URL.revokeObjectURL(img.src);
          reject(error);
        };
      });
    };

    const handleImageUpload = async (event) => {
      const files = event.target.files;
      if (!files.length) return;

      // Process each file
      for (const file of files) {
        try {
          // Validate file type
          if (!file.type.startsWith('image/')) {
            alert('Please upload only image files');
            continue;
          }

          // Validate file size (max 25MB)
          if (file.size > 25 * 1024 * 1024) {
            alert(`File ${file.name} is too large. Maximum size is 25MB`);
            continue;
          }

          // Resize image if needed
          const resizedFile = await resizeImage(file);

          // Add to files array
          imageFiles.value.push(resizedFile);

          // Create preview URL
          const reader = new FileReader();
          reader.onload = (e) => {
            imagePreviewUrls.value.push({
              original: e.target.result,
              thumbnail: e.target.result // For new uploads, use same URL for both
            });
          };
          reader.readAsDataURL(resizedFile);
        } catch (error) {
          console.error('Error processing image:', error);
          alert(`Failed to process image ${file.name}. Please try again.`);
        }
      }
    };

    const uploadImages = async () => {
      const uploadedUrls = [];
      uploadLoading.value = true;
      
      try {
        for (const file of imageFiles.value) {
          const formData = new FormData();
          formData.append('file', file);
          
          uploadStatus.value = `Uploading ${file.name}...`;
          const response = await fetch('/api/diary/upload-image/', {
            method: 'POST',
            body: formData,
          });
          
          if (!response.ok) {
            throw new Error(`Failed to upload image ${file.name}`);
          }
          
          const data = await response.json();
          uploadedUrls.push({
            original: data.url,
            thumbnail: data.thumbnail_url
          });
        }
        
        uploadStatus.value = '';
        return uploadedUrls;
      } catch (error) {
        console.error('Error uploading image:', error);
        alert(`Failed to upload images. Please try again.`);
        throw error;
      } finally {
        uploadLoading.value = false;
      }
    };

    const removeImage = (index) => {
      // If the image is a data URL (new upload), remove from both arrays
      if (imagePreviewUrls.value[index].original.startsWith('data:')) {
        const fileIndex = imageFiles.value.findIndex((_, i) => {
          const reader = new FileReader();
          return new Promise((resolve) => {
            reader.onload = (e) => {
              resolve(e.target.result === imagePreviewUrls.value[index].original);
            };
            reader.readAsDataURL(imageFiles.value[i]);
          });
        });
        if (fileIndex !== -1) {
          imageFiles.value.splice(fileIndex, 1);
        }
      }
      imagePreviewUrls.value.splice(index, 1);
    }

    const pickLocationOnMap = async () => {
      if (!map.value || !google.value) {
        console.warn('Map not initialized yet')
        return
      }

      // If we're in entry view mode, close it first
      if (selectedEntry.value) {
        await closeSelectedEntry();
      }

      // Make sure map is visible
      if (mapContainer.value) {
        mapContainer.value.style.visibility = 'visible';
      }

      // If map needs to be reinitialized
      if (!mapInitialized) {
        await initMap();
      }

      isPickingLocation.value = true;
      alert('Click on the map to set the location');

      const clickListener = map.value.addListener('click', (event) => {
        newEntry.value.location.lat = event.latLng.lat();
        newEntry.value.location.lng = event.latLng.lng();
        isPickingLocation.value = false;
        google.value.maps.event.removeListener(clickListener);
        alert('Location set!');
      });
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

    const handleDiaryEntryClick = (entry) => {
      selectedEntry.value = entry;
    }

    const closeSelectedEntry = () => {
      selectedEntry.value = null;
    }

    const closeEntry = (index) => {
      const collapseElement = document.getElementById('collapse' + index);
      const collapse = Collapse.getInstance(collapseElement);
      if (collapse) {
        collapse.hide();
      }
    }

    const openEditor = () => {
      isEditing.value = false;
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
      // Reset image-related state
      imagePreviewUrls.value = [];
      imageFiles.value = [];
      uploadStatus.value = '';
      if (imageInput.value) {
        imageInput.value.value = '';
      }
      
      // Close the options dropdown
      isDropdownOpen.value = false;
      
      // Show the modal using Bootstrap
      const modal = new Modal(editorModal.value);
      modal.show();
    };

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
        // Reset image-related state
        imagePreviewUrls.value = []
        imageFiles.value = []
        uploadStatus.value = ''
        if (imageInput.value) {
          imageInput.value.value = ''
        }
      }, { once: true });
    }

    const editEntry = (entry) => {
      // Set up the entry for editing with ALL fields
      newEntry.value = {
        _id: entry._id,
        title: entry.title,
        content: entry.content,
        location: {
          name: entry.location.name,
          lat: entry.location.lat,
          lng: entry.location.lng
        },
        images: entry.images || [],
        created_at: entry.created_at,
        updated_at: entry.updated_at
      };
      isEditing.value = true;
      
      // Set existing images for preview
      imagePreviewUrls.value = entry.images.map(url => ({
        original: url,
        thumbnail: url.replace('/uploads/', '/uploads/thumbnails/')
      }));
      imageFiles.value = []; // Reset image files since these are existing images
      
      // Show the editor modal
      const modal = new Modal(editorModal.value);
      modal.show();
    }

    const saveDiaryEntry = async () => {
      if (uploadLoading.value || loading.value) {
        return;
      }

      try {
        loading.value = true;
        
        // Upload only new images (from imageFiles)
        let uploadedImageUrls = [];
        if (imageFiles.value.length > 0) {
          uploadedImageUrls = await uploadImages();
        }
        
        // Combine existing images with newly uploaded ones
        const existingImages = imagePreviewUrls.value
          .filter(url => !url.original.startsWith('data:'))
          .map(url => url.original);
        
        // Prepare the complete entry data
        const entryData = {
          ...newEntry.value,
          images: [...existingImages, ...uploadedImageUrls.map(url => url.original)],
          updated_at: new Date().toISOString()
        };

        // Save the diary entry
        const url = isEditing.value 
          ? `/api/diary/entries/${entryData._id}` 
          : '/api/diary/entries/';

        const response = await fetch(url, {
          method: isEditing.value ? 'PUT' : 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(entryData),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to save diary entry');
        }

        // Reset form and close modal
        resetForm();
        closeEditor();
        
        // Refresh entries
        await loadEntries();
        
        alert(isEditing.value ? 'Entry updated successfully!' : 'Entry added successfully!');
      } catch (error) {
        console.error('Error saving diary entry:', error);
        alert(error.message || 'Failed to save diary entry. Please try again.');
      } finally {
        loading.value = false;
      }
    };

    const resetForm = () => {
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
      imageFiles.value = [];
      imagePreviewUrls.value = [];
      isEditing.value = false;
      if (imageInput.value) {
        imageInput.value.value = '';
      }
    };

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

    const toggleDropdown = (event) => {
      event.stopPropagation() // Prevent event bubbling
      
      // Close diary list if it's open
      if (!isDiaryListCollapsed.value) {
        isDiaryListCollapsed.value = true
      }
      
      isDropdownOpen.value = !isDropdownOpen.value

      // Close dropdown when clicking outside
      const closeDropdown = (e) => {
        if (!e.target.closest('.nav-item.dropdown')) {
          isDropdownOpen.value = false
          document.removeEventListener('click', closeDropdown)
        }
      }

      if (isDropdownOpen.value) {
        // Add event listener with a slight delay to avoid immediate trigger
        setTimeout(() => {
          document.addEventListener('click', closeDropdown)
        }, 0)
      }
    }

    const toggleDiaryList = (event) => {
      event.stopPropagation()
      
      // Close options dropdown if it's open
      if (isDropdownOpen.value) {
        isDropdownOpen.value = false
      }
      
      isDiaryListCollapsed.value = !isDiaryListCollapsed.value
    }

    // Add cleanup for dropdown listeners
    onUnmounted(() => {
      document.removeEventListener('click', closeDropdown)
      cleanup()
    })

    const openImagePreview = (imageUrl) => {
      selectedImage.value = imageUrl;
      new Modal(imagePreviewModal.value).show();
    };

    const triggerImageUpload = () => {
      if (imageInput.value) {
        imageInput.value.click();
      }
    };

    const handleClickOutside = (event) => {
      const diaryListButton = document.querySelector('.nav-item.dropdown .nav-link')
      const diaryList = document.querySelector('.diary-list')
      
      if (!isDiaryListCollapsed.value && 
          !diaryList?.contains(event.target) && 
          !diaryListButton?.contains(event.target)) {
        isDiaryListCollapsed.value = true
      }
    }

    onMounted(async () => {
      try {
        console.log('Component mounted, initializing...')
        await loadEntries() // Load entries first
        await nextTick() // Wait for DOM update
        await initMap() // Then initialize map

        // Initialize modals
        editorModal.value = document.getElementById('editorModal')
        imagePreviewModal.value = document.getElementById('imagePreviewModal')

        // Initialize modals with Bootstrap
        if (editorModal.value) {
          new Modal(editorModal.value)
        }
        if (imagePreviewModal.value) {
          new Modal(imagePreviewModal.value)
        }

        // Add click outside listener
        document.addEventListener('click', handleClickOutside)

        // Initialize tooltips
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
        tooltipTriggerList.forEach(tooltipTriggerEl => {
          new Tooltip(tooltipTriggerEl)
        })

      } catch (err) {
        console.error('Error during component mount:', err)
        error.value = 'Failed to initialize the application'
      }
    })

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
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
      uploadLoading,
      mapLoading,
      entriesLoading,
      error,
      retryLoading,
      handleDiaryEntryClick,
      viewAllLocations,
      closeSelectedEntry,
      editorModal,
      isEditing,
      openEditor,
      closeEditor,
      editEntry,
      saveDiaryEntry,
      closeEntry,
      getCountryFlag,
      isDropdownOpen,
      toggleDropdown,
      imageFiles,
      imagePreviewUrls,
      resetForm,
      imageInput,
      uploadStatus,
      selectedImage,
      openImagePreview,
      triggerImageUpload,
      isDiaryListCollapsed,
      toggleDiaryList,
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
  flex: 1;
  padding: 1rem;
  overflow: hidden;
}

.map-wrapper {
  position: relative;
  height: 85vh;
  max-width: 1400px;
  margin: 0 auto;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
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

.view-all-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 2;
  background: white;
  color: #007bff;
  border: 1px solid #007bff;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.view-all-btn:hover {
  background: #007bff;
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* Update diary list positioning */
.diary-list {
  position: absolute;
  right: 0;
  top: 100%;
  width: 400px;
  max-height: 600px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  overflow-y: auto;
  z-index: 1000;
  margin-top: 0.5rem;
  border: 1px solid rgba(0,0,0,0.1);
  padding: 1rem;
}

.rotate-180 {
  transform: rotate(180deg);
}

.nav-item.dropdown {
  position: relative;
}

.nav-item.dropdown .nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem 1rem;
  background: none;
  border: none;
  color: #212529;
  text-decoration: none;
}

.nav-item.dropdown .nav-link:hover {
  color: #0d6efd;
}

.nav-item.dropdown .nav-link i {
  transition: transform 0.3s ease;
}

.dropdown-menu {
  position: absolute;
  right: 0;
  top: 100%;
  margin-top: 0.5rem;
  min-width: 200px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  border: 1px solid rgba(0,0,0,0.1);
  z-index: 1000;
  padding: 0.5rem 0;
  display: none;
}

.dropdown-menu.show {
  display: block;
}

.dropdown-menu-end {
  right: 0;
  left: auto;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: #212529;
  text-decoration: none;
  transition: all 0.2s ease;
  white-space: nowrap;
  cursor: pointer;
}

.dropdown-item:hover {
  background: #f8f9fa;
  color: #0d6efd;
}

.diary-list-handle {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 40px;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 0 0 8px 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  padding: 0 1rem;
  display: none; /* Hide the handle by default */
}

.diary-list-handle::before {
  content: '↓';
  font-size: 1.2rem;
  color: #6c757d;
  transition: transform 0.3s ease;
}

.diary-list:hover .diary-list-handle::before {
  transform: rotate(180deg);
}

.handle-text {
  color: #6c757d;
  font-size: 0.9rem;
  font-weight: 500;
}

.diary-entries {
  padding-bottom: 40px; /* Add space for the handle */
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
  margin-bottom: 0.75rem;
}

.diary-card:last-child {
  margin-bottom: 0;
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

.diary-card-left {
  width: 60px;
  height: 60px;
  flex-shrink: 0;
  margin-right: 1rem;
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

.diary-card-right {
  flex-shrink: 0;
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

.modal-dialog {
  margin: 1.75rem auto;
}

.image-preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.image-preview-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease;
  border: 1px solid #dee2e6;
}

.image-preview-item:hover {
  transform: scale(1.05);
}

.image-preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-number {
  position: absolute;
  top: 8px;
  left: 8px;
  background-color: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
}

.remove-image {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 0.2rem 0.4rem;
  font-size: 0.8rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.image-preview-item:hover .remove-image {
  opacity: 1;
}

.preview-image {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
}

.preview-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-image.no-image {
  color: #adb5bd;
  font-size: 1.5rem;
}

.upload-status {
  margin-bottom: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  background-color: #cfe2ff;
  border-color: #b6d4fe;
  color: #084298;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
  border-width: 0.2em;
}

.btn:disabled {
  cursor: not-allowed;
  opacity: 0.65;
}

#imagePreviewModal .modal-body {
  background-color: #000;
  max-height: 80vh;
  overflow: auto;
}

#imagePreviewModal .img-fluid {
  max-height: 70vh;
  width: auto;
  margin: 0 auto;
}

.image-upload-box {
  position: relative;
  aspect-ratio: 1;
  border: 2px dashed #dee2e6;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
}

.image-upload-box:hover {
  border-color: #007bff;
  background-color: #f1f8ff;
}

.upload-content {
  text-align: center;
  color: #6c757d;
}

.upload-content i {
  color: #007bff;
}

.upload-content p {
  font-size: 0.9rem;
  color: #6c757d;
}

.image-upload-box:hover .upload-content {
  color: #007bff;
}

.image-upload-box:hover .upload-content p {
  color: #007bff;
}

.form-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 1rem;
  margin-bottom: 1rem;
}

.content-section {
  flex: 1;
}

.content-section textarea {
  height: 100%;
  min-height: 300px;
  resize: vertical;
}

.location-section {
  width: 100%;
}

.coordinates {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.5rem;
}

.coordinates input {
  width: 100%;
}

.entry-grid {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.entry-main {
  min-height: 400px;
}

.content-area {
  height: 300px !important;
  resize: vertical;
  font-size: 1rem;
  line-height: 1.6;
}

.entry-sidebar {
  position: sticky;
  top: 1rem;
}

.location-card {
  background-color: #f8f9fa;
  border-radius: 12px;
  padding: 1.25rem;
  border: 1px solid #e9ecef;
}

.location-card-title {
  color: #495057;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.form-floating {
  position: relative;
}

.form-floating > label {
  position: absolute;
  top: 0;
  left: 0;
  padding: 1rem;
  opacity: 0.65;
  transform-origin: 0 0;
  transition: opacity .1s ease-in-out, transform .1s ease-in-out;
}

.form-floating > .form-control:focus ~ label,
.form-floating > .form-control:not(:placeholder-shown) ~ label {
  opacity: .65;
  transform: scale(.85) translateY(-0.5rem) translateX(0.15rem);
  background-color: white;
  padding: 0 0.5rem;
  margin-left: -0.5rem;
}

.form-control-lg {
  font-size: 1.25rem;
  padding: 1rem 1.25rem;
}

.images-section {
  margin-top: 2rem;
}

.image-preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 1rem;
  margin-top: 0.5rem;
}

.image-preview-item {
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.image-upload-box {
  border: 2px dashed #dee2e6;
  border-radius: 12px;
  background-color: #f8f9fa;
  transition: all 0.2s ease;
}

.image-upload-box:hover {
  border-color: #007bff;
  background-color: #f1f8ff;
}

.btn-light {
  background-color: #f8f9fa;
  border-color: #e9ecef;
}

.btn-light:hover {
  background-color: #e9ecef;
  border-color: #dde2e6;
}

.modal-footer {
  border-top: 1px solid #e9ecef;
  padding: 1.25rem;
}

.form-label {
  font-weight: 500;
  color: #495057;
}

.entry-view-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 450px;
  gap: 2rem;
  min-height: 400px;
}

.entry-content {
  padding-right: 1rem;
  overflow-y: auto;
  max-height: 70vh;
}

.entry-metadata {
  color: #6c757d;
  font-size: 0.95rem;
}

.entry-text {
  font-size: 1rem;
  line-height: 1.6;
  white-space: pre-wrap;
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
}

.coordinates {
  font-size: 0.9rem;
  color: #6c757d;
  padding-top: 1rem;
  border-top: 1px solid #dee2e6;
}

.entry-images {
  overflow-y: auto;
  max-height: 70vh;
  padding-right: 0.5rem;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.image-item {
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.image-item:hover {
  transform: scale(1.05);
}

.image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.modal-xl {
  max-width: 1200px;
}

@media (max-width: 991px) {
  .entry-view-layout {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .entry-content {
    padding-right: 0;
  }

  .image-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.diary-entry-display {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
  background: white;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 450px;
  gap: 2rem;
  padding: 2rem;
  overflow-y: auto;
}

@media (max-width: 991px) {
  .diary-entry-display {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}

/* Add a toggle button in the navbar */
.toggle-list-btn {
  background: none;
  border: none;
  color: #212529;
  padding: 0.5rem 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.toggle-list-btn:hover {
  color: #0d6efd;
}

.toggle-list-btn i {
  transition: transform 0.3s ease;
}

.toggle-list-btn.collapsed i {
  transform: rotate(180deg);
}
</style> 