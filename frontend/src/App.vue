<template>
  <div id="app">
    <ControlPanel @simulation-update="simulationData = $event"/>
    <Visualization :sim-data="simulationData"/>
  </div>
</template>

<script>
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
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
