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
                        circular: true,
                        color: 'rgba(255, 255, 255, 0.3)'
                    },
                    angleLines : {
                        color: 'rgba(255, 255, 255, 0.3)'
                    },
                    ticks: {
                        beginAtZero: true,
                        suggestedMax: 100,
                        maxTicksLimit: 7,
                        backdropColor: 'black'
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