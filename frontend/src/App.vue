<template>
  <div id="app">
    <IntroAnimation v-if="showIntro" @animation-complete="showIntro = false" />
    <template v-else>
      <Navigation />
      <div class="container-fluid">
        <router-view></router-view>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import Navigation from './components/Navigation.vue'
import IntroAnimation from './components/IntroAnimation.vue'
import { shouldShowIntro } from './utils/cookies'

export default {
  name: 'App',
  components: {
    Navigation,
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
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.container-fluid {
  flex: 1;
  padding: 1rem;
}

body {
  margin: 0;
  padding: 0;
  background-color: #f8f9fa;
}
</style>
