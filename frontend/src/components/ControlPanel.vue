<template>
    <div class="control-panel">
        <PanelPane
            v-for="panel in panels"
            :key="panel.name"
            :name="panel.name"
            :description="panel.description"
            :controls="panel.controls"
            :charts="panel.charts"
            :visible="currentPanel === panel.name"
            @data-update="updateParameters"
            @mouse-entered="currentPanel = panel.name"
        ></PanelPane>
        
        <b-button-group class="simulation-button">
            <b-button variant="primary" :disabled="running" @click="runSimulation">
                {{ running ? status + percent : "Run Simulation" }}
                <div class="progress-fill" v-if="running" :style="{width: percent}"></div>
            </b-button>

            <b-button class="stop" variant="primary" v-if="running" @click="stopSimulation">
                <b-icon-stop-fill></b-icon-stop-fill>
            </b-button>
        </b-button-group>
    </div>
</template>

<script>
import axios from "axios";
import axiosCookieJarSupport from "axios-cookiejar-support";
import tough from "tough-cookie";

import PanelPane from './PanelPane.vue';

axiosCookieJarSupport(axios);
axios.defaults.withCredentials = true;

const cookieJar = new tough.CookieJar();

export default {
    name: "ControlPanel",
    props: {
        simulateApi: String,
        statusApi: String,
        resultsApi: String,
        stopApi: String,
        panels: Array,
        incentiveMode: Number,
    },
    components: {
        PanelPane,
    },
    data: function () {
        return {
            running: false, // Whether the simulation is currently running
            progress: 0,
            percent: '0%',
            status: 'Simulating...',
            maxProgress: 60,
            currentPanel: this.panels[0].name, // Current focused panel. Only show one panel at a time.
            parameters: {},
            heartbeat: null
        };
    },
    methods: {
        // Update current parameters
        updateParameters(data) {
            for (var key of Object.keys(data)) {
                this.parameters[key] = Number(data[key]);
            }

            if (this.incentiveMode === 2) {
                this.$emit('goal-update', [
                    this.parameters['normalized_low_inc_pop_ratio_target'].map(0, 1, 0, 100),
                    this.parameters['normalized_diversity_target'].map(0, 1, 0, 100),
                    this.parameters['normalized_building_energy_target'].map(0, 1, 0, 100),
                    this.parameters['normalized_commute_distance_decrease_target'].map(0, 1, 0, 100),
                ])
            }
        },

        // Send params to GAMA and start simulation
        runSimulation() {
            console.log("Running simulation");
            console.log(this.parameters);

            axios.get(this.statusApi, {
                jar: cookieJar,
                withCredentials: true,
            }).then((response) => {
                if (response.data === 'Terminated') {
                    axios.post(this.simulateApi, this.parameters, {
                        jar: cookieJar,
                        withCredentials: true,
                    }).then(() => {
                        this.running = true;
                        this.progress = 0;
                        this.percent = '0%';
                        this.status = 'Simulating...';
                        this.startHeartBeat();
                    }).catch((error) => {
                        console.log(error);
                        axios.post(this.simulateApi, this.parameters).then(() => {
                            this.running = true;
                            this.progress = 0;
                            this.percent = '0%';
                            this.status = 'Simulating...';
                            this.startHeartBeat();
                        })
                    });
                } else {
                    this.running = true;
                    this.progress = 0;
                    this.percent = '0%';
                    this.status = 'Simulating...';
                    this.startHeartBeat();
                }
            });

            
        },

        stopSimulation() {
            console.log('Stopping simulation');

            axios.get(this.stopApi, {
                jar: cookieJar,
                withCredentials: true,
            }).then((response) => {
                console.log(response);
                this.running = false;
                this.progress = 0;
                this.percent = '0%';
                this.status = 'Simulating...';
                if (this.heartbeat) {
                    clearInterval(this.heartbeat);
                    this.heartbeat = null;
                }
            });
        },

        heartbeatHandler () {
            axios.get(this.statusApi, {
                jar: cookieJar,
                withCredentials: true,
            }).then((response) => {
                console.log(response);
                this.progress = Math.min(this.progress + 1, this.maxProgress - 1);
                this.percent = Math.floor(this.progress / this.maxProgress * 100) + '%';
                if (response.data === 'Terminated') {
                    this.progress = this.maxProgress - 1;
                    this.percent = '99%';
                    this.status = 'Loading results...';
                    this.getResults();
                    setTimeout(() => {
                        this.progress = this.maxProgress;
                        this.heartbeat = null;
                    }, 3000);
                } else {
                    this.heartbeat = setTimeout(this.heartbeatHandler.bind(this), 1000);
                }
            });
        },

        // Start a heartbeat checking for completion once per second
        startHeartBeat() {
            this.heartbeat = setTimeout(this.heartbeatHandler.bind(this), 1000);
        },

        // Get simulation results and publish an event to update all data
        getResults() {
            axios.get(this.resultsApi, {
                jar: cookieJar,
                withCredentials: true,
            }).then((response) => {
                console.log(response);
                if (response.data !== 'GAMA is runninng') {
                    this.$emit("simulation-update", response.data);
                    this.percent = '100%';
                    this.running = false;
                }
            });
        },
    },
    watch: {
        panels () {
            this.parameters = {};
            for (var panel of this.panels) {
                for (var control of panel.controls) {
                    this.parameters[control.id] = control.default;
                }
            }
        }, 
        incentiveMode () {
            if (this.incentiveMode === 0) {
                this.parameters['incentive_policy'] = false;
                this.parameters['dynamic_policy'] = false;
                this.$emit('goal-update', [0, 0, 0, 0]);
            } else if (this.incentiveMode === 1) {
                this.parameters['incentive_policy'] = true;
                this.parameters['dynamic_policy'] = false;
                this.$emit('goal-update', [0, 0, 0, 0]);
            } else if (this.incentiveMode === 2) {
                this.parameters['incentive_policy'] = true;
                this.parameters['dynamic_policy'] = true;
            }
        }
    },
    mounted () {
        for (var panel of this.panels) {
            for (var control of panel.controls) {
                this.parameters[control.id] = control.default.map(0, 1, control.min, control.max);
            }
        }
        this.parameters['incentive_policy'] = false;
        this.parameters['dynamic_policy'] = false;

        axios.get(this.statusApi).then((response) => {
            console.log(response);
            if (response.data === 'Running') {
                this.running = true;
                this.progress = 0;
                this.percent = '0%';
                this.status = 'Simulating...';
                this.startHeartBeat();
            }
        });
    }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.simulation-button {
    width: 100%;
}

.progress-fill {
    position: absolute;
    top: 0px;
    left: 0px;
    height: 100%;
    border-radius: 0.25rem 0 0 0.25rem;
    background: #004da0;
    z-index: -1;
    transition: width 0.3s ease-in-out;
}

.simulation-button .stop {
    flex: 0 0 1em;
}
</style>
