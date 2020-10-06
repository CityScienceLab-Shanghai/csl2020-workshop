<template>
    <div id="app">
        <Visualization 
        :sim-data="agentsData"
        :step="currentStep" 
        :animate="animate"
        :highlights="highlights"
        @time-update="updateCurrentTime(Number.parseInt($event))"/>
        <img class="credit" src="images/credit.png"/>
        <img class="legends" src="images/legends.png"/>
        <b-container fluid>
            <b-row class="h-100">
                <b-col class="panel-col">
                    <IncentivePanel
                        :incentive-modes="incentiveModes"
                        :current-mode="incentiveMode"
                        @incentive-update="incentiveMode = Number.parseInt($event)"/>
                    <ControlPanel
                        :panels="[nonePanels, staticPanels, dynamicPanels][incentiveMode]"
                        :simulateApi="simulateApi"
                        :statusApi="statusApi"
                        :resultsApi="resultsApi"
                        :stopApi="stopApi"
                        :incentive-mode="incentiveMode"
                        @simulation-update="updateSimulationData($event)"
                    />
                </b-col>
                <b-col>
                    <div class="time">
                        <div class="time-title">Time of the day</div>
                        <div class="time-text" @click="animate = !animate">
                            {{ currentTime }}
                            <b-icon-pause-fill v-if="animate"></b-icon-pause-fill>
                            <b-icon-play-fill v-if="!animate"></b-icon-play-fill>
                        </div>
                    </div>
                </b-col>
                <b-col cols="3" class="output-col">
                    <OutputPanel :panels="outputPanels" />
                </b-col>
            </b-row>
            <b-row align-v="end">
                <b-col cols="3"></b-col>
                <b-col cols="6">
                    <div id="slider">
                        <b-input-group :prepend="'Simulation step: ' + (currentStep + 1)" class="mt-3">
                            <b-form-input type="range" min="0" max="12" value="0" 
                            @change="currentStep = Number.parseInt($event)"></b-form-input>
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

Number.prototype.map = function (in_min, in_max, out_min, out_max) {
    return (this - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

function makeRadarChartData (sourceData) {
    var data = {...Config.outputPanels[0].charts[0].data}
    data.datasets[0].data = [
        Number.parseFloat(sourceData[12]['kendall_low_inc_ratio']).map(0.35, 0.5, 0, 100), 
        Number.parseFloat(sourceData[12]['kendall_diversity']).map(0.62, 0.7, 0, 100), 
        Number.parseFloat(sourceData[12]['residence_energy_per_person']).map(54, 60, 100, 0),
        Number.parseFloat(sourceData[12]['commute_distance_decrease']).map(-0.05, 0.3, 0, 100)
    ];
    return data;
}

function makeLineChartsData (sourceData) {
    var chartsData = [];
    for (var chartId in Config.outputPanels[1].charts) {
        var data = {...Config.outputPanels[1].charts[chartId].data}

        for (var datasetId in Config.outputPanels[1].charts[chartId].data.datasets) {
            var datasetKey = Config.outputPanels[1].charts[chartId].data.datasets[datasetId].key;
            data.datasets[datasetId].data = [];
            for (var i = 0; i <= 12; i++) {
                data.datasets[datasetId].data.push(
                    Number.parseFloat(sourceData[i][datasetKey])
                );
            }
        }

        chartsData.push(data);
    }
    console.log(chartsData)
    return chartsData;
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
            stopApi: Config.stopApi,

            nonePanels: Config.nonePanels,
            staticPanels: Config.staticPanels,
            dynamicPanels: Config.dynamicPanels,
            outputPanels: Config.outputPanels,

            incentiveModes: Config.incentiveModes,
            incentiveMode: 0,

            agentsData: {},
            highlights: [],

            currentStep: 0,
            currentTime: '0:00 AM',
            animate: false,
        };
    },
    methods: {
        updateSimulationData (data) {
            this.outputPanels[0].charts[0].data = makeRadarChartData(data);
            var chartData = makeLineChartsData(data);
            for (var chartId in this.outputPanels[1].charts) {
                this.outputPanels[1].charts[chartId].data = chartData[chartId];
            }
            this.updateAgentsData(data);
        },

        updateAgentsData (data) {
            console.log(data);
            var parsedData = {};
            for (var step = 0; step < 13; step++) {
                if (!data[step]) continue;
                parsedData[step] = [];
                for (var agentid in data[step]['Name List']) {
                    if (data[step]['Population List'][agentid] === 0) continue;
                    parsedData[step].push( {
                        name: data[step]['Name List'][agentid],
                        home: data[step]['Home Loc List'][agentid],
                        work: data[step]['Work Loc List'][agentid],
                        population: data[step]['Population List'][agentid], 
                        income: data[step]['Income List'][agentid]
                    } );
                }
            }
            this.agentsData = parsedData;

            if (!this.animate) this.animate = true;
        },

        updateCurrentTime(time) {
            var hours = Math.floor(time / 60);
            var minutes = time % 60;
            // hours = hours < 10 ? '0' + hours : '' + hours;
            minutes = minutes < 10 ? '0' + minutes : '' + minutes;

            if (hours > 12) {
                this.currentTime = hours - 12 + ':' + minutes + ' PM';
            } else {
                this.currentTime = hours + ':' + minutes + ' AM';
            }

            // this.highlights = [
            //     'landuse' + Math.floor(Math.random() * 252),
            //     'landuse' + Math.floor(Math.random() * 252),
            //     'landuse' + Math.floor(Math.random() * 252),
            //     'landuse' + Math.floor(Math.random() * 252),
            //     'landuse' + Math.floor(Math.random() * 252),
            //     'landuse' + Math.floor(Math.random() * 252),
            // ];
        }
    }
};
</script>

<style>
html, body {
    font-family: 'Titillium Web';
    margin: 0;
    padding: 0;
    overflow: hidden;
    -moz-user-select: none; 
    -webkit-user-select: none; 
    -ms-user-select:none; 
    user-select:none;
    -o-user-select:none;
    background: black;
    color: white;
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

.time {
    color: white;
    text-align: center;
    margin-top: 0.5em;
}

.time-title {
    margin: 0px;
    font-size: 0.8em;
}

.time-text {
    margin: 0px;
    font-size: 1.8em;
    font-weight: bold;
    cursor: pointer;
}

.input-group-text {
    color: white;
    background-color: #2F2F2F;
    border: 1px solid #979797;
    font-weight: bold;
    font-size: 0.8em;
}

.input-group .custom-range {
    background-color: black;
    border: 1px solid #979797;
}

.input-group .custom-range:focus {
    background-color: black;
    border: 1px solid #979797;
}

.panel-col {
    width: 20%;
    min-width: 300px;
    max-width: 350px;
    height: 100%;
    overflow-y: auto;
    padding-bottom: 2em;
}

.output-col {
    min-width: 350px;
    height: 100%;
    overflow-y: auto;
    padding-bottom: 2em;
}

img.credit {
    position: absolute;
    width: 20%;
    min-width: 200px;
    max-width: 350px;
    bottom: 1em;
    right: 1em;
}

img.legends {
    position: absolute;
    width: 20%;
    min-width: 200px;
    max-width: 350px;
    bottom: 1.5em;
    left: 1em;
}
</style>
