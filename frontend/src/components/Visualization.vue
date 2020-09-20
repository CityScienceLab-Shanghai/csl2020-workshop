<template>
    <div class="visualization">
        <h1>Simulation result:</h1>
        <span></span>
    </div>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'Visualization',
    props: {
        simData: Object
    },
    data: function () {
        return {};
    },
    methods: {
        draw() {
            d3.selectAll("span")
            .text(this.simData.data);
        }
    },
    watch: {
        simData (newData) {
            this.simData = newData;
            this.draw();
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
span {
    font-size: 1.2em;
}
</style>
