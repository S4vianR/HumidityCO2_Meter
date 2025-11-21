<template>
    <div class="h-svh w-svw font-sans">
        <NavBar />
        <MainLayout>
            <section class="p-6 max-w-4xl mx-auto">
                <h1 class="text-2xl font-bold mb-4">Temperatura - Detalle</h1>
                <TimeCharts :samples="chartSamples" />
                <div class="mt-4 bg-white p-4 rounded shadow">
                    <h2 class="font-semibold">Últimas lecturas</h2>
                    <ul class="mt-2 text-sm text-gray-700">
                        <li v-for="s in chartSamples" :key="s.time">{{ new Date(s.time).toLocaleString() }} — {{
                            s.temperatura }} °C</li>
                    </ul>
                </div>
            </section>
        </MainLayout>
    </div>
</template>

<script setup lang="ts">
import { useSamples } from '@/composables/samples'
const { chartSamples } = useSamples()
</script>
