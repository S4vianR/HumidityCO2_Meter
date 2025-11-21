<template>
  <div class="w-full max-w-4xl my-4 p-4 bg-white/60 rounded shadow">
    <h3 class="text-lg font-semibold mb-2">Gráficas: Temperatura y Humedad</h3>
    <div v-if="!hasSamples" class="text-sm text-gray-600">Esperando datos... (se mostrarán aquí las gráficas)</div>
    <canvas v-else ref="canvas" class="w-full" :height="height"></canvas>
    <div v-if="hasSamples" class="flex gap-4 mt-2 text-sm items-center">
      <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full" :style="{background: colors.temp}"></span>Temperatura (°C)</span>
      <span class="inline-flex items-center gap-2"><span class="w-3 h-3 rounded-full" :style="{background: colors.hum}"></span>Humedad (%)</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'

interface Sample { time: string; temperatura: number; humedad: number }

const props = defineProps<{ samples: Sample[] }>()
const canvas = ref<HTMLCanvasElement | null>(null)
const height = 240
const colors = { temp: '#ef4444', hum: '#3b82f6', diff: '#10b981' }

const hasSamples = computed(() => Array.isArray(props.samples) && props.samples.length > 0)

function draw() {
  if (!canvas.value) return
  const ctx = canvas.value.getContext('2d')!
  const w = canvas.value.clientWidth
  const h = height
  // Set backing store size for crisp rendering
  const dpr = window.devicePixelRatio || 1
  canvas.value.width = Math.round(w * dpr)
  canvas.value.height = Math.round(h * dpr)
  ctx.scale(dpr, dpr)
  ctx.clearRect(0, 0, w, h)

  if (!hasSamples.value) {
    ctx.fillStyle = '#6b7280'
    ctx.font = '14px sans-serif'
    ctx.fillText('Esperando datos...', 10, 20)
    return
  }

  const samples = props.samples.slice(-100)
  const times = samples.map(s => new Date(s.time))
  const temps = samples.map(s => s.temperatura)
  const hums = samples.map(s => s.humedad)

  const values = temps.concat(hums)
  let min = Math.min(...values)
  let max = Math.max(...values)
  // add small padding
  if (min === max) { min -= 1; max += 1 }
  const padLeft = 40
  const padRight = 10
  const padTop = 20
  const padBottom = 30
  const plotW = w - padLeft - padRight
  const plotH = h - padTop - padBottom

  // draw grid lines
  ctx.strokeStyle = '#e6e7ea'
  ctx.lineWidth = 1
  ctx.beginPath()
  for (let i = 0; i <= 4; i++) {
    const y = padTop + (plotH * i) / 4
    ctx.moveTo(padLeft, y)
    ctx.lineTo(padLeft + plotW, y)
  }
  ctx.stroke()

  // y axis labels
  ctx.fillStyle = '#374151'
  ctx.font = '12px sans-serif'
  ctx.textAlign = 'right'
  for (let i = 0; i <= 4; i++) {
    const v = max - ((max - min) * i) / 4
    const y = padTop + (plotH * i) / 4 + 4
    ctx.fillText(v.toFixed(1), padLeft - 6, y)
  }

  // x axis ticks (show up to 6)
  const step = Math.max(1, Math.floor(samples.length / 6))
  ctx.textAlign = 'center'
  ctx.fillStyle = '#6b7280'
  ctx.font = '11px sans-serif'
  for (let i = 0; i < samples.length; i += step) {
    const x = padLeft + (plotW * i) / (samples.length - 1)
    const t = times[i]
    const label = t?.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    ctx.fillText(label ?? "", x, h - 8)
  }

  function toXY(i: number, v: number) {
    const x = padLeft + (plotW * i) / (samples.length - 1)
    const y = padTop + ((max - v) / (max - min)) * plotH
    return { x, y }
  }

  // draw line helper
  function drawLine(arr: number[], color: string, width = 2) {
    ctx.beginPath()
    for (let i = 0; i < arr.length; i++) {
      const { x, y } = toXY(i, arr[i] ?? 0)
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    }
    ctx.strokeStyle = color
    ctx.lineWidth = width
    ctx.stroke()
  }

  // draw temp (solid)
  drawLine(temps, colors.temp, 2.5)
  // draw hum (dashed)
  ctx.setLineDash([6, 4])
  drawLine(hums, colors.hum, 2)
  ctx.setLineDash([])

  // legend handled below visually by HTML markers
}

let raf = 0
onMounted(() => {
  // draw initially
  raf = requestAnimationFrame(draw)
})

watch(() => props.samples, () => {
  if (raf) cancelAnimationFrame(raf)
  raf = requestAnimationFrame(draw)
}, { deep: true })

</script>

<style scoped>
canvas { width: 100%; display: block; }
</style>
