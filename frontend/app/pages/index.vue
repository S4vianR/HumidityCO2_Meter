<template>
  <div class="h-svh w-svw font-sans">
    <NavBar />
    <MainLayout>
      <section class="min-w-full min-h-11/12 flex flex-col justify-center items-center">
        <h2 class="text-2xl font-bold text-center my-4">
          Bienvenido al Medidor de Humedad y Gas
        </h2>
        <BentoGrid :cards="cards" :temp-series="tempSeries" :hum-series="humSeries" :gas-series="gasSeries" />
      </section>
    </MainLayout>
  </div>
</template>

<script setup lang="ts">
const RPI_URL = 'https://sensor.rubr.xyz' as string

// Setup del titulo de la página
useHead({
  title: 'Medidor Humedad/Gas - Home',
  meta: [
    { name: 'description', content: 'Página principal del Medidor de Humedad y Gas' }
  ]
})
import { ref, onMounted, computed } from 'vue'
import { useSamples } from '@/composables/samples'
import type { Sample } from '@/composables/samples'

const { chartSamples, gasSamples } = useSamples()

const datos_humedad = ref<string>('')
const datos_temperatura = ref<string>('')
const datos_gas = ref<string>('')
const MAX_SAMPLES = 100

// Lee ambos valores (temperatura y humedad) desde el mismo endpoint
const getDHT11Data = async () => {
  console.log('Obteniendo datos DHT11...')
  try {
    const response = await fetch(`${RPI_URL}/api/dht11`)
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
    const json = await response.json()
    console.log('Respuesta DHT11 recibida:', json)
    const payload = json?.message ?? json
    const tempVal = Number(payload?.temperatura ?? NaN)
    const humVal = Number(payload?.humedad ?? NaN)
    datos_temperatura.value = Number.isFinite(tempVal) ? String(tempVal) + '°C' : ''
    datos_humedad.value = Number.isFinite(humVal) ? String(humVal) + '%' : ''

    if (Number.isFinite(tempVal) && Number.isFinite(humVal)) {
      chartSamples.value.push({ time: new Date().toISOString(), temperatura: tempVal, humedad: humVal })
      if (chartSamples.value.length > MAX_SAMPLES) chartSamples.value.shift()
    }
  } catch (error) {
    console.error('Error al obtener datos de DHT11 (temp/humedad):', error)
    datos_humedad.value = ''
    datos_temperatura.value = ''
  }
}

const getGasData = async () => {
  try {
    const response = await fetch(`${RPI_URL}/api/gas`)
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
    const json = await response.json()
    const val = Number(json.message ?? NaN)
    datos_gas.value = String(json.message ?? '')
    if (Number.isFinite(val)) {
      gasSamples.value.push(val)
      if (gasSamples.value.length > MAX_SAMPLES) gasSamples.value.shift()
    }
  } catch (error) {
    console.error('Error al obtener datos de Gas:', error)
    datos_gas.value = ''
  }
}

onMounted(() => {
  // petición inicial y luego polling cada 5 minutos
  getDHT11Data()
  getGasData()
  setInterval(() => {
    getDHT11Data()
    getGasData()
  }, 300000)
})

const tempSeries = computed(() => chartSamples.value.map((s: Sample) => s.temperatura))
const humSeries = computed(() => chartSamples.value.map((s: Sample) => s.humedad))
const gasSeries = computed(() => gasSamples.value.slice())

// Computed cards para el BentoGrid — reactivo a los valores actuales
const cards = computed(() => {
  const now = new Date()
  return [
    { id: 'temp', title: 'Temperatura', subtitle: 'Sensor A', value: datos_temperatura.value || '—', cols: 3, rows: 2, route: '/temp' },
    { id: 'hum', title: 'Humedad', subtitle: 'Sensor A', value: datos_humedad.value || '—', cols: 3, rows: 2, route: '/hum' },
    { id: 'gas', title: 'Gas', subtitle: 'Sensor B', value: datos_gas.value || '—', cols: 3, rows: 2, route: '/gas' },
    { id: 'last', title: 'Última actualización', value: now.toLocaleTimeString(), cols: 2, rows: 1 },
    { id: 'conn', title: 'Conexión', value: 'OK', cols: 2, rows: 1 },
    { id: 'summary', title: 'Resumen', value: 'Normal', cols: 2, rows: 1 }
  ]
})
</script>
