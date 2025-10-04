<template>
  <div id="map" class="map-container"></div>
</template>

<script setup>
import { onMounted, onBeforeUnmount } from 'vue'
import mapboxgl from 'mapbox-gl'
import { env } from 'process'

let map

onMounted(() => {
  const container = document.getElementById('map')
  if (!container) {
    console.error('Map container not found!')
    return
  }

  mapboxgl.accessToken = import.meta.env.VITE_MAP_TOKEN

  map = new mapboxgl.Map({
    container: container,
    style: 'mapbox://styles/mapbox/streets-v12',
    center: [19.9450, 50.0647],
    zoom: 13,
  })

  const el = document.createElement('div')
  el.className = 'character-marker'
  el.style.backgroundImage = 'url(/character.png)'
  el.style.width = '40px'
  el.style.height = '40px'
  el.style.backgroundSize = 'cover'

  new mapboxgl.Marker(el).setLngLat([6.5665, 52.2194]).addTo(map)
})

onBeforeUnmount(() => {
  if (map) map.remove()
})
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100vh;
}

.character-marker {
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.4);
}
</style>
