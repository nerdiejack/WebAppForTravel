<template>
  <div class="diary-display-container">
    <!-- Back to Map Button -->
    <button class="back-to-map-btn" @click="handleBackToMap">
      <i class="fas fa-map-marked-alt me-2"></i>Back to Map
    </button>

    <!-- Entry Header -->
    <div class="entry-header">
      <h1>{{ entry.title }}</h1>
      <div class="entry-meta">
        <span class="location">
          <i class="fas fa-map-marker-alt me-2"></i>{{ entry.location.name }}
        </span>
        <span class="date">
          <i class="fas fa-calendar me-2"></i>{{ formatDate(entry.created_at) }}
        </span>
      </div>
    </div>

    <!-- Image Gallery -->
    <div v-if="entry.images.length > 0" class="image-gallery">
      <!-- Fullscreen Gallery Modal -->
      <div class="modal fade" id="galleryModal" tabindex="-1" ref="galleryModal">
        <div class="modal-dialog modal-fullscreen">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Gallery</h5>
              <button type="button" class="btn-close" @click="closeGallery"></button>
            </div>
            <div class="modal-body gallery-modal-body">
              <div class="fullscreen-gallery">
                <img :src="currentImage" :alt="entry.title" class="fullscreen-image">
                <button v-if="entry.images.length > 1" class="gallery-nav prev" @click="previousImage">
                  <i class="fas fa-chevron-left"></i>
                </button>
                <button v-if="entry.images.length > 1" class="gallery-nav next" @click="nextImage">
                  <i class="fas fa-chevron-right"></i>
                </button>
              </div>
              <div class="gallery-thumbnails fullscreen">
                <div 
                  v-for="(image, index) in entry.images" 
                  :key="index"
                  class="thumbnail"
                  :class="{ active: currentImageIndex === index }"
                  @click="setCurrentImage(index)"
                >
                  <img :src="image" :alt="`Thumbnail ${index + 1}`">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Gallery Preview -->
      <div class="gallery-main" @click="openGallery">
        <img :src="currentImage" :alt="entry.title" class="main-image">
        <div class="gallery-overlay">
          <i class="fas fa-expand"></i>
          <span>View Gallery</span>
        </div>
        <button v-if="entry.images.length > 1" class="gallery-nav prev" @click.stop="previousImage">
          <i class="fas fa-chevron-left"></i>
        </button>
        <button v-if="entry.images.length > 1" class="gallery-nav next" @click.stop="nextImage">
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
      <div v-if="entry.images.length > 1" class="gallery-thumbnails">
        <div 
          v-for="(image, index) in entry.images" 
          :key="index"
          class="thumbnail"
          :class="{ active: currentImageIndex === index }"
          @click="setCurrentImage(index)"
        >
          <img :src="image" :alt="`Thumbnail ${index + 1}`">
        </div>
      </div>
    </div>

    <!-- Entry Content -->
    <div class="entry-content">
      <p>{{ entry.content }}</p>
    </div>

    <!-- Entry Footer -->
    <div class="entry-footer">
      <button class="btn btn-primary" @click="$emit('edit', entry)">
        <i class="fas fa-edit me-2"></i>Edit Entry
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { Modal } from 'bootstrap'

export default {
  name: 'DiaryEntryDisplay',
  props: {
    entry: {
      type: Object,
      required: true
    }
  },
  setup(props, { emit }) {
    const currentImageIndex = ref(0)
    const currentImage = ref(props.entry.images[0] || '')
    const galleryModal = ref(null)

    const setCurrentImage = (index) => {
      currentImageIndex.value = index
      currentImage.value = props.entry.images[index]
    }

    const nextImage = () => {
      const nextIndex = (currentImageIndex.value + 1) % props.entry.images.length
      setCurrentImage(nextIndex)
    }

    const previousImage = () => {
      const prevIndex = currentImageIndex.value - 1 < 0 
        ? props.entry.images.length - 1 
        : currentImageIndex.value - 1
      setCurrentImage(prevIndex)
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const openGallery = () => {
      new Modal(galleryModal.value).show()
    }

    const closeGallery = () => {
      const modalInstance = Modal.getInstance(galleryModal.value)
      if (modalInstance) {
        modalInstance.hide()
      }
    }

    const handleBackToMap = () => {
      emit('back-to-map')
    }

    onMounted(() => {
      galleryModal.value = document.getElementById('galleryModal')
    })

    return {
      currentImageIndex,
      currentImage,
      setCurrentImage,
      nextImage,
      previousImage,
      formatDate,
      openGallery,
      closeGallery,
      handleBackToMap
    }
  }
}
</script>

<style scoped>
.diary-display-container {
  position: relative;
  height: 100%;
  padding: 2rem;
  overflow-y: auto;
  background: white;
}

.back-to-map-btn {
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
  transition: all 0.2s ease;
  z-index: 10;
}

.back-to-map-btn:hover {
  background: #007bff;
  color: white;
}

.entry-header {
  margin-bottom: 2rem;
  padding-right: 120px; /* Space for back button */
}

.entry-header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.entry-meta {
  display: flex;
  gap: 2rem;
  color: #6c757d;
  font-size: 1.1rem;
}

.image-gallery {
  margin-bottom: 2rem;
}

.gallery-main {
  position: relative;
  width: 100%;
  height: 500px;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.gallery-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0;
  transition: opacity 0.3s ease;
  cursor: pointer;
}

.gallery-main:hover .gallery-overlay {
  opacity: 1;
}

.gallery-overlay i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.fullscreen-gallery {
  position: relative;
  height: calc(100vh - 200px);
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000;
}

.fullscreen-image {
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}

.gallery-modal-body {
  padding: 0;
  background: #000;
}

.gallery-thumbnails.fullscreen {
  background: #000;
  padding: 1rem;
  margin: 0;
}

.gallery-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.9);
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 10;
}

.gallery-nav:hover {
  background: white;
  transform: translateY(-50%) scale(1.1);
}

.gallery-nav.prev {
  left: 20px;
}

.gallery-nav.next {
  right: 20px;
}

.gallery-thumbnails {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  padding-bottom: 1rem;
  scrollbar-width: thin;
  scrollbar-color: #007bff #f8f9fa;
}

.gallery-thumbnails::-webkit-scrollbar {
  height: 6px;
}

.gallery-thumbnails::-webkit-scrollbar-track {
  background: #f8f9fa;
}

.gallery-thumbnails::-webkit-scrollbar-thumb {
  background-color: #007bff;
  border-radius: 6px;
}

.thumbnail {
  flex: 0 0 100px;
  height: 100px;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  opacity: 0.7;
  transition: all 0.2s ease;
}

.thumbnail:hover {
  opacity: 0.9;
}

.thumbnail.active {
  opacity: 1;
  box-shadow: 0 0 0 2px #007bff;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.modal-header {
  background: #000;
  border-bottom: 1px solid #333;
}

.modal-header .modal-title {
  color: white;
}

.modal-header .btn-close {
  filter: invert(1) grayscale(100%) brightness(200%);
}

.entry-content {
  font-size: 1.2rem;
  line-height: 1.8;
  color: #2c3e50;
  margin-bottom: 2rem;
  white-space: pre-wrap;
}

.entry-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 2rem;
  border-top: 1px solid #dee2e6;
}
</style> 