<template>
    <div class="output-panel">
        <PanelPane
            v-for="panel in panels"
            :key="panel.name"
            :name="panel.name"
            :description="panel.description"
            :controls="panel.controls"
            :charts="panel.charts"
            :visible="panel.name === currentPanel"
            @mouse-entered="currentPanel = panel.name"
        ></PanelPane>
    </div>
</template>

<script>
import PanelPane from './PanelPane.vue';

export default {
    name: "OutputPanel",
    props: {
        panels: Array
    },
    components: {
        PanelPane,
    },
    data: function () {
        return {
            currentPanel: this.panels[0].name,
        };
    },
    methods: {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
img {
    position: absolute;
    width: 90%;
    bottom: 2em;
}
</style>
