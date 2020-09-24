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

import Config from "./Config.js"

export default {
  name: "App",
  components: {
    ControlPanel,
    Visualization,
  },
  data: function () {
    return {
      simulateApi: Config.simulateApi,
      statusApi: Config.statusApi,
      resultsApi: Config.resultsApi,
      panels: Config.panels,
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
