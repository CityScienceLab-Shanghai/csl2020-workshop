<template>
    <b-card
        :title="name"
        :sub-title="description"
        class="mb-2"
    >
            <Slider
                v-for="control in controls"
                :key="control.id"
                :id="control.id"
                :name="control.name"
                :description="control.description"
                @slider-change="dataUpdated"
            ></Slider>
    </b-card>
</template>

<script>
import Slider from './Slider.vue'

export default {
    name: "PanelPane",
    props: {
        name: String,
        description: String,
        controls: Array,
    },
    components: {
        Slider
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
            this.parameters[control.id] = 0;
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
