<template>
  <div class="diary-entry-display">
    <div class="sticky-header">
      <div class="entry-header">
        <button class="back-btn" @click="$emit('back-to-map')">
          <i class="fas fa-arrow-left"></i> Back to Map
        </button>
        <button class="edit-btn" @click="$emit('edit', entry)">
          <i class="fas fa-edit"></i> Edit Entry
        </button>
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

      <!-- Images section moved to top and made sticky -->
      <div v-if="entry.images && entry.images.length > 0" class="sticky-images">
        <div class="images-container">
          <div class="images-grid">
            <div 
              v-for="(image, index) in entry.images" 
              :key="index"
              class="image-thumbnail"
              @click="openGallery(index)"
            >
              <img :src="image" :alt="'Image ' + (index + 1)">
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="scrollable-content">
      <div class="entry-content">
        <div class="content-text">
          {{ entry.content }}
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
  setup() {
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

    return {
      showGallery,
      currentImageIndex,
      formatDate,
      openGallery,
      closeGallery
    }
  }
}
</script>

<style scoped>
.diary-entry-display {
  height: 100%;
  background: white;
  display: flex;
  flex-direction: column;
  position: relative;
}

.sticky-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.entry-header {
  margin-top: 0;
  display: flex;
  justify-content: space-between;
  padding: 1rem 2rem;
  background: white;
  border-bottom: 1px solid #eee;
}

.entry-title {
  margin-top: 0;
  padding: 1.5rem 2rem;
  background: white;
  text-align: center;
  border-bottom: 1px solid #eee;
}

.entry-title h2 {
  font-size: 2rem;
  color: #1a1a1a;
  margin-bottom: 1rem;
}

.entry-meta {
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.sticky-images {
  margin-top: 0;
  padding: 1.5rem 2rem;
  background: white;
  border-bottom: 1px solid #eee;
}

.images-container {
  max-width: 1200px;
  margin: 0 auto;
}

.scrollable-content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  position: relative;
  z-index: 1;
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

.entry-content {
  max-width: 800px;
  margin: 0 auto;
}

.location-info, .date-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
}

.content-text {
  margin: 2rem 0;
  white-space: pre-wrap;
  line-height: 1.8;
  color: #334155;
  font-size: 1.1rem;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  justify-items: center;
}

.image-thumbnail {
  width: 180px;
  height: 180px;
  overflow: hidden;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.image-thumbnail:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.image-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

@media (max-width: 768px) {
  .entry-header,
  .entry-title,
  .sticky-images {
    padding: 1rem;
  }

  .entry-title h2 {
    font-size: 1.5rem;
  }

  .entry-meta {
    flex-direction: column;
    gap: 0.5rem;
    align-items: center;
  }

  .images-grid {
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  }

  .image-thumbnail {
    width: 140px;
    height: 140px;
  }
}
</style> 