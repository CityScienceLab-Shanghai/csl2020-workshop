<template>
    <b-card
        class="mb-2"
        :title="name"
        :sub-title="description"
        @mouseenter="$emit('mouse-entered')"
        @click="$emit('mouse-entered')"
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
                :min="control.min"
                :max="control.max"
                :disabled="control.disabled"
                @slider-change="dataUpdated"
            ></Slider>

            <div v-for="chart in charts" :key="chart.id">
                <b v-if="chart.title" style="font-size: 1em;">{{chart.title}}</b>
                <Chart
                    :type="chart.type"
                    :chart-data="chart.data"
                ></Chart>
            </div>
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
.card {
    border: #979797;
}

.card-body {
    background: black;
    border: 1px solid #979797;
    border-radius: 5px;
    font-size: 0.9em !important;
    color: white;
}

.card-title {
    color: white !important;
    font-size: 1.5em !important;
}

.card-subtitle.text-muted {
    color: white !important;
    font-size: 0.9em !important;
    font-weight: 100;
}

.col-form-label {
    font-size: 0.9em !important;
    font-weight: 100;
}
</style>
