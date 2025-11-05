<template>
  <div
    class="grid gap-6 p-4 grid-cols-6 auto-rows-[120px] lg:grid-cols-6 md:grid-cols-4 sm:grid-cols-2"
    role="list">
    <div
      v-for="card in cards"
      :key="card.id"
      :style="gridStyle(card)"
      class="bg-slate-50 rounded-xl shadow-md hover:shadow-lg transform hover:-translate-y-1 transition-transform duration-150 flex items-stretch">

      <div class="p-4 flex flex-col w-full">
        <div class="flex justify-between items-start gap-2">
          <h3 class="font-semibold text-slate-900 text-base">{{ card.title }}</h3>
          <small v-if="card.subtitle" class="text-slate-500 text-sm">{{ card.subtitle }}</small>
        </div>

        <div class="mt-auto flex items-center">
          <div class="text-2xl font-bold text-slate-900">{{ card.value }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Card {
  id: number | string
  title: string
  subtitle?: string
  value?: string
  cols?: number
  rows?: number
}

const props = defineProps<{
  cards: Card[]
}>()

// Mantenemos style dinámico para grid spans; Tailwind se usa para el resto del estilo.
const gridStyle = (card: Card) => {
  const cols = card.cols ?? 1
  const rows = card.rows ?? 1
  return {
    gridColumn: `span ${cols}`,
    gridRow: `span ${rows}`,
  }
}
</script>

