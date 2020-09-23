<template>
    <div class="control-panel">
        <PanelPane
            :name="'Agent preferences'"
            :description="'Settings like preference for moving, commute distance, and house prices.'"
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
        simulationApi: String,
        statusApi: String,
        resultsApi: String,
    },
    components: {
        PanelPane,
    },
    data: function () {
        return {
            running: false, // Whether the simulation is currently running
        };
    },
    methods: {
        // Send params to GAMA and start simulation
        runSimulation() {
            console.log("Running simulation");

            axios.get("").then(() => {
                this.running = true;
                this.startHeartBeat();
            });
        },

        // Start a heartbeat checking for completion once per second
        startHeartBeat() {
            var heartbeat = setInterval(() => {
                axios.get("").then(() => {
                    this.running = false;
                    clearInterval(heartbeat);
                    this.getResults();
                });
            }, 1000);
        },

        // Get simulation results and publish an event to update all data
        getResults() {
            axios.get("").then((response) => {
                this.$emit("simulation-update", response);
            });
        },
    },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
