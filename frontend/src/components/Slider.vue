<template>
    <b-form-group
      :label="`${name}: ${value}`"
      :description="description"
      for="input-small"
    >
        <b-form-input 
            id="range-1" type="range"
            min="-5" max="5" step="0.01"
            v-model="value"
        >
        </b-form-input>
    </b-form-group>
</template>

<script>
export default {
    name: "Slider",
    props: {
        id: String,
        name: String,
        description: String,
        default: Number
    },
    data: function () {
        return {
            value: this.default
        };
    },
    watch: {
        value (data) {
            this.$emit('slider-change', this.id, data);
        }
    },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
