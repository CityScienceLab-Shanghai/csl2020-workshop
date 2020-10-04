<template>
    <b-form-group
      :label="`${name}: ${value}`"
      :description="description"
      for="input-small"
    >
        <b-form-input 
            id="range-1" type="range"
            :min="min"
            :max="max" 
            :step="step"
            :disabled="disabled"
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
        default: Number,
        step: {
            type: Number,
            default: 0.01
        },
        min: {
            type: Number,
            default: -5
        },
        max: {
            type: Number,
            default: 5
        },
        disabled: {
            type: Boolean,
            default: false
        }
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
.custom-range {
    height: 1rem;
}
</style>
