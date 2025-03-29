<template>
  <div class="travel-diary-container">
    <div class="diary-form">
      <h3>Travel Diary</h3>
      <button class="btn btn-primary" @click="openEditor">
        <i class="fas fa-plus me-2"></i>New Entry
      </button>
    </div>

    <div class="map-wrapper">
      <transition name="fade" mode="out-in">
        <div v-if="!selectedEntry" class="map-container" ref="mapContainer">
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

          <button v-if="!loading && !error" @click="viewAllLocations" class="view-all-btn">
            <i class="fas fa-globe-americas me-2"></i>View All Locations
          </button>
        </div>
        <diary-entry-display
          v-else
          :entry="selectedEntry"
          @back-to-map="closeSelectedEntry"
          @edit="editEntry"
        />
      </transition>
    </div>

    <div class="diary-list">
      <h3>Diary Entries</h3>
      
      <!-- Loading state -->
      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        {{ error }}
        <button @click="retryLoading" class="btn btn-outline-danger btn-sm ms-2">
          Retry
        </button>
      </div>

      <!-- Empty state -->
      <div v-else-if="entries.length === 0" class="text-center py-4 text-muted">
        <i class="fas fa-book-open fa-3x mb-3"></i>
        <p>No diary entries yet. Start documenting your journey!</p>
      </div>

      <!-- Diary entries -->
      <div v-else class="accordion" id="diaryAccordion">
        <div v-for="(entry, index) in entries" 
             :key="entry._id" 
             class="accordion-item diary-card"
             @click="handleDiaryEntryClick(entry)">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed"
                    type="button"
                    :data-bs-target="'#collapse' + index"
                    data-bs-toggle="collapse">
              <div>
                <strong>{{ entry.title }}</strong>
                <div class="text-muted">{{ entry.location.name }}</div>
              </div>
            </button>
          </h2>
          <div :id="'collapse' + index" 
               class="accordion-collapse collapse"
               data-bs-parent="#diaryAccordion">
            <div class="accordion-body">
              <div class="entry-details">
                <div class="d-flex justify-content-end mb-2">
                  <button class="btn btn-outline-secondary btn-sm me-2" @click.stop="closeEntry(index)">
                    <i class="fas fa-times me-1"></i>Close
                  </button>
                  <button class="btn btn-primary btn-sm" @click.stop="editEntry(entry)">
                    <i class="fas fa-edit me-1"></i>Edit
                  </button>
                </div>
                <p><i class="fas fa-map-marker-alt me-2"></i>{{ entry.location.name }}</p>
                <p><i class="fas fa-calendar me-2"></i>Created: {{ formatDate(entry.created_at) }}</p>
                <p><i class="fas fa-images me-2"></i>Images: {{ entry.images.length }}</p>
                <div class="content-section">
                  <h6><i class="fas fa-book me-2"></i>Content</h6>
                  <p class="diary-content">{{ entry.content }}</p>
                </div>
                <div v-if="entry.images.length > 0" class="images-section">
                  <h6><i class="fas fa-camera me-2"></i>Images</h6>
                  <div class="diary-images">
                    <div v-for="(image, imgIndex) in entry.images" 
                         :key="imgIndex" 
                         class="diary-image">
                      <img :src="image" :alt="'Image ' + (imgIndex + 1)">
                    </div>
                  </div>
                </div>
                <div class="coordinates-section">
                  <h6><i class="fas fa-location-arrow me-2"></i>Coordinates</h6>
                  <p>Latitude: {{ entry.location.lat }}</p>
                  <p>Longitude: {{ entry.location.lng }}</p>
                </div>
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
import { Collapse } from 'bootstrap'
import { Modal } from 'bootstrap'
import DiaryEntryDisplay from './DiaryEntryDisplay.vue'

