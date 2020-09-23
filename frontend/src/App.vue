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
        <b-col cols="7">
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
          name: "Low-income residents",
          description: "Describes the preferences of low-income residents, like moving, commute distance, and house prices.",
          controls: [
            {
              id: "b_move_low_inc",
              name: "Moving",
              default: -1.43
            },
            {
              id: "b_commute_distance_low_inc",
              name: "Commute distance",
              default: -0.88
            },
            {
              id: "b_large_size_low_inc",
              name: "Large size",
              default: 0.24
            },
            {
              id: "b_price_low_low_inc",
              name: "Low price",
              default: -0.002
            },
            {
              id: "b_pop_density_low_inc",
              name: "Low population density",
              default: -0.0056
            },
            {
              id: "b_inc_disparity_low_inc",
              name: "Low income disparity",
              default: -0.21
            },
          ],
        },
        {
          name: "High-income residents",
          description: "Describes the preferences of high-income residents.",
          controls: [
            {
              id: "b_move_high_inc",
              name: "Moving",
              default: -1.29
            },
            {
              id: "b_commute_distance_high_inc",
              name: "Commute distance",
              default: -0.81
            },
            {
              id: "b_large_size_high_inc",
              name: "Large size",
              default: 0.52
            },
            {
              id: "b_price_low_high_inc",
              name: "Low price",
              default: -0.0006
            },
            {
              id: "b_pop_density_high_inc",
              name: "Low population density",
              default: -0.0123
            },
            {
              id: "b_inc_disparity_high_inc",
              name: "Low income disparity",
              default: -0.52
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
  margin-top: 1em;
}

.container {
  margin: 0px;
  width: 100%;
}
</style>
