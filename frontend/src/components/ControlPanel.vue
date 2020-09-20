<template>
    <div class="control-panel">
        <button
            :disabled="running"
            @click="runSimulation"
        >{{ running ? "Running...": "Run Simulation" }}</button>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "ControlPanel",
    props: {
        simulationApi: String,
        statusApi: String,
        resultsApi: String,
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
button {
    padding: 1em;
    padding-left: 1.5em;
    padding-right: 1.5em;
    border-radius: 0.3em;

    font-size: 1.2em;
    background: rgb(7, 190, 166);
    color: white;

    cursor: pointer;

    transition: width 0.5s ease-in-out;
}

button:active {
    background: rgb(14, 113, 126);
}

button:disabled {
    background: rgb(134, 201, 192);
}
</style>
