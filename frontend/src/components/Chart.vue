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
    data: function () {
        return {
        };
    }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
