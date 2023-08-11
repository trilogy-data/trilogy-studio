<template>
    <div class="sidebar">
        <div class="upper-parent">
            <div  class="selector-sidebar py-0 px-0">
                <SidebarSelector />
            </div>
            <div  class="content-sidebar pa-0">
                <ConnectionManager v-if="selectedItem == 'connections'" />
            </div>
        </div>
        <SidebarFooter />
    </div>
</template>

<style>
.selector-sidebar {
    background-color: rgba(0, 0, 0, 0.695);
    width: 40px;
}
.content-sidebar {
    flex: 1;
}
.upper-parent {
    display:flex;
    height: 100%;
}
.sidebar {
    background-color: var(--main-bg-color);
    display: flex;
    flex-direction: column;
    flex-grow: 0;
    flex-shrink: 1;
    /* flex-wrap: wrap; */
    height: 100%;
    width: 100%;
}
</style>

<script>
import ConnectionManager from './ConnectionManager.vue'
import SidebarFooter from './SidebarFooter.vue'
import SidebarSelector from './SidebarSelector.vue'
export default {
    name: "SidebarComponent",
    data() {
        return {
            connections: [{ 'name': 'duckdb' },
            { 'name': 'bigquery' }],
            selectedItem: 'connections'
        };
    },
    components: { ConnectionManager, SidebarFooter, SidebarSelector }
};
</script>