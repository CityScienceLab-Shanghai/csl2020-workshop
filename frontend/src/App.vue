<template>
  <div id="app">
    <b-container fluid>
      <b-row>
        <b-col>
          <ControlPanel 
          :panels="panels"
          :simulateApi="simulateApi"
          :statusApi="statusApi"
          :resultsApi="resultsApi"
          @simulation-update="simulationData = $event" />
        </b-col>
        <b-col cols="6">
          <Visualization :sim-data="simulationData" />
        </b-col>
        <b-col></b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import Vue from "vue";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
// Install BootstrapVue
Vue.use(BootstrapVue);
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin);
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

import ControlPanel from "./components/ControlPanel.vue";
import Visualization from "./components/Visualization.vue";

export default {
  name: "App",
  components: {
    ControlPanel,
    Visualization,
  },
  data: function () {
    return {
      simulateApi: "",
      statusApi: "",
      resultsApi: "",
      panels: [
        {
          name: "Agent preferences",
          description: "Settings like preference for moving, commute distance, and house prices.",
          controls: [
            {
              id: "b_move_low_inc",
              name: "Moving",
            },
            {
              id: "b_commute_distance_low_inc",
              name: "Commute distance",
            },
            {
              id: "b_large_size_low_inc",
              name: "Large size",
            },
            {
              id: "b_price_low_low_inc",
              name: "Low price",
            },
            {
              id: "b_pop_density_low_inc",
              name: "Low population density",
            },
            {
              id: "b_inc_disparity_low_inc",
              name: "Low income disparity",
            },
          ],
        },
      ],
      simulationData: {},
    };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}

.container {
  margin: 0px;
  width: 100%;
}
</style>
