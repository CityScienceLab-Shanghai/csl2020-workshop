<template>
    <b-card style="margin-bottom: 0.5em;" 
        title="Incentive policy"
        sub-title="You can choose from three different policies: no incentives (baseline model), static incentives, and dynamic incentives.">

        <b-dropdown id="dropdown-1" 
            block
            class="m-2"
            menu-class="w-100"
            variant="primary"
            :text="incentiveModes[currentMode]" >
            <b-dropdown-item @click="$emit('incentive-update', 0)">No incentives</b-dropdown-item>
            <b-dropdown-item @click="$emit('incentive-update', 1)">Static incentives</b-dropdown-item>
            <b-dropdown-item @click="$emit('incentive-update', 2)">Dynamic incentives</b-dropdown-item>
        </b-dropdown>
        <!-- 
        <b-nav pills fill small>
            
            <b-nav-item active>None</b-nav-item>
            <b-nav-item>Static</b-nav-item>
            <b-nav-item>Dynamic</b-nav-item>
        </b-nav> -->
    </b-card>
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
.b-card {
    padding-top: 10em;
}
</style>
