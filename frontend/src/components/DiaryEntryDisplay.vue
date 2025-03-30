<template>
  <div class="diary-entry-display">
    <!-- Left side: Text content -->
    <div class="content-column">
      <div class="entry-header">
        <button class="back-btn" @click="$emit('back-to-map')">
          <i class="fas fa-arrow-left"></i> Back to Map
        </button>
        <div class="action-buttons">
          <button class="edit-btn" @click="$emit('edit', entry)">
            <i class="fas fa-edit"></i> Edit Entry
          </button>
          <button class="delete-btn" @click="confirmDelete">
            <i class="fas fa-trash"></i> Delete
          </button>
        </div>
      </div>

      <div class="entry-title">
        <h2>{{ entry.title }}</h2>
        <div class="entry-meta">
          <div class="location-info">
            <i class="fas fa-map-marker-alt"></i>
            <span>{{ entry.location.name }}</span>
          </div>

          <div class="date-info">
            <i class="fas fa-calendar"></i>
            <span>{{ formatDate(entry.created_at) }}</span>
          </div>
        </div>
      </div>

      <div class="entry-content">
        <div class="content-text">
          {{ entry.content }}
        </div>
      </div>
    </div>

    <!-- Right side: Images -->
    <div v-if="entry.images && entry.images.length > 0" class="images-column">
      <div class="images-grid">
        <div 
          v-for="(image, index) in entry.images" 
          :key="index"
          class="image-item"
          @click="openGallery(index)"
        >
          <img :src="image" :alt="'Image ' + (index + 1)">
        </div>
      </div>
    </div>

    <!-- Use the ImageGallery component -->
    <image-gallery
      :show="showGallery"
      :images="entry.images"
      :start-index="currentImageIndex"
      @close="closeGallery"
    />
  </div>
</template>

<script>
import { ref } from 'vue'
import ImageGallery from './ImageGallery.vue'
import api from '../utils/axios'

export default {
  name: 'DiaryEntryDisplay',
  components: {
    ImageGallery
  },
  props: {
    entry: {
      type: Object,
      required: true
    }
  },
  emits: ['back-to-map', 'edit', 'entry-deleted'],
  setup(props, { emit }) {
    const showGallery = ref(false)
    const currentImageIndex = ref(0)

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString()
    }

    const openGallery = (index) => {
      currentImageIndex.value = index
      showGallery.value = true
    }

    const closeGallery = () => {
      showGallery.value = false
    }

    const confirmDelete = async () => {
      if (confirm('Are you sure you want to delete this diary entry? This will also delete all associated images.')) {
        try {
          await api.delete(`/api/diary/entries/${props.entry._id}`)
          emit('entry-deleted')
          emit('back-to-map')
        } catch (error) {
          console.error('Error deleting diary entry:', error)
          alert('Failed to delete diary entry. Please try again.')
        }
      }
    }

    return {
      showGallery,
      currentImageIndex,
      formatDate,
      openGallery,
      closeGallery,
      confirmDelete
    }
  }
}
</script>

<style scoped>
.diary-entry-display {
  height: 100%;
  background: white;
  display: grid;
  grid-template-columns: 65% 35%; /* Text takes 65%, images take 35% */
  gap: 0;
}

.content-column {
  padding: 2rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  border-right: 1px solid #eee;
}

.entry-header {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.entry-title {
  text-align: left;
}

.entry-title h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.entry-meta {
  display: flex;
  gap: 2rem;
  color: #64748b;
}

.entry-content {
  flex: 1;
}

.content-text {
  white-space: pre-wrap;
  line-height: 1.8;
  color: #334155;
  font-size: 1.1rem;
}

.images-column {
  padding: 2rem;
  overflow-y: auto;
  background: #f8f9fa;
  display: flex;
  justify-content: center;
  align-items: start;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  width: 100%;
  max-width: 400px;
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

.back-btn, .edit-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
  font-weight: 500;
}

.back-btn {
  background: #f1f5f9;
  color: #475569;
}

.edit-btn {
  background: #2196F3;
  color: white;
}

.back-btn:hover {
  background: #e2e8f0;
}

.edit-btn:hover {
  background: #1976D2;
}

.action-buttons {
  display: flex;
  gap: 1rem;
}

.delete-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
  font-weight: 500;
  background: #dc3545;
  color: white;
}

.delete-btn:hover {
  background: #bb2d3b;
}

@media (max-width: 991px) {
  .diary-entry-display {
    grid-template-columns: 1fr;
  }

  .content-column {
    border-right: none;
    border-bottom: 1px solid #eee;
  }

  .images-column {
    padding: 2rem;
  }

  .images-grid {
    max-width: 500px;
    gap: 1.5rem;
  }
}
</style> 