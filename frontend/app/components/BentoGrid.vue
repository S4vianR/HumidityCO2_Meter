<template>
  <div
    class="grid gap-6 p-4 grid-cols-6 auto-rows-[120px] lg:grid-cols-6 md:grid-cols-4 sm:grid-cols-2"
    role="list">
    <div
      v-for="card in cards"
      :key="card.id"
      :style="gridStyle(card)"
      class="bg-slate-50 rounded-xl shadow-md hover:shadow-lg transform hover:-translate-y-1 transition-transform duration-150 flex items-stretch"
      @click="onCardClick(card)">

      <div class="p-4 flex flex-col w-full">
        <div class="flex justify-between items-start gap-2">
          <h3 class="font-semibold text-slate-900 text-base">{{ card.title }}</h3>
          <small v-if="card.subtitle" class="text-slate-500 text-sm">{{ card.subtitle }}</small>
        </div>

        <div class="mt-2 flex-1 flex flex-col">
          <div class="mt-auto flex items-center justify-between gap-4">
            <div class="text-2xl font-bold text-slate-900">{{ card.value }}</div>
            <!-- mini chart preview for temperature/humidity/gas cards -->
            <div v-if="isPreviewCard(card.id)" class="w-36 h-16 bg-white rounded shadow-inner flex items-center justify-center">
              <canvas :ref="setMiniCanvas(card.id)" class="w-full h-full"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, nextTick, type ComponentPublicInstance } from 'vue'
import { useRouter } from 'vue-router'

interface Card {
  id: number | string
  title: string
  subtitle?: string
  value?: string
  cols?: number
  rows?: number
  route?: string
}

const props = defineProps<{
  cards: Card[]
  tempSeries?: number[]
  humSeries?: number[]
  gasSeries?: number[]
}>()

const router = useRouter()

const miniRefs: Record<string, HTMLCanvasElement | null> = {}

/*
  The ref callback can receive either a DOM Element or a ComponentPublicInstance.
  Accept both and normalize to an HTMLCanvasElement when possible.
*/
const setMiniCanvas = (id: string | number) => (el: Element | ComponentPublicInstance | null, _refs?: Record<string, any>) => {
  if (!el) return

  // If it's a Vue component instance, try to use its $el
  if ((el as ComponentPublicInstance).$el && (el as ComponentPublicInstance).$el instanceof Element) {
    const possibleEl = (el as ComponentPublicInstance).$el as Element
    if (possibleEl instanceof HTMLCanvasElement) {
      miniRefs[String(id)] = possibleEl
      drawMini(String(id))
      return
    }
  }

  // If it's a DOM element, coerce to canvas if possible
  if (el instanceof HTMLCanvasElement) {
    const canvasEl = el as HTMLCanvasElement
    miniRefs[String(id)] = canvasEl
    // draw when element is attached
    if (canvasEl) drawMini(String(id))
  } else {
    // not a canvas element -> clear stored ref
    miniRefs[String(id)] = null
  }
}

const gridStyle = (card: Card) => {
  const cols = card.cols ?? 1
  const rows = card.rows ?? 1
  return {
    gridColumn: `span ${cols}`,
    gridRow: `span ${rows}`,
  }
}

const isPreviewCard = (id: string | number) => ['temp', 'hum', 'gas'].includes(String(id))

function onCardClick(card: Card) {
  if (card.route) router.push(card.route)
}

function drawMini(id: string) {
  const canvas = miniRefs[id]
  if (!canvas) return
  const ctx = canvas.getContext('2d')!
  const w = canvas.clientWidth
  const h = canvas.clientHeight
  const dpr = window.devicePixelRatio || 1
  canvas.width = Math.round(w * dpr)
  canvas.height = Math.round(h * dpr)
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  ctx.clearRect(0, 0, w, h)

  let arr: number[] = []
  let color = '#111'
  if (id === 'temp') { arr = props.tempSeries ?? []; color = '#ef4444' }
  if (id === 'hum') { arr = props.humSeries ?? []; color = '#3b82f6' }
  if (id === 'gas') { arr = props.gasSeries ?? []; color = '#f59e0b' }
  if (!arr || arr.length === 0) {
    ctx.fillStyle = '#9ca3af'
    ctx.font = '11px sans-serif'
    ctx.fillText('sin datos', 8, 14)
    return
  }

  const max = Math.max(...arr)
  const min = Math.min(...arr)
  const pad = 4
  const plotW = w - pad * 2
  const plotH = h - pad * 2
  const denom = Math.max(arr.length - 1, 1)
  const toXY = (i: number, v: number) => {
    const x = pad + (plotW * i) / denom
    const range = (max - min) || 1
    const y = pad + ((max - v) / range) * plotH
    return { x, y }
  }
  ctx.beginPath()
  for (let i = 0; i < arr.length; i++) {
    const value = arr[i] ?? arr[0]!
    const { x, y } = toXY(i, value)
    if (i === 0) ctx.moveTo(x, y)
    else ctx.lineTo(x, y)
  }
  ctx.strokeStyle = color
  ctx.lineWidth = 1.5
  ctx.stroke()
}

onMounted(() => {
  // redraw all mini charts after mount
  nextTick(() => {
    ;['temp', 'hum', 'gas'].forEach(id => drawMini(id))
  })
})

// redraw when series change
watch(() => props.tempSeries, () => drawMini('temp'))
watch(() => props.humSeries, () => drawMini('hum'))
watch(() => props.gasSeries, () => drawMini('gas'))
</script>

<style scoped>
canvas { width: 100%; height: 100%; display: block }
</style>

