<template>
    <b-card
    class="mb-2 w-50"
    style="max-width: 400px;"
    :title="'Dynamic incentives at step ' + (step + 1)">
        <b-container class="chart">
            <b-row h-align="start">
                <b-col cols="6">Low income</b-col>
                <b-col cols="3" style="text-align: right">{{ policy[0].toFixed(2) }}</b-col>
                <b-col cols="3">
                    <div class="bar" :style="{width: policy[0] * 100 + '%'}"></div>
                </b-col>
            </b-row>
            <b-row>
                <b-col cols="6">Less commuting</b-col>
                <b-col cols="3" style="text-align: right">{{ policy[1].toFixed(2) }}</b-col>
                <b-col cols="3">
                    <div class="bar" :style="{width: policy[1] * 100 + '%'}"></div>
                </b-col>
            </b-row>
            <b-row>
                <b-col cols="6">Small scale housing</b-col>
                <b-col cols="3" style="text-align: right">{{ policy[2].toFixed(2) }}</b-col>
                <b-col cols="3">
                    <div class="bar" :style="{width: policy[2] * 100 + '%'}"></div>
                </b-col>
            </b-row>
        </b-container>
    </b-card>
</template>

<script>

export default {
    name: "DynamicPolicy",
    props: {
        step: {
            type: Number,
            default: 12
        },
        policy: {
            type: Array,
            default: () => [0, 0, 0]
        }
    }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.card {
    border: #979797;
}

.card-body {
    background: black;
    border: 1px solid #979797;
    border-radius: 0.25rem;
    font-size: 0.9em !important;
    color: white;
    /* text-overflow: ellipsis;
    overflow: hidden; 
    white-space: nowrap; */
}

.card-title {
    color: white !important;
    font-size: 1.5em !important;
}

.card-subtitle.text-muted {
    color: white !important;
    font-size: 0.9em !important;
    font-weight: 100;
}

.bar {
    position: absolute;
    top: 0;
    left: 0;
    height: 1.2em;
    background-color: #303030;
    border: 1px solid #979797;
    padding: 0px;
}

.col-6,.col-4 {
    padding: 0px;
    padding-right: 0.25rem;
}
</style>
