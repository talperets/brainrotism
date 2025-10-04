<script lang="ts">
import Character from '../components/Character.vue';
</script>

<template>
<h1>Characters</h1>

<Character v-for="x in [1,2,3,4]"/>

</template>