<template>
    <div class="incentive-panel">
        <div>
            <p class="title">Equity WITHOUT Zoning</p>
            <p class="description">
                Please select one of the three <b>incentive policy scenarios</b> and run the <b>simulation</b> below.
            </p>
        </div>

        <b-dropdown id="dropdown-1" 
            class="m-1" size="sm"
            :text="incentiveModes[currentMode]" >
            <b-dropdown-item @click="$emit('incentive-update', 0)">No incentives</b-dropdown-item>
            <b-dropdown-item @click="$emit('incentive-update', 1)">Static incentives</b-dropdown-item>
            <b-dropdown-item @click="$emit('incentive-update', 2)">Dynamic incentives</b-dropdown-item>
        </b-dropdown>
    </div>
</template>

<script>

export default {
    name: "IncentivePanel",
    props: {
        incentiveModes: Array,
        currentMode: {
            type: Number,
            default: 0
        }
    }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.incentive-panel {
    color: white;
    margin-bottom: 2em;
}

p.title {
    font-size: 1.7em;
    font-weight: 800;
    margin-bottom: 0.2em;
}

p.description {
    font-size: 0.8em;
}

.dropdown {
    margin: 0 !important;
}

#dropdown-1__BV_toggle_ {
    background: #2F2F2F;
    border: 1px solid #717171;
}

</style>
