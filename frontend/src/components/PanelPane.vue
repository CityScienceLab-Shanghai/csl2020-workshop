<template>
    <b-card
        :title="name"
        :sub-title="description"
        class="mb-2"
    >
            <Slider
                v-for="element in elements"
                :key="element.id"
                :id="element.id"
                :name="element.name"
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
        elements: Array,
    },
    components: {
        Slider
    },
    data: function () {
        return {};
    },
    methods: {
        dataUpdated (element, data) {
            console.log(element, data);
        }
    },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.b-card {
    padding-top: 10em;
}
</style>
