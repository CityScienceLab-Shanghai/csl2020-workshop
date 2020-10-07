// DONE: Remove all value mapping, except for radar chart (0...1 => 0...100)
// DONE: Radar chart add last time history and goals
// TODO: Add a line chart showing the change in three policies in dynamic mode
// TODO: Bind to Can's grid and dynamic policy data
// TODO: Add favicon
// TODO: Smaller screens?

<template>
    <div id="app">
        <Visualization 
        :sim-data="agentsData"
        :step="currentStep" 
        :animate="animate"
        :highlights="highlights[currentStep]"
        :map-data="mapData"
        @time-update="updateCurrentTime(Number.parseInt($event))"/>

        <b-container fluid id="bottom-container">
            <b-row align-v="end" class="h-100" >
                <b-col cols="3" class="panel-col" align-self="end">
                    <img style="width: 100%;" src="images/legends.png"/>
                </b-col>
                <b-col align-self="end">
                    <DynamicPolicy v-if="incentiveMode === 2" class="w-80"
                    :step="currentStep" :policy="policies[currentStep]"/>
                    <div id="slider">
                        <b-input-group :prepend="'Simulation step: ' + currentStep" class="mt-3">
                            <b-form-input type="range" min="0" max="12" value="12" 
                            @change="currentStep = Number.parseInt($event)"></b-form-input>
                        </b-input-group>
                    </div>
                </b-col>
                <b-col cols="3" class="output-col" align-self="end">
                    <img style="width: 100%;" src="images/credit.png"/>
                </b-col>
            </b-row>
        </b-container>

        <b-container fluid style="pointer-events: none;">
            <b-row class="h-100">
                <b-col cols="3" class="panel-col h-100" style="pointer-events: auto; padding-bottom: 2em;">
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
                        @goal-update="updateGoalData($event)"
                    />
                </b-col>
                <b-col>
                    <div class="time" style="pointer-events: auto;">
                        <div class="time-title">Time of the day</div>
                        <div class="time-text" @click="animate = !animate">
                            {{ currentTime }}
                            <b-icon-pause-fill v-if="animate"></b-icon-pause-fill>
                            <b-icon-play-fill v-if="!animate"></b-icon-play-fill>
                        </div>
                    </div>
                </b-col>
                <b-col cols="3" class="output-col h-100" style="pointer-events: auto; padding-bottom: 2em;">
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

import axios from "axios";

import IncentivePanel from "./components/IncentivePanel.vue";
import ControlPanel from "./components/ControlPanel.vue";
import Visualization from "./components/Visualization.vue";
import OutputPanel from "./components/OutputPanel.vue";
import DynamicPolicy from "./components/DynamicPolicy.vue";

import Config from "./Config.js";

Number.prototype.map = function (in_min, in_max, out_min, out_max) {
    return (this - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

export default {
    name: "App",
    components: {
        IncentivePanel,
        ControlPanel,
        Visualization,
        OutputPanel,
        DynamicPolicy
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

            mapData: [],
            agentsData: {},
            highlights: {
                0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 
                7: [], 8: [], 9: [], 10: [], 11: [], 12: []
            },
            policies: {
                0: [0, 0, 0], 1: [0, 0, 0], 2: [0, 0, 0], 3: [0, 0, 0], 4: [0, 0, 0],
                5: [0, 0, 0], 6: [0, 0, 0], 7: [0, 0, 0], 8: [0, 0, 0], 
                9: [0, 0, 0], 10: [0, 0, 0], 11: [0, 0, 0], 12: [0, 0, 0]
            },

            currentStep: 12,
            currentTime: '0:00 AM',
            animate: false,
        };
    },
    methods: {

        makeRadarChartData (sourceData, goals) {
            var data = {...this.outputPanels[0].charts[0].data}
            if (sourceData) {
                data.datasets[2].data = [...data.datasets[0].data];
                data.datasets[0].data = [
                    Number.parseFloat(sourceData[12]['normalized_kendall_low_inc_ratio']).map(0, 1, 0, 100), //.map(0.35, 0.65, 0, 100), 
                    Number.parseFloat(sourceData[12]['normalized_kendall_diversity']).map(0, 1, 0, 100), //.map(0.62, 0.694, 0, 100), 
                    Number.parseFloat(sourceData[12]['normalized_residence_energy_per_person']).map(0, 1, 0, 100), //.map(50, 60, 100, 0),
                    Number.parseFloat(sourceData[12]['normalized_mean_commute_distance_decrease']).map(0, 1, 0, 100), //.map(-0.1, 0.6, 0, 100)
                ];
            }
            if (goals) {
                data.datasets[3].data = goals;
            }
            return data;
        },

        makeLineChartsData (sourceData) {
            var chartsData = [];
            for (var chartId in Config.outputPanels[1].charts) {
                var data = {...Config.outputPanels[1].charts[chartId].data}

                for (var datasetId in Config.outputPanels[1].charts[chartId].data.datasets) {
                    var datasetKey = Config.outputPanels[1].charts[chartId].data.datasets[datasetId].key;
                    if (!datasetKey) continue;
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
        },

        updateGoalData (data) {
            this.outputPanels[0].charts[0].data = this.makeRadarChartData(null, data);
        },

        updateSimulationData (data) {
            this.outputPanels[0].charts[0].data = this.makeRadarChartData(data);
            var chartData = this.makeLineChartsData(data);
            for (var chartId in chartData) {
                this.outputPanels[1].charts[chartId].data = chartData[chartId];
            }
            this.updateAgentsData(data);
            this.updateHighlightPoliciesData(data);

            if (!this.animate) this.animate = true;
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
        },

        updateHighlightPoliciesData (data) {
            for (var step = 0; step < 13; step++) {
                if (!data[step]) continue;
                this.highlights[step] = data[step].grids_with_top6_potential.map( name => 'landuse' + name);
                this.policies[step] = [
                    Number.parseFloat(data[step].normalized_rent_discount_ratio_low_inc),
                    Number.parseFloat(data[step].normalized_rent_discount_ratio_less_commuting),
                    Number.parseFloat(data[step].normalized_rent_discount_ratio_small_scale),
                ]
            }
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
        }
    },
    mounted () {
        var gridUrl = "/geodata/grid.json";
        var mapUrl = "/geodata/greater_area.geojson";
        
        Promise.all([axios.get(gridUrl), axios.get(mapUrl)]).then((results) => {
            this.mapData = [
                results[0].data, results[1].data
            ]
        });
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
    overflow-y: auto;
}

.output-col {
    min-width: 350px;
    overflow-y: auto;
}

img.credit {
    width: 100%;
}

img.legends {
    width: 100%;
}

#bottom-container {
    bottom: 1.5em;
}

</style>
