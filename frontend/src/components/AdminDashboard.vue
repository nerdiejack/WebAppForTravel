<template>
  <div class="admin-dashboard">
    <div class="container-fluid py-4">
      <div class="row mb-4">
        <div class="col">
          <h2>Hotel Reservations Admin</h2>
        </div>
      </div>

      <!-- Search and Filter -->
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

      <!-- Reservations Table -->
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
            <tr v-for="reservation in filteredReservations" :key="reservation._id">
              <td>{{ reservation.hotel_name }}</td>
              <td>{{ reservation.city }}</td>
              <td>{{ reservation.guest_name }}</td>
              <td>{{ formatDate(reservation.check_in) }}</td>
              <td>{{ formatDate(reservation.check_out) }}</td>
              <td>{{ reservation.room_type }}</td>
              <td>${{ reservation.price_per_night }}</td>
              <td>
                <span :class="getStatusClass(reservation.status)">
                  {{ reservation.status }}
                </span>
              </td>
              <td>
                <div class="btn-group">
                  <button 
                    class="btn btn-sm btn-primary" 
                    @click="editReservation(reservation)"
                  >
                    Edit
                  </button>
                  <button 
                    class="btn btn-sm btn-danger" 
                    @click="confirmDelete(reservation)"
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
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
                  <label class="form-label">Price per Night</label>
                  <input type="number" class="form-control" v-model="editingReservation.price_per_night" required>
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
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { Modal } from 'bootstrap'
import api from '../utils/axios'

export default {
  name: 'AdminDashboard',
  setup() {
    const reservations = ref([])
    const filteredReservations = ref([])
    const searchQuery = ref('')
    const editingReservation = ref(null)
    const deletingReservation = ref(null)
    const editModal = ref(null)
    const deleteModal = ref(null)

    const loadReservations = async () => {
      try {
        const response = await api.get('/api/hotels')
        // Safely handle the reservation data and IDs
        reservations.value = response.data.map(reservation => {
          const id = reservation._id || reservation.id // Try both _id and id
          return {
            ...reservation,
            _id: id ? id.toString() : undefined // Only convert to string if id exists
          }
        }).filter(reservation => reservation._id) // Filter out any reservations without valid IDs
        filteredReservations.value = [...reservations.value]
      } catch (error) {
        console.error('Error loading reservations:', error)
        alert('Failed to load reservations. Please check the console for details.')
      }
    }

    const filterReservations = () => {
      const query = searchQuery.value.toLowerCase()
      filteredReservations.value = reservations.value.filter(reservation => 
        reservation.hotel_name.toLowerCase().includes(query) ||
        reservation.city.toLowerCase().includes(query) ||
        reservation.guest_name.toLowerCase().includes(query)
      )
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString()
    }

    const getStatusClass = (status) => {
      const classes = {
        confirmed: 'badge bg-success',
        cancelled: 'badge bg-danger',
        completed: 'badge bg-secondary'
      }
      return classes[status] || 'badge bg-primary'
    }

    const editReservation = (reservation) => {
      editingReservation.value = { ...reservation }
      // Convert dates to YYYY-MM-DD format for input[type="date"]
      editingReservation.value.check_in = new Date(reservation.check_in).toISOString().split('T')[0]
      editingReservation.value.check_out = new Date(reservation.check_out).toISOString().split('T')[0]
      new Modal(editModal.value).show()
    }

    const updateReservation = async () => {
      try {
        const response = await api.put(`/api/hotels/${editingReservation.value._id}`, editingReservation.value)
        const index = reservations.value.findIndex(r => r._id === response.data._id)
        if (index !== -1) {
          reservations.value[index] = response.data
          filterReservations()
        }
        new Modal(editModal.value).hide()
      } catch (error) {
        console.error('Error updating reservation:', error)
        alert('Failed to update reservation')
      }
    }

    const confirmDelete = (reservation) => {
      deletingReservation.value = reservation
      new Modal(deleteModal.value).show()
    }

    const deleteReservation = async () => {
      try {
        if (!deletingReservation.value || !deletingReservation.value._id) {
          throw new Error('Invalid reservation ID')
        }
        
        const id = deletingReservation.value._id.toString()
        const response = await api.delete(`/api/hotels/${id}`)
        
        if (response.status === 200) {
          // Remove the deleted reservation from both arrays
          reservations.value = reservations.value.filter(r => r._id !== id)
          filteredReservations.value = filteredReservations.value.filter(r => r._id !== id)
          new Modal(deleteModal.value).hide()
          alert('Reservation deleted successfully')
        }
      } catch (error) {
        console.error('Error deleting reservation:', error)
        const errorMessage = error.response?.data?.detail || error.message || 'Unknown error'
        alert(`Error deleting reservation: ${errorMessage}`)
      } finally {
        deletingReservation.value = null
      }
    }

    onMounted(() => {
      loadReservations()
    })

    return {
      filteredReservations,
      searchQuery,
      editingReservation,
      deletingReservation,
      editModal,
      deleteModal,
      formatDate,
      getStatusClass,
      filterReservations,
      editReservation,
      updateReservation,
      confirmDelete,
      deleteReservation
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
</style> 