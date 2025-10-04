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
  const krakowCenter = [19.9450, 50.0647];

  map = new mapboxgl.Map({
    container: container,
    style: 'mapbox://styles/ixapa/cmgcjb7lt00ew01pde8lja121',
    center: krakowCenter,
    zoom: 12,
  })

  for (let i = 0; i < 10; i++) {
    const randomLng = krakowCenter[0] + (Math.random() - 0.5) * 0.05;
    const randomLat = krakowCenter[1] + (Math.random() - 0.5) * 0.05;

    const el = document.createElement('div');
    el.className = 'character';
    el.style.backgroundImage = 'url(/vite.svg)';
    el.style.width = '40px';
    el.style.height = '40px';
    el.style.backgroundSize = 'cover';

    new mapboxgl.Marker(el).setLngLat([randomLng, randomLat]).addTo(map);
  }

  const geoControl = new mapboxgl.GeolocateControl({
    positionOptions: { enableHighAccuracy: true },
    trackUserLocation: true,
    showUserHeading: true
  });
  map.addControl(geoControl);
  map.on('load', () => geoControl.trigger());
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
