<template>
  <div class="movie-card" style="border:1px solid #ddd; padding:10px; margin:10px;">
    <h3>{{ title }}</h3>
    <p>{{ genre }} ({{ year }})</p>
  </div>
</template>

<script setup lang="ts">
defineProps({
  title: String,
  genre: String,
  year: Number
})
</script>
