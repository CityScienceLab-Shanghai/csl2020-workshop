<template>
    <div id="app">
        <Visualization 
        :sim-data="agentsData"
        :step="currentStep" 
        :animate="animate"
        @agents-update="updateAgentsData($event)"
        @time-update="updateCurrentTime(Number.parseInt($event))"/>
        <b-container fluid>
            <b-row class="h-100">
                <b-col cols="3">
                    <IncentivePanel
                        :incentive-modes="incentiveModes"
                        :current-mode="incentiveMode"
                        @incentive-update="incentiveMode = Number.parseInt($event)"/>
                    <ControlPanel
                        v-if="incentiveMode > 0"
                        :panels="[[], staticPanels, dynamicPanels][incentiveMode]"
                        :simulateApi="simulateApi"
                        :statusApi="statusApi"
                        :resultsApi="resultsApi"
                        @simulation-update="updateSimulationData($event)"
                    />
                </b-col>
                <b-col>
                    <b-button size="lg" :variant="animate ? 'success' : 'danger'" @click="animate = !animate">
                        <b-icon-pause-fill v-if="animate"></b-icon-pause-fill>
                        <b-icon-play-fill v-if="!animate"></b-icon-play-fill>
                        {{ currentTime }}
                    </b-button>
                </b-col>
                <b-col cols="3">
                    <OutputPanel :panels="outputPanels" />
                </b-col>
            </b-row>
            <b-row align-v="end">
                <b-col cols="3"></b-col>
                <b-col cols="6">
                    <div id="slider">
                        <b-input-group :prepend="'Simulation step: ' + (currentStep + 1)" class="mt-3">
                            <b-form-input type="range" min="1" max="12" value="1" 
                                @change="currentStep = Number.parseInt($event) - 1"></b-form-input>
                            <!-- <b-input-group-append>
                                <b-button :variant="animate ? 'success' : 'danger'" @click="animate = !animate">
                                    <b-icon-pause-fill v-if="animate"></b-icon-pause-fill>
                                    <b-icon-play-fill v-if="!animate"></b-icon-play-fill>
                                    {{ currentTime }}:00
                                </b-button>
                            </b-input-group-append> -->
                        </b-input-group>
                    </div>
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

import IncentivePanel from "./components/IncentivePanel.vue";
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
    for (var i = 0; i < 12; i++) {
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
        IncentivePanel,
        ControlPanel,
        Visualization,
        OutputPanel
    },
    data: function () {
        return {
            simulateApi: Config.simulateApi,
            statusApi: Config.statusApi,
            resultsApi: Config.resultsApi,
            staticPanels: Config.staticPanels,
            dynamicPanels: Config.dynamicPanels,
            outputPanels: Config.outputPanels,
            incentiveModes: Config.incentiveModes,
            incentiveMode: 0,
            agentsData: {},
            currentStep: 0,
            currentTime: '00:00',
            animate: true,
        };
    },
    methods: {
        updateSimulationData (data) {
            this.outputPanels[0].charts[0].data = makeRadarChartData(data);
            this.outputPanels[0].charts[1].data = makeLineChartData(data);
        },

        updateAgentsData (data) {
            this.agentsData = data;
        },

        changeStep (_, value) {
            this.currentStep = Number.parseInt(value) - 1;
        },

        updateCurrentTime(time) {
            var hours = Math.floor(time / 60);
            var minutes = time % 60;
            hours = hours < 10 ? '0' + hours : '' + hours;
            minutes = minutes < 10 ? '0' + minutes : '' + minutes;
            this.currentTime = hours + ':' + minutes;
        }
    }
};
</script>

<style>
html, body {
    margin: 0;
    padding: 0;
    overflow: hidden;
    -moz-user-select: none; 
    -webkit-user-select: none; 
    -ms-user-select:none; 
    user-select:none;
    -o-user-select:none;
}

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

.container-fluid {
    height: 100%;
    position: absolute;
}

.bar {
    padding: 0.25rem;
}

.slider {
    padding-bottom: 0.25rem;
}

#slider {
    transform: translateY(-250%);
}
</style>
