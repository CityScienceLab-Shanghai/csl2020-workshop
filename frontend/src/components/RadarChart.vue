<script>
import { Radar, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
    name: 'RadarChart',
    extends: Radar,
    mixins: [reactiveProp],
    data () {
        return {
            options: {
                scale: {
                    gridLines: {
                        circular: true
                    },
                    ticks: {
                        beginAtZero: true,
                        suggestedMax: 100,
                        maxTicksLimit: 7
                    },
                },
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

<style>
</style>