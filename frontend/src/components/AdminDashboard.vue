<template>
  <div class="admin-dashboard">
    <!-- Toast Notification -->
    <div class="custom-toast" v-if="showToast" :class="toastType">
      {{ toastMessage }}
    </div>

    <div class="container-fluid py-4">
      <!-- Tabs -->
      <ul class="nav nav-tabs mb-4">
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'hotels' }" @click="activeTab = 'hotels'" href="#">
            Hotel Reservations
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'diary' }" @click="activeTab = 'diary'" href="#">
            Diary Entries
          </a>
        </li>
      </ul>

      <!-- Hotels Tab Content -->
      <div v-if="activeTab === 'hotels'">
        <div class="row mb-4">
          <div class="col">
            <h2>Hotel Reservations Admin</h2>
          </div>
        </div>

        <!-- Hotels Search and Filter -->
        <div class="row mb-4">
          <div class="col-md-4">
            <input 
              type="text" 
              class="form-control" 
              v-model="searchQuery" 
              placeholder="Search by hotel name, city, or guest name..."
              @input="filterReservations"
            >
          </div>
        </div>

        <!-- Hotels Table -->
        <div class="table-responsive">
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>Hotel Name</th>
                <th>City</th>
                <th>Guest</th>
                <th>Check-in</th>
                <th>Check-out</th>
                <th>Room Type</th>
                <th>Price/Night</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="reservation in filteredReservations" 
                  :key="reservation._id" 
                  @click="handleReservationClick(reservation)"
                  class="cursor-pointer hover-highlight">
                <td>{{ reservation.hotel_name || 'Unnamed Hotel' }}</td>
                <td>{{ reservation.city || 'Unknown City' }}</td>
                <td>{{ reservation.guest_name || 'Unknown Guest' }}</td>
                <td>{{ formatDate(reservation.check_in) }}</td>
                <td>{{ formatDate(reservation.check_out) }}</td>
                <td>{{ reservation.room_type || 'Standard Room' }}</td>
                <td>€{{ formatPrice(reservation.price_per_night) }}</td>
                <td>
                  <span :class="getStatusClass(reservation.status)">
                    {{ reservation.status || 'confirmed' }}
                  </span>
                </td>
                <td>
                  <div class="btn-group">
                    <button class="btn btn-sm btn-primary" @click="editReservation(reservation)">
                      Edit
                    </button>
                    <button class="btn btn-sm btn-danger" @click="confirmDelete(reservation)">
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredReservations.length === 0">
                <td colspan="9" class="text-center py-4">
                  No reservations found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Diary Entries Tab Content -->
      <div v-if="activeTab === 'diary'">
        <div class="row mb-4">
          <div class="col">
            <h2>Diary Entries Admin</h2>
          </div>
        </div>

        <!-- Diary Search and Filter -->
        <div class="row mb-4">
          <div class="col-md-4">
            <input 
              type="text" 
              class="form-control" 
              v-model="diarySearchQuery" 
              placeholder="Search by title or location..."
              @input="filterDiaryEntries"
            >
          </div>
        </div>

        <!-- Diary Entries Table -->
        <div class="table-responsive">
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>Title</th>
                <th>Location</th>
                <th>Created At</th>
                <th>Images</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="entry in filteredDiaryEntries" 
                  :key="entry._id" 
                  @click="handleDiaryEntryClick(entry)"
                  class="cursor-pointer hover-highlight">
                <td>{{ entry.title }}</td>
                <td>{{ entry.location.name }}</td>
                <td>{{ formatDate(entry.created_at) }}</td>
                <td>{{ entry.images.length }} images</td>
                <td>
                  <div class="btn-group">
                    <button class="btn btn-sm btn-primary" @click="editDiaryEntry(entry)">
                      Edit
                    </button>
                    <button class="btn btn-sm btn-danger" @click="confirmDeleteDiary(entry)">
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredDiaryEntries.length === 0">
                <td colspan="5" class="text-center py-4">
                  No diary entries found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div class="modal fade" id="editModal" tabindex="-1" ref="editModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Reservation</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateReservation" v-if="editingReservation">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Hotel Name</label>
                  <input type="text" class="form-control" v-model="editingReservation.hotel_name" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">City</label>
                  <input type="text" class="form-control" v-model="editingReservation.city" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Latitude</label>
                  <input type="number" class="form-control" v-model="editingReservation.latitude" step="any" placeholder="e.g., 13.7563">
                </div>
                <div class="col-md-6">
                  <label class="form-label">Longitude</label>
                  <input type="number" class="form-control" v-model="editingReservation.longitude" step="any" placeholder="e.g., 100.5018">
                </div>
                <div class="col-md-6">
                  <label class="form-label">Check-in</label>
                  <input type="date" class="form-control" v-model="editingReservation.check_in" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Check-out</label>
                  <input type="date" class="form-control" v-model="editingReservation.check_out" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Room Type</label>
                  <input type="text" class="form-control" v-model="editingReservation.room_type" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Price per Night (€)</label>
                  <div class="input-group">
                    <span class="input-group-text">€</span>
                    <input type="number" class="form-control" v-model="editingReservation.price_per_night" step="0.01" min="0" required>
                  </div>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Guest Name</label>
                  <input type="text" class="form-control" v-model="editingReservation.guest_name" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Number of Guests</label>
                  <input type="number" class="form-control" v-model="editingReservation.number_of_guests" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Status</label>
                  <select class="form-select" v-model="editingReservation.status">
                    <option value="confirmed">Confirmed</option>
                    <option value="cancelled">Cancelled</option>
                    <option value="completed">Completed</option>
                  </select>
                </div>
                <div class="col-12">
                  <label class="form-label">Special Requests</label>
                  <textarea class="form-control" v-model="editingReservation.special_requests" rows="3"></textarea>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="updateReservation">Save Changes</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div class="modal fade" id="deleteModal" tabindex="-1" ref="deleteModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Delete</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="deletingReservation">
            <p>Are you sure you want to delete the reservation for:</p>
            <p class="fw-bold">{{ deletingReservation.hotel_name }} - {{ deletingReservation.guest_name }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="deleteReservation">Delete</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Booking Details Modal -->
    <div class="modal fade" id="bookingDetailsModal" tabindex="-1" ref="bookingDetailsModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Booking Details</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="selectedReservation">
            <div class="row">
              <div class="col-md-6">
                <h6>Hotel Information</h6>
                <p><strong>Hotel Name:</strong> {{ selectedReservation.hotel_name }}</p>
                <p><strong>City:</strong> {{ selectedReservation.city }}</p>
                <p><strong>Address:</strong> {{ selectedReservation.address }}</p>
                <p><strong>Room Type:</strong> {{ selectedReservation.room_type }}</p>
                <p><strong>Price per Night:</strong> €{{ formatPrice(selectedReservation.price_per_night) }}</p>
              </div>
              <div class="col-md-6">
                <h6>Guest Information</h6>
                <p><strong>Guest Name:</strong> {{ selectedReservation.guest_name }}</p>
                <p><strong>Number of Guests:</strong> {{ selectedReservation.number_of_guests }}</p>
                <p><strong>Status:</strong> <span :class="getStatusClass(selectedReservation.status)">{{ selectedReservation.status }}</span></p>
                <p><strong>Booking Reference:</strong> {{ selectedReservation.booking_reference || 'N/A' }}</p>
              </div>
              <div class="col-md-6">
                <h6>Dates</h6>
                <p><strong>Check-in:</strong> {{ formatDate(selectedReservation.check_in) }}</p>
                <p><strong>Check-out:</strong> {{ formatDate(selectedReservation.check_out) }}</p>
                <p><strong>Total Price:</strong> €{{ formatPrice(selectedReservation.total_price) }}</p>
              </div>
              <div class="col-md-6">
                <h6>Location</h6>
                <p><strong>Latitude:</strong> {{ selectedReservation.latitude || 'N/A' }}</p>
                <p><strong>Longitude:</strong> {{ selectedReservation.longitude || 'N/A' }}</p>
                <button v-if="selectedReservation.latitude && selectedReservation.longitude" 
                        class="btn btn-sm btn-primary mt-2"
                        @click="zoomToLocation">
                  <i class="fas fa-map-marker-alt me-1"></i> View on Map
                </button>
              </div>
              <div class="col-12 mt-3" v-if="selectedReservation.special_requests">
                <h6>Special Requests</h6>
                <p>{{ selectedReservation.special_requests }}</p>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="editSelectedReservation">Edit</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Diary Entry Edit Modal -->
    <div class="modal fade" id="editDiaryModal" tabindex="-1" ref="editDiaryModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Diary Entry</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateDiaryEntry" v-if="editingDiaryEntry">
              <div class="row g-3">
                <div class="col-12">
                  <label class="form-label">Title</label>
                  <input type="text" class="form-control" v-model="editingDiaryEntry.title" required>
                </div>
                <div class="col-12">
                  <label class="form-label">Content</label>
                  <textarea class="form-control" v-model="editingDiaryEntry.content" rows="5" required></textarea>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Location Name</label>
                  <input type="text" class="form-control" v-model="editingDiaryEntry.location.name" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Latitude</label>
                  <input type="number" class="form-control" v-model="editingDiaryEntry.location.lat" step="any" required>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Longitude</label>
                  <input type="number" class="form-control" v-model="editingDiaryEntry.location.lng" step="any" required>
                </div>
                <div class="col-12">
                  <label class="form-label">Images</label>
                  <div class="image-grid">
                    <div v-for="(image, index) in editingDiaryEntry.images" 
                         :key="index" 
                         class="image-item">
                      <img :src="image" :alt="'Image ' + (index + 1)" class="img-thumbnail">
                      <button type="button" 
                              class="btn btn-danger btn-sm"
                              @click="removeDiaryImage(index)">
                        Remove
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="updateDiaryEntry">Save Changes</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Diary Entry Delete Modal -->
    <div class="modal fade" id="deleteDiaryModal" tabindex="-1" ref="deleteDiaryModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Delete</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="deletingDiaryEntry">
            <p>Are you sure you want to delete this diary entry?</p>
            <p class="fw-bold">{{ deletingDiaryEntry.title }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="deleteDiaryEntry">Delete</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Diary Entry Details Modal -->
    <div class="modal fade" id="diaryDetailsModal" tabindex="-1" ref="diaryDetailsModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Diary Entry Details</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body" v-if="selectedDiaryEntry">
            <div class="row">
              <div class="col-12">
                <h3>{{ selectedDiaryEntry.title }}</h3>
                <p class="text-muted">
                  Created: {{ formatDate(selectedDiaryEntry.created_at) }}
                </p>
              </div>
              <div class="col-12">
                <h6>Content</h6>
                <p class="diary-content">{{ selectedDiaryEntry.content }}</p>
              </div>
              <div class="col-md-6">
                <h6>Location</h6>
                <p><strong>Name:</strong> {{ selectedDiaryEntry.location.name }}</p>
                <p><strong>Coordinates:</strong> {{ selectedDiaryEntry.location.lat }}, {{ selectedDiaryEntry.location.lng }}</p>
              </div>
              <div class="col-12">
                <h6>Images</h6>
                <div class="image-grid">
                  <div v-for="(image, index) in selectedDiaryEntry.images" 
                       :key="index" 
                       class="image-item">
                    <img :src="image" :alt="'Image ' + (index + 1)" class="img-thumbnail">
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="editSelectedDiaryEntry">Edit</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, defineEmits } from 'vue'
import { Modal } from 'bootstrap'
import api from '../utils/axios'

export default {
  name: 'AdminDashboard',
  emits: ['zoomToLocation'],
  setup(props, { emit }) {
    const reservations = ref([])
    const filteredReservations = ref([])
    const searchQuery = ref('')
    const editingReservation = ref(null)
    const deletingReservation = ref(null)
    const editModal = ref(null)
    const deleteModal = ref(null)
    const showToast = ref(false)
    const toastMessage = ref('')
    const toastType = ref('success')
    let toastTimeout = null
    const selectedReservation = ref(null)
    const bookingDetailsModal = ref(null)

    const activeTab = ref('hotels')
    const diaryEntries = ref([])
    const filteredDiaryEntries = ref([])
    const diarySearchQuery = ref('')
    const editingDiaryEntry = ref(null)
    const deletingDiaryEntry = ref(null)
    const selectedDiaryEntry = ref(null)
    const editDiaryModal = ref(null)
    const deleteDiaryModal = ref(null)
    const diaryDetailsModal = ref(null)

    const displayToast = (message, type = 'success') => {
      if (toastTimeout) {
        clearTimeout(toastTimeout)
      }
      toastMessage.value = message
      toastType.value = type
      showToast.value = true
      
      toastTimeout = setTimeout(() => {
        showToast.value = false
      }, 3000)
    }

    const loadReservations = async () => {
      try {
        console.log('Loading reservations...')
        const response = await api.get('/api/hotels')
        console.log('API Response:', response)
        
        if (!response?.data) {
          throw new Error('No data received from server')
        }
        
        if (Array.isArray(response.data)) {
          const mappedReservations = response.data.map(reservation => {
            // Handle both id and _id fields
            const reservationId = reservation._id || reservation.id
            if (!reservationId) {
              console.warn('Reservation missing id:', reservation)
              return null
            }
            
            return {
              ...reservation,
              _id: reservationId.toString(),
              check_in: reservation.check_in ? new Date(reservation.check_in).toISOString().split('T')[0] : '',
              check_out: reservation.check_out ? new Date(reservation.check_out).toISOString().split('T')[0] : '',
              status: reservation.status || 'confirmed',
              hotel_name: reservation.hotel_name || 'Unnamed Hotel',
              city: reservation.city || 'Unknown City',
              guest_name: reservation.guest_name || 'Unknown Guest',
              room_type: reservation.room_type || 'Standard Room',
              price_per_night: reservation.price_per_night || 0
            }
          }).filter(r => r !== null)
          
          console.log('Mapped reservations:', mappedReservations)
          reservations.value = mappedReservations
          filteredReservations.value = [...mappedReservations]
          
          if (mappedReservations.length === 0) {
            console.log('No valid reservations found in response')
            displayToast('No reservations found', 'info')
          } else {
            console.log(`Loaded ${mappedReservations.length} reservations`)
          }
        } else {
          console.error('Unexpected response format:', response.data)
          displayToast('Invalid data format received from server', 'error')
          reservations.value = []
          filteredReservations.value = []
        }
      } catch (error) {
        console.error('Error loading reservations:', error)
        const errorDetail = error.response?.data?.detail || error.message || 'Unknown error'
        console.error('Error details:', errorDetail)
        displayToast(`Failed to load reservations: ${errorDetail}`, 'error')
        reservations.value = []
        filteredReservations.value = []
      }
    }

    const filterReservations = () => {
      const query = searchQuery.value.toLowerCase().trim()
      if (!query) {
        filteredReservations.value = [...reservations.value]
        return
      }
      
      filteredReservations.value = reservations.value.filter(reservation => 
        (reservation.hotel_name || '').toLowerCase().includes(query) ||
        (reservation.city || '').toLowerCase().includes(query) ||
        (reservation.guest_name || '').toLowerCase().includes(query)
      )
    }

    const formatDate = (date) => {
      if (!date) return ''
      try {
        return new Date(date).toLocaleDateString()
      } catch (error) {
        console.error('Error formatting date:', date, error)
        return ''
      }
    }

    const getStatusClass = (status) => {
      const classes = {
        confirmed: 'badge bg-success',
        cancelled: 'badge bg-danger',
        completed: 'badge bg-secondary'
      }
      return classes[status] || 'badge bg-primary'
    }

    const formatPrice = (price) => {
      if (!price) return '0.00'
      return Number(price).toLocaleString('de-DE', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    }

    const editReservation = (reservation) => {
      // Create a copy of the reservation and ensure we keep the original id
      editingReservation.value = {
        ...reservation,
        id: reservation.id || reservation._id, // Keep the original id
        _id: reservation._id || reservation.id // Ensure we have _id for frontend consistency
      }
      
      // Convert dates to YYYY-MM-DD format for input[type="date"]
      if (editingReservation.value.check_in) {
        editingReservation.value.check_in = new Date(editingReservation.value.check_in).toISOString().split('T')[0]
      }
      if (editingReservation.value.check_out) {
        editingReservation.value.check_out = new Date(editingReservation.value.check_out).toISOString().split('T')[0]
      }
      
      new Modal(editModal.value).show()
    }

    const updateReservation = async () => {
      try {
        if (!editingReservation.value) {
          throw new Error('Invalid reservation data')
        }

        // Get the correct ID from the reservation
        const reservationId = editingReservation.value.id?.toString() || editingReservation.value._id?.toString()
        if (!reservationId) {
          throw new Error('Missing reservation ID')
        }

        // Create the update data object without ID fields
        const updateData = { ...editingReservation.value }
        delete updateData._id
        delete updateData.id

        // Convert dates to ISO strings for the backend
        if (updateData.check_in) {
          updateData.check_in = new Date(updateData.check_in).toISOString()
        }
        if (updateData.check_out) {
          updateData.check_out = new Date(updateData.check_out).toISOString()
        }

        console.log('Updating reservation:', { id: reservationId, data: updateData })
        
        const response = await api.put(
          `/api/hotels/${reservationId}`,
          updateData
        )

        if (response.status === 200) {
          // Update the local data with the response
          const updatedReservation = {
            ...response.data,
            _id: response.data.id || response.data._id,
            check_in: response.data.check_in ? new Date(response.data.check_in).toISOString().split('T')[0] : '',
            check_out: response.data.check_out ? new Date(response.data.check_out).toISOString().split('T')[0] : ''
          }
          
          // Update both arrays
          const updateArray = (arr) => {
            const index = arr.findIndex(r => 
              (r._id?.toString() === reservationId) || (r.id?.toString() === reservationId)
            )
            if (index !== -1) {
              arr[index] = updatedReservation
            }
          }
          
          updateArray(reservations.value)
          updateArray(filteredReservations.value)
          
          // Close the modal
          const modalInstance = Modal.getInstance(editModal.value)
          if (modalInstance) {
            modalInstance.hide()
          }
          
          // Show success message
          displayToast('Reservation updated successfully')
        }
      } catch (error) {
        console.error('Error updating reservation:', error)
        const errorMessage = error.response?.data?.detail || error.message || 'Unknown error'
        displayToast(`Error updating reservation: ${errorMessage}`, 'error')
      } finally {
        editingReservation.value = null
      }
    }

    const confirmDelete = (reservation) => {
      deletingReservation.value = reservation
      new Modal(deleteModal.value).show()
    }

    const deleteReservation = async () => {
      try {
        if (!deletingReservation.value) {
          throw new Error('No reservation selected for deletion')
        }

        // Get the correct ID from the reservation
        const reservationId = deletingReservation.value.id?.toString() || deletingReservation.value._id?.toString()
        if (!reservationId) {
          throw new Error('Missing reservation ID')
        }

        console.log('Deleting reservation:', { id: reservationId })
        
        const response = await api.delete(`/api/hotels/${reservationId}`)
        
        if (response.status === 200) {
          // Remove the deleted reservation from both arrays
          const removeFromArray = (arr) => {
            return arr.filter(r => 
              (r._id?.toString() !== reservationId) && 
              (r.id?.toString() !== reservationId)
            )
          }
          
          reservations.value = removeFromArray(reservations.value)
          filteredReservations.value = removeFromArray(filteredReservations.value)
          
          // Close the modal
          const modalInstance = Modal.getInstance(deleteModal.value)
          if (modalInstance) {
            modalInstance.hide()
          }
          
          // Show success message
          displayToast('Reservation deleted successfully')
        }
      } catch (error) {
        console.error('Error deleting reservation:', error)
        const errorMessage = error.response?.data?.detail || error.message || 'Unknown error'
        displayToast(`Error deleting reservation: ${errorMessage}`, 'error')
      } finally {
        deletingReservation.value = null
      }
    }

    const handleReservationClick = (reservation) => {
      selectedReservation.value = reservation
      new Modal(bookingDetailsModal.value).show()
    }

    const zoomToLocation = () => {
      if (selectedReservation.value?.latitude && selectedReservation.value?.longitude) {
        emit('zoomToLocation', {
          lat: parseFloat(selectedReservation.value.latitude),
          lng: parseFloat(selectedReservation.value.longitude),
          name: selectedReservation.value.hotel_name,
          zoom: 15
        })
      }
    }

    const editSelectedReservation = () => {
      if (selectedReservation.value) {
        editReservation(selectedReservation.value)
        const modalInstance = Modal.getInstance(bookingDetailsModal.value)
        if (modalInstance) {
          modalInstance.hide()
        }
      }
    }

    const loadDiaryEntries = async () => {
      try {
        const response = await api.get('/api/diary/entries')
        if (response?.data) {
          diaryEntries.value = response.data
          filteredDiaryEntries.value = [...response.data]
        }
      } catch (error) {
        console.error('Error loading diary entries:', error)
        displayToast('Failed to load diary entries', 'error')
      }
    }

    const filterDiaryEntries = () => {
      const query = diarySearchQuery.value.toLowerCase().trim()
      if (!query) {
        filteredDiaryEntries.value = [...diaryEntries.value]
        return
      }
      
      filteredDiaryEntries.value = diaryEntries.value.filter(entry => 
        entry.title.toLowerCase().includes(query) ||
        entry.location.name.toLowerCase().includes(query)
      )
    }

    const editDiaryEntry = (entry) => {
      editingDiaryEntry.value = { ...entry }
      new Modal(editDiaryModal.value).show()
    }

    const updateDiaryEntry = async () => {
      try {
        if (!editingDiaryEntry.value?._id) return
        
        const response = await api.put(
          `/api/diary/entries/${editingDiaryEntry.value._id}`,
          editingDiaryEntry.value
        )

        if (response.data) {
          const index = diaryEntries.value.findIndex(e => e._id === editingDiaryEntry.value._id)
          if (index !== -1) {
            diaryEntries.value[index] = response.data
            filterDiaryEntries()
          }

          new Modal(editDiaryModal.value).hide()
          displayToast('Diary entry updated successfully')
        }
      } catch (error) {
        console.error('Error updating diary entry:', error)
        displayToast('Failed to update diary entry', 'error')
      }
    }

    const confirmDeleteDiary = (entry) => {
      deletingDiaryEntry.value = entry
      new Modal(deleteDiaryModal.value).show()
    }

    const deleteDiaryEntry = async () => {
      try {
        if (!deletingDiaryEntry.value?._id) return

        await api.delete(`/api/diary/entries/${deletingDiaryEntry.value._id}`)
        
        diaryEntries.value = diaryEntries.value.filter(
          e => e._id !== deletingDiaryEntry.value._id
        )
        filterDiaryEntries()

        new Modal(deleteDiaryModal.value).hide()
        displayToast('Diary entry deleted successfully')
      } catch (error) {
        console.error('Error deleting diary entry:', error)
        displayToast('Failed to delete diary entry', 'error')
      }
    }

    const handleDiaryEntryClick = (entry) => {
      selectedDiaryEntry.value = entry
      new Modal(diaryDetailsModal.value).show()
    }

    const editSelectedDiaryEntry = () => {
      if (selectedDiaryEntry.value) {
        editDiaryEntry(selectedDiaryEntry.value)
        new Modal(diaryDetailsModal.value).hide()
      }
    }

    const removeDiaryImage = (index) => {
      if (editingDiaryEntry.value) {
        editingDiaryEntry.value.images.splice(index, 1)
      }
    }

    onMounted(async () => {
      await Promise.all([
        loadReservations(),
        loadDiaryEntries()
      ])

      // Set up periodic refresh
      const refreshInterval = setInterval(() => {
        if (activeTab.value === 'hotels') {
          loadReservations()
        } else {
          loadDiaryEntries()
        }
      }, 30000)

      // Clean up on unmount
      onUnmounted(() => {
        clearInterval(refreshInterval)
      })
    })

    return {
      reservations,
      filteredReservations,
      searchQuery,
      editingReservation,
      deletingReservation,
      editModal,
      deleteModal,
      showToast,
      toastMessage,
      toastType,
      formatDate,
      getStatusClass,
      filterReservations,
      editReservation,
      updateReservation,
      confirmDelete,
      deleteReservation,
      formatPrice,
      handleReservationClick,
      selectedReservation,
      bookingDetailsModal,
      zoomToLocation,
      editSelectedReservation,
      activeTab,
      diaryEntries,
      filteredDiaryEntries,
      diarySearchQuery,
      editingDiaryEntry,
      deletingDiaryEntry,
      selectedDiaryEntry,
      editDiaryModal,
      deleteDiaryModal,
      diaryDetailsModal,
      filterDiaryEntries,
      editDiaryEntry,
      updateDiaryEntry,
      confirmDeleteDiary,
      deleteDiaryEntry,
      handleDiaryEntryClick,
      editSelectedDiaryEntry,
      removeDiaryImage
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
}

.table th {
  white-space: nowrap;
}

.btn-group {
  gap: 0.5rem;
}

.badge {
  font-size: 0.875rem;
  padding: 0.5em 0.75em;
}

.custom-toast {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 15px 25px;
  border-radius: 4px;
  color: white;
  z-index: 9999;
  animation: slideIn 0.3s ease-out;
}

.custom-toast.success {
  background-color: #198754;
}

.custom-toast.error {
  background-color: #dc3545;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Optional: Add animation for toast disappearance */
.custom-toast.hiding {
  animation: slideOut 0.3s ease-in forwards;
}

@keyframes slideOut {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(100%);
    opacity: 0;
  }
}

.cursor-pointer {
  cursor: pointer;
}

.hover-highlight:hover {
  background-color: rgba(0, 123, 255, 0.1) !important;
}

.modal-body h6 {
  color: #495057;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #dee2e6;
}

.modal-body p {
  margin-bottom: 0.5rem;
}

.modal-body .badge {
  font-size: 0.875rem;
  padding: 0.5em 0.75em;
}

.nav-tabs {
  border-bottom: 2px solid #dee2e6;
}

.nav-tabs .nav-link {
  border: none;
  color: #6c757d;
  padding: 0.75rem 1.25rem;
  cursor: pointer;
}

.nav-tabs .nav-link:hover {
  border: none;
  color: #495057;
}

.nav-tabs .nav-link.active {
  border: none;
  color: #0d6efd;
  border-bottom: 2px solid #0d6efd;
  margin-bottom: -2px;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.image-item {
  position: relative;
}

.image-item img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 4px;
}

.image-item .btn-danger {
  position: absolute;
  top: 5px;
  right: 5px;
  padding: 2px 8px;
  font-size: 0.75rem;
}

.diary-content {
  white-space: pre-wrap;
  margin: 1rem 0;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}
</style> 