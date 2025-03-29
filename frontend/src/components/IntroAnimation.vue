<template>
  <div class="intro-animation">
    <div class="image-slider">
      <div v-for="(image, index) in images" 
           :key="index"
           class="slide"
           :class="{ 
             active: currentIndex === index,
             'slide-out': currentIndex === index - 1,
             'slide-in': currentIndex === index
           }"
           :style="{ backgroundImage: `url(${image.url})` }">
        <div class="slide-content" :class="{ 'content-visible': currentIndex === index }">
          <h2>{{ image.title }}</h2>
          <p>{{ image.location }}</p>
        </div>
      </div>
    </div>
    <div class="progress-bar">
      <div class="progress" :style="{ width: `${progress}%` }"></div>
    </div>
    <div v-if="showBookAnimation" class="book-animation">
      <div class="book-page left"></div>
      <div class="book-page right"></div>
      <div class="book-content">
        <div class="explorer-text">
          <span>L</span>
          <span>E</span>
          <span>T</span>
          <span>'</span>
          <span>S</span>
        </div>
        <div class="explorer-text">
          <span>G</span>
          <span>O</span>
        </div>
        <div class="explorer-text">
          <span>E</span>
          <span>X</span>
          <span>P</span>
          <span>L</span>
          <span>O</span>
          <span>R</span>
          <span>E</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import angkorWat from '../assets/images/thailand/angkor-wat.jpg'
import angkorThom from '../assets/images/thailand/angkor-thom.jpg'
import elephantSanctuary from '../assets/images/thailand/elephant-sanctuary.jpg'
import khaoYaiHornbill from '../assets/images/thailand/khao_yai_hornbill.jpg'
import kuangSiFalls from '../assets/images/thailand/kuang-si-falls.jpg'
import luangPrabang from '../assets/images/thailand/luang_prabang.jpg'
import plainOfJars from '../assets/images/thailand/plain-of-jars.jpg'
import railayBeach from '../assets/images/thailand/railay-beach.jpg'
import vangVieng from '../assets/images/thailand/vang_vieng.jpg'
import watArun from '../assets/images/thailand/wat_arun.jpg'

export default {
  name: 'IntroAnimation',
  setup(props, { emit }) {
    const currentIndex = ref(0)
    const progress = ref(0)
    const showBookAnimation = ref(false)
    let progressInterval
    let slideInterval

    const images = [
      { url: angkorWat, title: 'Angkor Wat', location: 'Siem Reap, Cambodia' },
      { url: angkorThom, title: 'Angkor Thom', location: 'Siem Reap, Cambodia' },
      { url: elephantSanctuary, title: 'Elephant Sanctuary', location: 'Chiang Mai, Thailand' },
      { url: khaoYaiHornbill, title: 'Khao Yai National Park', location: 'Thailand' },
      { url: kuangSiFalls, title: 'Kuang Si Falls', location: 'Luang Prabang, Laos' },
      { url: luangPrabang, title: 'Luang Prabang', location: 'Laos' },
      { url: plainOfJars, title: 'Plain of Jars', location: 'Xieng Khouang, Laos' },
      { url: railayBeach, title: 'Railay Beach', location: 'Krabi, Thailand' },
      { url: vangVieng, title: 'Vang Vieng', location: 'Laos' },
      { url: watArun, title: 'Wat Arun', location: 'Bangkok, Thailand' }
    ]

    const updateProgress = () => {
      progress.value += (100 / (15 * 60)) // 15 seconds total
      if (progress.value >= 100) {
        showBookAnimation.value = true
        setTimeout(() => {
          emit('animation-complete')
        }, 2000) // Wait for book animation to complete
      }
    }

    const nextSlide = () => {
      currentIndex.value = (currentIndex.value + 1) % images.length
    }

    onMounted(() => {
      progressInterval = setInterval(updateProgress, 1000 / 60) // 60fps
      slideInterval = setInterval(nextSlide, 2500) // Change slide every 2.5 seconds
    })

    onUnmounted(() => {
      clearInterval(progressInterval)
      clearInterval(slideInterval)
    })

    return {
      currentIndex,
      progress,
      showBookAnimation,
      images
    }
  }
}
</script>

<style scoped>
.intro-animation {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #000;
  z-index: 9999;
  overflow: hidden;
}

.image-slider {
  position: relative;
  width: 100%;
  height: 100%;
}

.slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  opacity: 0;
  transform: scale(1.1);
  transition: opacity 1.5s ease-in-out, transform 1.5s ease-in-out;
}

.slide.active {
  opacity: 1;
  transform: scale(1);
}

.slide-out {
  opacity: 0;
  transform: scale(0.95);
}

.slide-in {
  opacity: 1;
  transform: scale(1);
}

.slide-content {
  position: absolute;
  bottom: 20%;
  left: 10%;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  transform: translateY(30px);
  opacity: 0;
  transition: all 1.5s ease-in-out;
}

.slide-content.content-visible {
  transform: translateY(0);
  opacity: 1;
}

.slide-content h2 {
  font-size: 3.5rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.slide-content p {
  font-size: 1.8rem;
  font-weight: 300;
}

.progress-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background-color: rgba(255, 255, 255, 0.2);
  z-index: 10000;
}

.progress {
  height: 100%;
  background-color: white;
  transition: width 0.1s linear;
}

.book-animation {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 10001;
  pointer-events: none;
  background-image: v-bind('`url(${images[0].url})`');
  background-size: cover;
  background-position: center;
}

.book-page {
  position: absolute;
  top: 0;
  width: 50%;
  height: 100%;
  background-color: #1a1a1a;
  transform-origin: center;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
}

.book-page.left {
  left: 0;
  transform: perspective(1500px) rotateY(-180deg);
  animation: openLeft 1s ease-in-out forwards;
}

.book-page.right {
  right: 0;
  transform: perspective(1500px) rotateY(180deg);
  animation: openRight 1s ease-in-out forwards;
}

.book-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  z-index: 10002;
  opacity: 0;
  animation: fadeInText 0.5s ease-in-out 0.5s forwards;
}

.explorer-text {
  margin: 0.5rem 0;
  font-family: 'Playfair Display', serif;
  font-size: 4rem;
  font-weight: 700;
  color: #fff;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.explorer-text span {
  display: inline-block;
  opacity: 0;
  transform: translateY(20px);
  animation: letterReveal 0.5s ease-out forwards;
}

.explorer-text:nth-child(1) span {
  animation-delay: 0.1s;
}

.explorer-text:nth-child(2) span {
  animation-delay: 0.3s;
}

.explorer-text:nth-child(3) span {
  animation-delay: 0.5s;
}

@keyframes letterReveal {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInText {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes openLeft {
  from {
    transform: perspective(1500px) rotateY(-180deg);
  }
  to {
    transform: perspective(1500px) rotateY(0deg);
  }
}

@keyframes openRight {
  from {
    transform: perspective(1500px) rotateY(180deg);
  }
  to {
    transform: perspective(1500px) rotateY(0deg);
  }
}
</style> 