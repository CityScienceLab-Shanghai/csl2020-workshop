<script>
import { Line, mixins, defaults } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
    name: 'LineChart',
    extends: Line,
    mixins: [reactiveProp],
    data () {
        return {
            options: {
                ...defaults,
                maintainAspectRatio: false,
                legend: {
                    labels: {
                        boxWidth: 30
                    }
                }
            }
        };
    },
    mounted () {
        this.renderChart(this.chartData, this.options)
    }
}
</script>

<style scoped>
canvas {
    height: 15em;
}
</style>