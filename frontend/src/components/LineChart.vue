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
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    align: 'end',
                    labels: {
                        boxWidth: 10,
                        fontSize: 10,
                        fontColor: 'white'
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
canvas#line-chart {
    height: 8em !important;
}
</style>