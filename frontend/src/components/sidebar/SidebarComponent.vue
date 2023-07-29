<template>
    <div class="sidebar">
        <ConnectionManager/>
        <SidebarFooter/>
    </div>
</template>

<style>
.sidebar {
    background-color: var(--main-bg-color);
    display: flex;
    flex-direction: column;
    flex-grow: 0;
    flex-shrink: 1;
    /* flex-wrap: wrap; */
    height: 100%;
}
</style>

<script>
import ConnectionManager from './ConnectionManager.vue'
import SidebarFooter from './SidebarFooter.vue'
export default {
    name: "SidebarComponent",
    data() {
        return {
            connections: [{ 'name': 'duckdb' },
            { 'name': 'bigquery' }]
        };
    },
    components: {ConnectionManager, SidebarFooter}
};
</script>