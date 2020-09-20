<template>
  <div class="visualization">
      <span> {{ simData }} </span>
  </div>
</template>

<script>

export default {
  name: 'Visualization',
  props: {
    simData: Object
  },
  data: function () {
    return {}
  },
  methods: {}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
span {
    font-size: 1.2em;
}
</style>
