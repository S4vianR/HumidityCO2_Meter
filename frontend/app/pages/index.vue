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

// Declaración reactiva para filas crudas de mediciones (evita el error "No se encuentra el nombre 'measurementsRows'")
const measurementsRows = ref<any[]>([])

const datos_humedad = ref<string>('')
const datos_temperatura = ref<string>('')
const datos_gas = ref<string>('')
const MAX_SAMPLES = 100

// Petición dedicada para obtener el estado/mensaje de gas (endpoint aparte)
const fetchGasData = async () => {
  try {
    const resp = await fetch(`${RPI_URL}/api/gas`)
    if (!resp.ok) throw new Error(`HTTP error! status: ${resp.status}`)
    const j = await resp.json()
    // estructura posible: { message: { message: 'On development' } } o { message: '...' }
    const msg = j?.message?.message ?? j?.message ?? ''
    datos_gas.value = msg ? String(msg) : ''
  } catch (e) {
    console.warn('fetchGasData error', e)
    datos_gas.value = ''
  }
}

// Obtener historial directamente desde la API de mediciones
const fetchMeasurements = async () => {
  try {
    const response = await fetch(`${RPI_URL}/api/measurements`)
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
    const json = await response.json()
    // La API devuelve { data: [ [id, timestamp, temp, hum, gasMsg, ...], ... ] }
    const rows = Array.isArray(json?.data) ? json.data as any[] : []

    // ordenar filas por timestamp asc
    const sortedRows = rows.slice().sort((a, b) => new Date(String(a[1])).getTime() - new Date(String(b[1])).getTime())

    // Mapear filas a muestras con temperatura y humedad (solo filas con ambos valores numéricos)
    const samples: Sample[] = sortedRows
      .map(r => ({ time: String(r[1]), temperatura: r[2] == null ? NaN : Number(r[2]), humedad: r[3] == null ? NaN : Number(r[3]) }))
      .filter(s => Number.isFinite(s.temperatura) && Number.isFinite(s.humedad))
      .slice(-MAX_SAMPLES)

    chartSamples.value = samples
    // Guardar filas crudas para páginas de detalle
    measurementsRows.value = sortedRows.slice(-MAX_SAMPLES)

    // Construir serie numérica simple para gas: 1 = evento gas, 0 = no evento
    gasSamples.value = measurementsRows.value.map(r => r && r[4] ? 1 : 0)

    // Últimos valores legibles para mostrar en las tarjetas
    const last = [...sortedRows].reverse().find(r => r && (r[2] != null || r[3] != null))
    if (last) {
      const t = Number(last[2])
      const h = Number(last[3])
      datos_temperatura.value = Number.isFinite(t) ? `${t}°C` : datos_temperatura.value
      datos_humedad.value = Number.isFinite(h) ? `${h}%` : datos_humedad.value
    }

    // Gas: la API devuelve un mensaje de evento en r[4]; guardamos el último mensaje como texto en datos_gas
    const lastGas = [...sortedRows].reverse().find(r => r && r[4])
    datos_gas.value = lastGas ? String(lastGas[4]) : datos_gas.value

  } catch (error) {
    console.error('Error al obtener measurements:', error)
  }
}

onMounted(() => {
  // petición inicial y luego polling cada 5 minutos (incluye gas)
  fetchMeasurements()
  fetchGasData()
  setInterval(() => {
    fetchMeasurements()
    fetchGasData()
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
