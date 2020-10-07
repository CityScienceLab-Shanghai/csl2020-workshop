<template>
    <div>
        <RadarChart
            v-if="type === 'radar'"
            :chart-data="chartData"
        />
        <LineChart
            v-else-if="type === 'line'"
            :chart-data="chartData"
        />
    </div>
</template>

<script>
import RadarChart from './RadarChart.vue'
import LineChart from './LineChart.vue'

export default {
    name: "Chart",
    props: {
        id: String,
        type: String,
        chartData: Object
    },
    components: {
        RadarChart, 
        LineChart
    },
    data () {
        return {
            // lastData: {},
        };
    },
    watch: {
        // chartData () {
        //     if (this.type === 'radar') {
        //         this.chartData.datasets[2].data = this.lastData;
        //         this.lastData = [...this.chartData.datasets[0].data];
        //     }
        // }
    },
    mounted () {
        // if (this.type === 'radar') {
        //     this.lastData = [...this.chartData.datasets[0].data];
        // }
    }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
