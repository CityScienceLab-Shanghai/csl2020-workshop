<template>
    <div class="control-panel">
        <PanelPane
            v-for="panel in panels"
            :key="panel.name"
            :name="panel.name"
            :description="panel.description"
            :controls="panel.controls"
            :visible="currentPanel === panel.name"
            @data-update="updateParameters"
            @mouse-entered="currentPanel = panel.name"
        ></PanelPane>
        
        <b-button
            class="md-raised md-primary"
            :disabled="running"
            @click="runSimulation"
        >{{ running ? "Running...": "Run Simulation" }}</b-button>
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
        panels: Array
    },
    components: {
        PanelPane,
    },
    data: function () {
        return {
            running: false, // Whether the simulation is currently running
            currentPanel: this.panels[0].name, // Current focused panel. Only show one panel at a time.
            parameters: {}
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

            axios.get(this.simulateApi, this.parameters).then(() => {
                this.running = true;
                this.startHeartBeat();
            });
        },

        // Start a heartbeat checking for completion once per second
        startHeartBeat() {
            var heartbeat = setInterval(() => {
                axios.get(this.statusApi).then(() => {
                    this.running = false;
                    clearInterval(heartbeat);
                    this.getResults();
                });
            }, 1000);
        },

        // Get simulation results and publish an event to update all data
        getResults() {
            axios.get(this.resultsApi).then((response) => {
                this.$emit("simulation-update", response);
            });
        },
    },
    mounted () {
        for (var panel of this.panels) {
            for (var control of panel.controls) {
                this.parameters[control.id] = control.default;
            }
        }
    }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
