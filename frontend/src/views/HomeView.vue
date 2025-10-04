<script setup>
import Character from '../components/Character.vue';

</script>
<template>
  <div>
    <p>xp</p>
    <p>Dollar</p>
    <RouterLink to="/settings">Settings</RouterLink>
  </div>
  <div><RouterLink to="/leaderboard">Leaderboard</RouterLink></div>
  <div>
    <RouterLink to="/library">Characters</RouterLink>
    <p>Top character </p>
    <p>quick change</p>
    <Character>Trallarero trallala</Character>
  </div>
</template>