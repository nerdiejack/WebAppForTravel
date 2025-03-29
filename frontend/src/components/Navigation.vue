<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">Travel App</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav w-100">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/hotels">Hotels</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/diary">Travel Diary</router-link>
          </li>
          <li class="nav-item ms-lg-auto">
            <router-link class="nav-link" to="/admin">Admin</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { onMounted } from 'vue'
import { Collapse } from 'bootstrap'

export default {
  name: 'Navigation',
  setup() {
    onMounted(() => {
      // Initialize Bootstrap collapse
      const navbarToggler = document.querySelector('.navbar-toggler')
      if (navbarToggler) {
        new Collapse(navbarToggler)
      }
    })
  }
}
</script>

<style scoped>
.navbar {
  margin-bottom: 1rem;
}

.navbar-brand {
  font-weight: bold;
}

.nav-link {
  font-size: 1.1rem;
}

.nav-link.router-link-active {
  color: #fff !important;
  font-weight: bold;
}

/* Ensure admin link is pushed to the right */
@media (min-width: 992px) {
  .ms-lg-auto {
    margin-left: auto !important;
  }
}

/* Ensure navbar items are properly spaced in mobile view */
@media (max-width: 991.98px) {
  .navbar-nav {
    padding: 1rem 0;
  }
  
  .nav-item {
    padding: 0.5rem 0;
  }
}
</style>