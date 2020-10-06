<template>
    <b-card
    class="mb-2 w-50"
    style="max-width: 400px;"
    :title="'Dynamic incentives at step ' + (step + 1)">
        <b-container class="chart">
            <b-row h-align="start">
                <b-col cols="6">Low income</b-col>
                <b-col cols="2" style="text-align: right">{{lowIncome}}</b-col>
                <b-col cols="4">
                    <div class="bar" :style="{width: lowIncome + '%'}"></div>
                </b-col>
            </b-row>
            <b-row>
                <b-col cols="6">Less commuting</b-col>
                <b-col cols="2" style="text-align: right">{{lessCommuting}}</b-col>
                <b-col cols="4">
                    <div class="bar" :style="{width: lessCommuting * 10 + '%'}"></div>
                </b-col>
            </b-row>
            <b-row>
                <b-col cols="6">Small scale housing</b-col>
                <b-col cols="2" style="text-align: right">{{smallScaleHousing}}</b-col>
                <b-col cols="4">
                    <div class="bar" :style="{width: smallScaleHousing * 10 + '%'}"></div>
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
        lowIncome: {
            type: Number,
            default: 0
        },
        lessCommuting: {
            type: Number,
            default: 1
        },
        smallScaleHousing: {
            type: Number,
            default: 2
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
