<template>
  <div id="app">
    <b-container>
      <b-row>
        <b-col>
          <ControlPanel @simulation-update="simulationData = $event"/>
        </b-col>
        <b-col>
          <Visualization :sim-data="simulationData"/>
        </b-col>
        <b-col></b-col>
      </b-row>
    </b-container>
    
    
  </div>
</template>

<script>
import Vue from 'vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import ControlPanel from './components/ControlPanel.vue'
import Visualization from './components/Visualization.vue'

export default {
  name: 'App',
  components: {
    ControlPanel,
    Visualization
  },
  data: function () {
    return {
      simulationData: {},
    }
  }
}
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
}
</style>
