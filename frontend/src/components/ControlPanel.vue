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
                {{ running ? "Running..." + Math.floor(progress / 60 * 100) + '%' : "Run Simulation" }}
            </b-button>

            <b-button class="stop" variant="primary" v-if="running" @click="stopSimulation">
                <b-icon-stop-fill></b-icon-stop-fill>
            </b-button>
        </b-button-group>
    </div>
</template>

<script>
import axios from "axios";
import PanelPane from './PanelPane.vue';

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
        },

        // Send params to GAMA and start simulation
        runSimulation() {
            console.log("Running simulation");
            console.log(this.parameters);

            axios.post(this.simulateApi, this.parameters).then(() => {
                this.running = true;
                this.progress = 0;
                this.startHeartBeat();
            });
        },

        stopSimulation() {
            console.log('Stopping simulation');

            axios.get(this.stopApi).then((response) => {
                console.log(response);
                this.running = false;
                this.progress = 0;
                if (this.heartbeat) {
                    clearInterval(this.heartbeat);
                    this.heartbeat = null;
                }
            });
        },

        // Start a heartbeat checking for completion once per second
        startHeartBeat() {
            this.heartbeat = setInterval(() => {
                axios.get(this.statusApi).then((response) => {
                    console.log(response);
                    this.progress = Math.min(this.progress + 1, 60);
                    if (response.data === 'Terminated') {
                        this.progress = 60;
                        this.getResults();
                        setTimeout(() => {
                            this.running = false;
                            clearInterval(this.heartbeat);
                            this.heartbeat = null;
                        }, 3000);
                    }
                });
            }, 1000);
        },

        // Get simulation results and publish an event to update all data
        getResults() {
            axios.get(this.resultsApi).then((response) => {
                console.log(response);
                this.$emit("simulation-update", response.data);
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
            } else if (this.incentiveMode === 1) {
                this.parameters['incentive_policy'] = true;
                this.parameters['dynamic_policy'] = false;
            } else if (this.incentiveMode === 2) {
                this.parameters['incentive_policy'] = true;
                this.parameters['dynamic_policy'] = true;
            }
        }
    },
    mounted () {
        for (var panel of this.panels) {
            for (var control of panel.controls) {
                this.parameters[control.id] = control.default;
            }
        }
        this.parameters['incentive_policy'] = false;
        this.parameters['dynamic_policy'] = false;

        axios.get(this.statusApi).then((response) => {
            console.log(response);
        });
    }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.simulation-button {
    width: 100%;
}

.simulation-button .stop {
    flex: 0 0 1em;
}
</style>
