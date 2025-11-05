<template>
  <div class="h-svh w-svw font-sans">
    <NavBar />
    <MainLayout>
      <section class="min-w-full min-h-11/12 flex flex-col justify-center items-center">
        <h2 class="text-2xl font-bold text-center my-4">
          Bienvenido al Medidor de Humedad y Gas
        </h2>
        <BentoGrid :cards="cards" />
      </section>
    </MainLayout>
  </div>
</template>

<script setup lang="ts">
// Setup del titulo de la página
useHead({
  title: 'Medidor Humedad/Gas - Home',
  meta: [
    { name: 'description', content: 'Página principal del Medidor de Humedad y Gas' }
  ]
})
import { ref, onMounted, computed } from 'vue'

const datos_humedad = ref<string>('')
const datos_gas = ref<string>('')

const getHumidityData = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/humidity')
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
    const json = await response.json()
    datos_humedad.value = String(json.message ?? '')
  } catch (error) {
    console.error('Error al obtener datos de humedad:', error)
    datos_humedad.value = ''
  }
}

const getGasData = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/gas')
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
    const json = await response.json()
    datos_gas.value = String(json.message ?? '')
  } catch (error) {
    console.error('Error al obtener datos de Gas:', error)
    datos_gas.value = ''
  }
}

onMounted(() => {
  getHumidityData()
  getGasData()
  setInterval(() => {
    getHumidityData()
    getGasData()
  }, 300000)
})

// Computed cards para el BentoGrid — reactivo a los valores actuales
const cards = computed(() => {
  const now = new Date()
  return [
    { id: 'hum', title: 'Humedad', subtitle: 'Sensor A', value: datos_humedad.value || '—', cols: 3, rows: 2 },
    { id: 'gas', title: 'Gas', subtitle: 'Sensor B', value: datos_gas.value || '—', cols: 3, rows: 2 },
    { id: 'last', title: 'Última actualización', value: now.toLocaleTimeString(), cols: 2, rows: 1 },
    { id: 'conn', title: 'Conexión', value: 'OK', cols: 2, rows: 1 },
    { id: 'summary', title: 'Resumen', value: 'Normal', cols: 2, rows: 1 }
  ]
})
</script>