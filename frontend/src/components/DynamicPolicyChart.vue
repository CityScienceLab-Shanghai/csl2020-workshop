<script>
import { HorizontalBar, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
    name: 'DynamicPolicyChart',
    extends: HorizontalBar,
    mixins: [reactiveProp],
    data () {
        return {
            options: {
                legend: {
                    align: 'start',
                    labels: {
                        boxWidth: 18,
                        fontSize: 18,
                        fontColor: 'white'
                    }
                },
                // scale: {
                //     xAxes: [{
                //         ticks: {
                //             beginAtZero: true,
                //             suggestedMax: 100,
                //             maxTicksLimit: 7,
                //             backdropColor: 'black'
                //         },
                //     }],
                //     yAxes: [{
                //         ticks: {
                //             sampleSize: 3,
                //             beginAtZero: true,
                //             suggestedMax: 100,
                //             maxTicksLimit: 7,
                //             backdropColor: 'black'
                //         },
                //     }]
                // },
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