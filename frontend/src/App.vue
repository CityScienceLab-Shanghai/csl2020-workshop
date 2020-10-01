<template>
    <div id="app">
        <b-container fluid>
            <b-row>
                <b-col cols="2">
                    <ControlPanel
                        :panels="controlPanels"
                        :simulateApi="simulateApi"
                        :statusApi="statusApi"
                        :resultsApi="resultsApi"
                        @simulation-update="updateSimulationData($event)"
                    />
                </b-col>
                <b-col cols="7">
                    <Visualization :sim-data="agentsData" />
                </b-col>
                <b-col cols="3">
                    <OutputPanel :panels="outputPanels" />
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
import Vue from "vue";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

import ControlPanel from "./components/ControlPanel.vue";
import Visualization from "./components/Visualization.vue";
import OutputPanel from "./components/OutputPanel.vue";

import Config from "./Config.js";

function makeRadarChartData (sourceData) {
    var data = {...Config.outputPanels[0].charts[0].data}
    data.datasets[2].data = [
        Number.parseFloat(sourceData[12]['Low Income Proportion']) * 100, 
        Number.parseFloat(sourceData[12]['Diversity']) * 100, 
        10, 
        Number.parseFloat(sourceData[12]['All']) / 20
    ];
    return data;
}

function makeLineChartData (sourceData) {
    var data = {...Config.outputPanels[0].charts[1].data}
    data.datasets[0].data = [];
    data.datasets[1].data = [];

    data.datasets[3].data = [];
    for (var i = 1; i <= 12; i++) {
        data.datasets[0].data.push(
            Number.parseFloat(sourceData[i]['Low Income Proportion']) * 100
        );
        data.datasets[1].data.push(
            Number.parseFloat(sourceData[i]['Diversity']) * 100
        );

        data.datasets[3].data.push(
            Number.parseFloat(sourceData[i]['All']) / 20
        );
    }
    return data;
}

export default {
    name: "App",
    components: {
        ControlPanel,
        Visualization,
        OutputPanel,
    },
    data: function () {
        return {
            simulateApi: Config.simulateApi,
            statusApi: Config.statusApi,
            resultsApi: Config.resultsApi,
            controlPanels: Config.controlPanels,
            outputPanels: Config.outputPanels,
            agentsData: {},
        };
    },
    methods: {
        updateSimulationData (data) {
            console.log(data);
            // this.agentsData = data;
            // console.log(getThemeColor('gray', 0.5));
            this.outputPanels[0].charts[0].data = makeRadarChartData(data);
            this.outputPanels[0].charts[1].data = makeLineChartData(data);
        }
    },
};
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
    margin-top: 1em;
}

.container {
    margin: 0px;
    width: 100%;
}
</style>
