<template>
  <form @submit.prevent="onSubmit" style="margin-top:20px;">
    <div>
      <label>Movie ID:</label>
      <input v-model.number="form.movie_id" type="number" required class="w-full border border-gray-600 rounded px-3 py-2 text-black placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-400"/>
    </div>
    <button style="margin: 20px" class=" max-w-md mx-auto mt-10 space-y-6 bg-green-500 hover:bg-green-600 active:bg-green-700 text-white font-bold py-2 px-6 rounded transition duration-150" type="submit">Consultar</button>
  </form>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

const emit = defineEmits(['submit'])
const form = reactive({
  movie_id: '',
  customer_name: ''
})

function onSubmit() {
  emit('submit', { ...form })
  form.movie_id = ''
  form.customer_name = ''
}
</script>
