<template>
  <div class="gallery-overlay" v-if="show" @click="closeGallery">
    <div class="gallery-content" @click.stop>
      <button class="close-btn" @click="closeGallery">×</button>
      
      <div class="gallery-main">
        <button class="nav-btn prev" @click="prevImage" v-if="images.length > 1 && currentIndex > 0">
          <i class="fas fa-chevron-left"></i>
        </button>
        
        <div class="main-image-container">
          <div class="image-wrapper">
            <img 
              :src="currentImage" 
              :alt="'Image ' + (currentIndex + 1)" 
              class="main-image"
              :class="{ 'landscape': isLandscape, 'portrait': !isLandscape }"
              @load="onImageLoad"
            >
          </div>
        </div>
        
        <button class="nav-btn next" @click="nextImage" v-if="images.length > 1 && currentIndex < images.length - 1">
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
      
      <div class="thumbnails" v-if="images.length > 1">
        <div class="thumbnails-container">
          <div 
            v-for="(image, index) in images" 
            :key="index"
            class="thumbnail"
            :class="{ active: index === currentIndex }"
            @click="setImage(index)"
          >
            <img :src="image" :alt="'Thumbnail ' + (index + 1)">
          </div>
        </div>
      </div>
      
      <div class="image-counter" v-if="images.length > 1">
        {{ currentIndex + 1 }} / {{ images.length }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  name: 'ImageGallery',
  props: {
    show: {
      type: Boolean,
      required: true
    },
    images: {
      type: Array,
      required: true
    },
    startIndex: {
      type: Number,
      default: 0
    }
  },
  
  setup(props, { emit }) {
    const currentIndex = ref(props.startIndex)
    const currentImage = ref(props.images[currentIndex.value])
    const isLandscape = ref(true)
    
    watch(() => props.show, (newValue) => {
      if (newValue) {
        // Prevent body scrolling when gallery is open
        document.body.style.overflow = 'hidden'
      } else {
        // Restore body scrolling when gallery is closed
        document.body.style.overflow = 'auto'
      }
    })
    
    watch(() => props.startIndex, (newValue) => {
      currentIndex.value = newValue
      currentImage.value = props.images[currentIndex.value]
    })
    
    const onImageLoad = (event) => {
      const img = event.target
      isLandscape.value = img.naturalWidth >= img.naturalHeight
    }
    
    const closeGallery = () => {
      emit('close')
    }
    
    const nextImage = () => {
      if (currentIndex.value < props.images.length - 1) {
        currentIndex.value++
        currentImage.value = props.images[currentIndex.value]
      }
    }
    
    const prevImage = () => {
      if (currentIndex.value > 0) {
        currentIndex.value--
        currentImage.value = props.images[currentIndex.value]
      }
    }
    
    const setImage = (index) => {
      currentIndex.value = index
      currentImage.value = props.images[index]
    }
    
    // Handle keyboard navigation
    const handleKeydown = (e) => {
      if (!props.show) return
      
      switch (e.key) {
        case 'ArrowLeft':
          prevImage()
          break
        case 'ArrowRight':
          nextImage()
          break
        case 'Escape':
          closeGallery()
          break
      }
    }
    
    // Add and remove keyboard event listeners
    watch(() => props.show, (newValue) => {
      if (newValue) {
        window.addEventListener('keydown', handleKeydown)
      } else {
        window.removeEventListener('keydown', handleKeydown)
      }
    })
    
    return {
      currentIndex,
      currentImage,
      isLandscape,
      closeGallery,
      nextImage,
      prevImage,
      setImage,
      onImageLoad
    }
  }
}
</script>

<style scoped>
.gallery-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.95);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.gallery-content {
  position: relative;
  width: 95%;
  height: 95%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.close-btn {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: white;
  font-size: 2.5rem;
  cursor: pointer;
  padding: 0.5rem;
  z-index: 1001;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.close-btn:hover {
  opacity: 1;
}

.gallery-main {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
  min-height: 0; /* Important for proper flex sizing */
}

.main-image-container {
  flex: 1;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.image-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

.main-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.main-image.landscape {
  width: 100%;
  height: auto;
}

.main-image.portrait {
  width: auto;
  height: 100%;
}

.nav-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  opacity: 0.8;
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  opacity: 1;
}

.nav-btn i {
  font-size: 1.5rem;
}

.thumbnails {
  padding: 1rem;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 8px;
}

.thumbnails-container {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  padding: 0.5rem;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
}

.thumbnails-container::-webkit-scrollbar {
  height: 6px;
}

.thumbnails-container::-webkit-scrollbar-track {
  background: transparent;
}

.thumbnails-container::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}

.thumbnail {
  flex: 0 0 80px;
  height: 80px;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  opacity: 0.6;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.thumbnail:hover {
  opacity: 0.8;
}

.thumbnail.active {
  opacity: 1;
  border-color: white;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-counter {
  position: absolute;
  bottom: -30px;
  left: 50%;
  transform: translateX(-50%);
  color: white;
  font-size: 0.9rem;
  opacity: 0.8;
}

@media (max-width: 768px) {
  .gallery-content {
    width: 100%;
    height: 100%;
  }

  .close-btn {
    top: 10px;
    right: 10px;
  }

  .nav-btn {
    width: 40px;
    height: 40px;
  }

  .thumbnail {
    flex: 0 0 60px;
    height: 60px;
  }

  .image-counter {
    bottom: 10px;
  }
}
</style> 