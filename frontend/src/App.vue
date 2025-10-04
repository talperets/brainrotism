<script setup lang="ts">
import LocationAR from './components/LocationAR.vue'
</script>

<template>
  <link href="/src/style.css" rel="stylesheet">
  <RouterView />
  <LocationAR />
</template>

<style>
#arjs-video {
  position: absolute !important;
  top: 0;
  left: 0;
  width: 100% !important;
  height: 100% !important;
  object-fit: cover;
  z-index: 0; /* behind AR objects but visible */
  margin: 0 !important;
}
</style>
