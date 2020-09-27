<template>
    <b-card
        class="mb-2"
        :title="name"
        :sub-title="description"
        @mouseenter="$emit('mouse-entered')"
    >
        <b-collapse
            :visible="visible"
        >
            <Slider
                v-for="control in controls"
                :key="control.id"
                :id="control.id"
                :name="control.name"
                :description="control.description"
                :default="control.default"
                @slider-change="dataUpdated"
            ></Slider>

            <Chart
                v-for="chart in charts"
                :key="chart.id"
                :type="chart.type"
                :chart-data="chart.data"
            ></Chart>
        </b-collapse>
    </b-card>
</template>

<script>
import Slider from './Slider.vue'
import Chart from './Chart.vue'

export default {
    name: "PanelPane",
    props: {
        name: String,
        description: String,
        controls: Array,
        charts: Array,
        visible: Boolean
    },
    components: {
        Slider, Chart
    },
    data: function () {
        return {
            parameters: {}
        };
    },
    methods: {
        dataUpdated (id, data) {
            this.parameters[id] = data;
            this.$emit('data-update', this.parameters);
        }
    },
    mounted () {
        for (var control of this.controls) {
            this.parameters[control.id] = control.default;
        }
    }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.b-card {
    padding-top: 10em;
}
</style>
