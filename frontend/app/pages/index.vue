<template>
  <div class="h-svh w-svw font-sans">
    <NavBar />
    <MainLayout>
      <section class="p-4">
        <h2 class="text-2xl font-bold mb-4">Bienvenido al Medidor de Humedad y CO2</h2>
        <p class="mb-2">Esta es la página principal de la aplicación para monitorear los niveles de humedad y CO2.</p>
        <p>
          <span class="font-bold">Niveles actuales de Humedad: </span>
          <span v-if="datos_humedad">{{ datos_humedad }}</span>
          <span v-else>No disponible</span>
        </p>
        <p class="mb-4">
          <span class="font-bold">Niveles actuales de CO2: </span>
          <span v-if="datos_co2">{{ datos_co2 }}</span>
          <span v-else>No disponible</span>
        </p>
        <button class="py-1 px-2 border rounded-lg cursor-pointer transition-colors hover:bg-slate-700 hover:text-white hover:border-white" @click="getHumidityData">
          Pedir datos de humedad
        </button>
        <button class="ml-4 py-1 px-2 border rounded-lg cursor-pointer transition-colors hover:bg-slate-700 hover:text-white hover:border-white" @click="getCO2Data">
          Pedir datos de CO2
        </button>
      </section>
    </MainLayout>
  </div>
</template>

<script setup lang="ts">
// Setup del titulo de la página
useHead({
  title: 'Medidor Humedad/CO2 - Home',
  meta: [
    { name: 'description', content: 'Página principal del Medidor de Humedad y CO2' }
  ]
})
import { ref } from 'vue'

const datos_humedad = ref<string>('')
const datos_co2 = ref<string>('')

const getHumidityData = async () => {
  // Fetch localhost:8000/api/humidity
  try {
    const response = await fetch('http://localhost:8000/api/humidity')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const json = await response.json()
  // Mostrar el campo "message" que devuelve el backend
  datos_humedad.value = String(json.message ?? '')
  } catch (error) {
    console.error('Error al obtener datos de humedad:', error)
  }
}

const getCO2Data = async () => {
  // Fetch localhost:8000/api/co2
  try {
    const response = await fetch('http://localhost:8000/api/co2')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const json = await response.json()
  // Mostrar el campo "message" que devuelve el backend
  datos_co2.value = String(json.message ?? '')
  } catch (error) {
    console.error('Error al obtener datos de CO2:', error)
  }
}

onMounted(() => {
  // Obtener datos iniciales al montar el componente
  getHumidityData()
  getCO2Data()
})
</script>