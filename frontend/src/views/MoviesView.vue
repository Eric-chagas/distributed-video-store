<template>
  <div>
    <h1 class="text-2xl font-bold text-center">Consultar Filme</h1>
    <RentForm @submit="handleRent" />
    <div v-if="message" class="p-4 bg-gray-100 text-black rounded shadow text-center">{{ message }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import MovieCard from '../components/MovieCard.vue'
import { getMovies } from '../services/catalogueService'
import RentForm from '../components/RentForm.vue'

const movies = ref([])
const loading = ref(true)
const message = ref('')

async function handleRent(formData: FormData) {
  try {
    const response = await getMovies(formData)
    message.value = `Movie response: id = ${response.id}, title = ${response.title}, year = ${response.year}, genre = ${response.genre}`
  } catch (err) {
    message.value = `Error: ${err}`
  }
}
</script>
