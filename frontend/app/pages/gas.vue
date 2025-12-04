<template>
    <div class="h-svh w-svw font-sans">
        <NavBar />
  <MainLayout>
    <section class="p-6 max-w-4xl mx-auto">
      <h1 class="text-2xl font-bold mb-4">Gas - Detalle</h1>

      <div class="bg-white p-4 rounded shadow">
        <h2 class="font-semibold mb-2">Eventos de Gas</h2>
        <canvas ref="canvas" class="w-full h-40 mb-4"></canvas>
        <ul class="mt-2 text-sm text-gray-700">
          <li v-for="(row, idx) in gasRows" :key="idx">
            <strong>{{ new Date(row[1]).toLocaleString() }}</strong> — {{ row[4] }}
          </li>
          <li v-if="gasRows.length === 0" class="text-gray-500">No hay eventos de gas registrados.</li>
        </ul>
      </div>
    </section>
  </MainLayout>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick, computed } from 'vue'
import { useSamples } from '@/composables/samples'

const { measurementsRows, gasSamples } = useSamples()

const canvas = ref<HTMLCanvasElement | null>(null)

const gasRows = computed(() => (measurementsRows.value ?? []).filter((r: any) => r && r[4]))

function draw() {
  const c = canvas.value
  if (!c) return
  const ctx = c.getContext('2d')!
  const w = c.clientWidth
  const h = c.clientHeight
  const dpr = window.devicePixelRatio || 1
  c.width = Math.round(w * dpr)
  c.height = Math.round(h * dpr)
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  ctx.clearRect(0, 0, w, h)

  const arr = gasSamples.value ?? []
  if (!arr || arr.length === 0) {
    ctx.fillStyle = '#9ca3af'
    ctx.font = '13px sans-serif'
    ctx.fillText('sin datos', 10, 20)
    return
  }

  const pad = 6
  const plotW = w - pad * 2
  const plotH = h - pad * 2
  const denom = Math.max(arr.length - 1, 1)

  ctx.beginPath()
  for (let i = 0; i < arr.length; i++) {
    const x = pad + (plotW * i) / denom
    const y = pad + (1 - (arr[i] ?? 0)) * plotH // 1 -> top, 0 -> bottom
    if (i === 0) ctx.moveTo(x, y)
    else ctx.lineTo(x, y)
  }
  ctx.strokeStyle = '#ef4444'
  ctx.lineWidth = 1.5
  ctx.stroke()
}

onMounted(() => {
  nextTick(() => draw())
})

watch(() => gasSamples.value, () => draw())
</script>

<style scoped>
canvas { width: 100%; height: 160px; display: block }
</style>