export default {
  name: 'TravelDiary',
  components: {
    DiaryEntryDisplay
  },
  setup() {
    const mapContainer = ref(null)
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
        if (!mapContainer.value) {
          throw new Error('Map container not found');
        }

        loading.value = true;
        error.value = null;

        // Load Google Maps API first
        google.value = await loadGoogleMaps();
        
        // Create map instance
        const mapElement = document.createElement('div');
        mapElement.style.width = '100%';
        mapElement.style.height = '100%';
        mapContainer.value.appendChild(mapElement);

        map.value = new google.value.maps.Map(mapElement, {
          center: { lat: 13.7563, lng: 100.5018 },
          zoom: 6,
          mapTypeControl: true,
          streetViewControl: true,
          fullscreenControl: true,
          zoomControl: true,
          gestureHandling: 'greedy'
        });

        geocoder.value = new google.value.maps.Geocoder();

        if (!geocoder.value) {
          throw new Error('Failed to initialize geocoder');
        }
        
        // Create markers for existing entries
        markers.value = entries.value.map(entry => {
          if (entry.location.lat && entry.location.lng) {
            const position = {
              lat: entry.location.lat,
              lng: entry.location.lng
            };

            const marker = new google.value.maps.Marker({
              map: map.value,
              position,
              title: entry.location.name,
              icon: {
                path: google.value.maps.SymbolPath.CIRCLE,
                scale: 8,
                fillColor: '#007bff',
                fillOpacity: 1,
                strokeColor: '#ffffff',
                strokeWeight: 2
              }
            });

            // Create info window
            const infoWindow = new google.value.maps.InfoWindow({
              content: `
                <div class="info-window">
                  <h5>${entry.title}</h5>
                  <div class="location-name">${entry.location.name}</div>
                  <div class="entry-preview">
                    ${entry.content.substring(0, 100)}...
                  </div>
                </div>
              `
            });

            // Add click listener
            marker.addListener('click', () => {
              if (activeInfoWindow.value) {
                activeInfoWindow.value.close();
              }
              infoWindow.open(map.value, marker);
              activeInfoWindow.value = infoWindow;
              selectedEntry.value = entry;
            });

            return marker;
          }
          return null;
        }).filter(marker => marker !== null);

        // Show all markers
        if (markers.value.length > 0) {
          viewAllLocations();
        }

        console.log('Map and geocoder initialized successfully');
        mapInitialized = true;
      } catch (err) {
        console.error('Error initializing map:', err);
        error.value = 'Failed to initialize map. Please try again.';
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
      if (!map.value || !google.value) {
        console.warn('Map not initialized yet')
        return
      }

      try {
        // Clear existing markers
        markers.value.forEach(marker => marker.setMap(null))
        markers.value = []

        if (!entries.value || entries.value.length === 0) {
          return
        }

        const bounds = new google.value.maps.LatLngBounds()
        
        for (const entry of entries.value) {
          const position = {
            lat: entry.location.lat,
            lng: entry.location.lng
          }

          bounds.extend(position)
          const marker = await createMarker(entry, position)
          if (marker) {
            markers.value.push(marker)
          }
        }

        map.value.fitBounds(bounds)
        if (markers.value.length === 1) {
          map.value.setZoom(15)
        }
      } catch (error) {
        console.error('Error displaying entries on map:', error)
        error.value = 'Failed to display entries on map. Please try again later.'
      }
    }

    const createMarker = async (entry, position) => {
      if (!map.value || !google.value) return null;

      try {
        const marker = new google.value.maps.Marker({
          map: map.value,
          position,
          title: entry.location.name,
          icon: {
            path: google.value.maps.SymbolPath.CIRCLE,
            scale: 8,
            fillColor: '#007bff',
            fillOpacity: 1,
            strokeColor: '#ffffff',
            strokeWeight: 2
          }
        });

        // Create info window
        const infoWindow = new google.value.maps.InfoWindow({
          content: `
            <div class="info-window">
              <h5>${entry.title}</h5>
              <div class="location-name">${entry.location.name}</div>
              <div class="entry-preview">
                ${entry.content.substring(0, 100)}...
              </div>
            </div>
          `
        });

        // Add click listener
        marker.addListener('click', () => {
          if (activeInfoWindow.value) {
            activeInfoWindow.value.close();
          }
          infoWindow.open(map.value, marker);
          activeInfoWindow.value = infoWindow;
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
      if (markers.value) {
        markers.value.forEach(marker => {
          if (marker) marker.setMap(null)
        })
        markers.value = []
      }

      if (activeInfoWindow.value) {
        activeInfoWindow.value.close()
        activeInfoWindow.value = null
      }

      if (map.value) {
        google.value?.maps.event.clearInstanceListeners(map.value)
        map.value = null
      }

      if (geocoder.value) {
        geocoder.value = null
      }

      if (google.value) {
        google.value = null
      }

      if (mapContainer.value) {
        mapContainer.value.innerHTML = ''
      }

      mapInitialized = false
      cleanupGoogleMaps()
    }

    const viewAllLocations = () => {
      if (!map.value || !markers.value.length) return;

      const bounds = new google.value.maps.LatLngBounds();
      markers.value.forEach(marker => {
        bounds.extend(marker.getPosition());
      });

      map.value.fitBounds(bounds);
      // Add some padding to the bounds
      map.value.setZoom(map.value.getZoom() - 0.5);
    }

    const handleDiaryEntryClick = (entry) => {
      selectedEntry.value = entry
      // Center map on entry location before switching view
      if (map.value && entry.location.lat && entry.location.lng) {
        map.value.setCenter({
          lat: entry.location.lat,
          lng: entry.location.lng
        })
        map.value.setZoom(15)
      }
    }

    const closeSelectedEntry = () => {
      selectedEntry.value = null;
      // Ensure the map is visible before updating its view
      nextTick(async () => {
        // Wait a bit for the transition to complete
        await new Promise(resolve => setTimeout(resolve, 300));
        if (map.value && markers.value.length > 0) {
          const bounds = new google.value.maps.LatLngBounds();
          markers.value.forEach(marker => {
            bounds.extend(marker.position);
          });
          map.value.fitBounds(bounds);
          map.value.setZoom(map.value.getZoom() - 0.5);
        }
      });
    };

    const closeEntry = (index) => {
      const collapseEl = document.querySelector(`#collapse${index}`);
      if (collapseEl) {
        const collapse = Collapse.getInstance(collapseEl);
        if (collapse) {
          collapse.hide();
          // Reset map to show all locations after closing entry
          viewAllLocations();
        }
      }
    };

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
      isEditing.value = true
      newEntry.value = { ...entry }
      new Modal(viewEntryModal.value).hide()
      nextTick(() => {
        new Modal(editorModal.value).show()
      })
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

    onMounted(async () => {
      try {
        await initMap()
        await loadEntries()
      } catch (err) {
        console.error('Error during component mount:', err)
        error.value = 'Failed to initialize the application. Please refresh the page.'
      }
    })

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
      saveDiaryEntry
    }
  }
}
</script>

<style scoped>
.travel-diary-container {
  display: grid;
  grid-template-columns: 200px minmax(600px, 1fr) 250px;
  gap: 1rem;
  height: 100vh;
  padding: 1rem;
  background: #f8f9fa;
}

.diary-form {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow-y: auto;
  height: calc(100vh - 2rem);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.map-wrapper {
  position: relative;
  height: calc(100vh - 2rem);
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
  background: #fff;
}

.diary-list {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow-y: auto;
  height: calc(100vh - 2rem);
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
  top: 20px;
  right: 20px;
  background: white;
  color: #007bff;
  border: 1px solid #007bff;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.2s ease;
}

.view-all-btn:hover {
  background: #007bff;
  color: white;
}

.entry-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
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

.diary-card {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.diary-card:hover {
  transform: translateY(-2px);
}

.accordion-button {
  transition: all 0.2s ease;
}

.accordion-button:not(.collapsed) {
  background-color: #e7f1ff;
  color: #0d6efd;
}

.accordion-button:hover {
  background-color: #f8f9fa;
}

.me-2 {
  margin-right: 0.5rem;
}

.diary-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
  margin: 0.5rem 0;
}

.diary-image {
  position: relative;
  padding-bottom: 100%;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.diary-image img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.2s ease;
}

.diary-image:hover img {
  transform: scale(1.05);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.marker-content {
  display: flex;
  align-items: center;
  justify-content: center;
}

.marker-pin {
  color: #007bff;
  font-size: 24px;
  filter: drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.3));
}
</style> 