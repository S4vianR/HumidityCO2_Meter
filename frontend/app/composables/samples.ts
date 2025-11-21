export type Sample = { time: string; temperatura: number; humedad: number }

export const useSamples = () => {
  const chartSamples = useState<Sample[]>('chartSamples', () => [])
  const gasSamples = useState<number[]>('gasSamples', () => [])
  const measurementsRows = useState<any[]>('measurementsRows', () => [])
  return { chartSamples, gasSamples, measurementsRows }
}
