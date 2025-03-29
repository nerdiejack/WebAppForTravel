<template>
  <div id="app">
    <IntroAnimation v-if="showIntro" @animation-complete="showIntro = false" />
    <template v-else>
      <!-- Fixed Navigation Bar -->
      <nav class="navbar">
        <div class="navbar-brand">
          <router-link to="/" class="brand-link">
            <i class="fas fa-globe-americas"></i>
            Travel Journal
          </router-link>
        </div>
        <div class="navbar-menu">
          <router-link to="/diary" class="nav-link">
            <i class="fas fa-book-open"></i>
            <span>Travel Diary</span>
          </router-link>
          <router-link to="/hotels" class="nav-link">
            <i class="fas fa-hotel"></i>
            <span>Hotels</span>
          </router-link>
          <router-link to="/admin" class="nav-link admin-link">
            <i class="fas fa-cog"></i>
            <span>Admin</span>
          </router-link>
        </div>
      </nav>

      <!-- Scrollable Content Area -->
      <main class="main-content">
        <router-view></router-view>
      </main>
    </template>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import IntroAnimation from './components/IntroAnimation.vue'
import { shouldShowIntro } from './utils/cookies'

export default {
  name: 'App',
  components: {
    IntroAnimation
  },
  setup() {
    const showIntro = ref(false)

    onMounted(() => {
      showIntro.value = shouldShowIntro()
    })

    return {
      showIntro
    }
  }
}
</script>

<style>
/* Global styles */
:root {
  --navbar-height: 64px;
  --primary-color: #2196F3;
  --secondary-color: #64748b;
  --background-color: #f8f9fa;
  --hover-color: #1976D2;
  --admin-color: #9333ea;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
}

body {
  font-family: 'Roboto', sans-serif;
  line-height: 1.6;
  color: #333;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Fixed Navigation Bar */
.navbar {
  position: sticky;
  top: 0;
  z-index: 9999;
  height: var(--navbar-height);
  background: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: bold;
}

.brand-link {
  text-decoration: none;
  color: var(--primary-color);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 600;
  transition: color 0.2s;
}

.brand-link:hover {
  color: var(--hover-color);
}

.navbar-menu {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-link {
  text-decoration: none;
  color: var(--secondary-color);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.2s;
}

.nav-link:hover {
  color: var(--primary-color);
  background: rgba(33, 150, 243, 0.1);
}

.nav-link.router-link-active {
  color: var(--primary-color);
  background: rgba(33, 150, 243, 0.1);
}

.admin-link {
  color: var(--admin-color);
}

.admin-link:hover,
.admin-link.router-link-active {
  color: var(--admin-color);
  background: rgba(147, 51, 234, 0.1);
}

.nav-link i {
  font-size: 1.2rem;
}

/* Main Content Area */
.main-content {
  flex: 1;
  background-color: var(--background-color);
  position: relative;
}

/* Utility Classes */
.text-center {
  text-align: center;
}

.mb-3 {
  margin-bottom: 1rem;
}

.mt-3 {
  margin-top: 1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar {
    padding: 0 1rem;
  }

  .navbar-menu {
    gap: 0.5rem;
  }

  .nav-link {
    padding: 0.5rem;
  }

  .nav-link span {
    display: none;
  }
}
</style>
