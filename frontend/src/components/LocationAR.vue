<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isClient = ref(false)
const coords = ref<{ latitude: number; longitude: number } | null>(null)

onMounted(() => {
  isClient.value = true

  // Check if geolocation is available
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        coords.value = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        }
        console.log('Current GPS coords:', coords.value)
      },
      (err) => {
        console.warn('Could not get GPS:', err)
      },
      { enableHighAccuracy: true }
    )
  } else {
    console.warn('Geolocation is not available in this browser.')
  }
})
</script>

<template>
  <div v-if="isClient">
    <a-scene
      vr-mode-ui="enabled: false"
      embedded
      arjs="sourceType: webcam; trackingMethod: best; debugUIEnabled: false;"
    >
      <!-- GPS Camera -->
      <a-camera gps-camera rotation-reader></a-camera>

      <!-- AR object dynamically positioned at your current location -->
      <a-entity
        v-if="coords"
        :gps-entity-place="`latitude: ${coords.latitude}; longitude: ${coords.longitude};`"
        gltf-model="https://models.babylonjs.com/CornellBox/cornellBox.glb"
        scale="100 100 100"
        rotation="0 180 0"
      ></a-entity>
    </a-scene>
  </div>
</template>

<style scoped>

</style>
