<template>
  <div class="home">
    <div class="jumbotron text-center">
      <h1 class="display-4">Welcome to Travel App</h1>
      <p class="lead">Your all-in-one travel companion for managing hotels and documenting your journey.</p>
    </div>

    <div class="row">
      <div class="col-md-6 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">Hotel Reservations</h5>
            <p class="card-text">Manage your hotel bookings, view locations on a map, and keep track of your stays.</p>
            <router-link to="/hotels" class="btn btn-primary">Go to Hotels</router-link>
          </div>
        </div>
      </div>

      <div class="col-md-6 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">Travel Diary</h5>
            <p class="card-text">Document your travel experiences, add photos, and mark special locations on the map.</p>
            <router-link to="/diary" class="btn btn-primary">Go to Travel Diary</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
.home {
  padding: 2rem 0;
}

.jumbotron {
  background-color: #f8f9fa;
  padding: 4rem 2rem;
  margin-bottom: 2rem;
  border-radius: 0.5rem;
}

.display-4 {
  margin-bottom: 1rem;
}

.card {
  transition: transform 0.2s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card:hover {
  transform: translateY(-5px);
}

.card-title {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.card-text {
  color: #6c757d;
  margin-bottom: 1.5rem;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}
</style> 