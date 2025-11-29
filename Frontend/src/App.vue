<!-- src/App.vue -->
<template>
  <div id="app">
    <!-- Navbar solo si la ruta NO indica hideNavbar -->
    <MainNavbar v-if="!$route.meta.hideNavbar" />

    <!-- Si hideNavbar = true, se elimina el padding -->
    <main class="main-content" :class="{ 'no-padding': $route.meta.hideNavbar }">
      <router-view />
    </main>
  </div>
</template>

<script>
import MainNavbar from './components/MainNavbar.vue'

export default {
  name: 'App',
  components: { MainNavbar }
}
</script>

<style>

.no-padding {
  padding: 0 !important;
  padding-top: 0 !important;
  min-height: 100vh !important; /* asegura que ocupe toda la pantalla */
}

:root{
  --header-height: 64px;
  --bg: #f4f6f8;
  --card-bg: #ffffff;
  --accent: #0f6fff;
}

html, body, #app {
  height: 100%;
  margin: 0;
  font-family: Inter, Arial, sans-serif;
  background: var(--bg);
  color: #1f2937;
}

.main-content {
  padding: 24px;
  padding-top: calc(var(--header-height) + 16px); /* espacio cuando navbar existe */
  min-height: calc(100vh - var(--header-height));
  box-sizing: border-box;
}
</style>
