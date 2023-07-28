<template>
    <div class="sidebar">
        <ConnectionManager/>
    </div>
</template>

<style>
.sidebar {
    background-color: var(--main-bg-color);
}
</style>

<script>
import ConnectionManager from './ConnectionManager.vue'
export default {
    name: "SidebarComponent",
    data() {
        return {
            connections: [{ 'name': 'duckdb' },
            { 'name': 'bigquery' }]
        };
    },
    components: {ConnectionManager}
};
</script>