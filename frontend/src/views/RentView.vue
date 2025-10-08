<template>
  <div>
    <h1 class="text-2xl font-bold text-center">Consultar status de locação de Filme</h1>
    <RentForm @submit="handleRent" />
    <div v-if="message">{{ message }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import RentForm from '../components/RentForm.vue'
import { consultRentStatus } from '../services/rentService'

const message = ref('')

async function handleRent(formData: FormData) {
  try {
    const response = await consultRentStatus(formData)
    message.value = `Movie response: available = ${response.available}, status = ${response.status}`
  } catch (err) {
    message.value = `Error: ${err}`
  }
}
</script>
