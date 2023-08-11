<template>
    <div class="sidebar-selectors py-2 px-0">
        <template v-for="link in links">
            <div class="sidebar-selector-nav-item py-2 px-0">
                <v-btn size="x-small" variant="outlined" @click.prevent="click(link.name)" :icon="link.icon">
                </v-btn>
                <!-- <v-icon @click.prevent="click(link.name)">{{link.icon}}</v-icon> -->
                <!-- <a href="" @click.prevent="click(link.name)" class="selectable"
                    :class="{ active: activeItem === 'connections2' }" :title="link.name">
                    
                </a> -->
            </div>
        </template>

    </div>
</template>
<style>
.sidebar-selectors {
    display: flex;
    flex-direction: column;
    font-size: 110%;
    color: var(--text-lighter);
}

.sidebar-selector-nav-item {
    flex: 1;
    width: 100%;
}
</style>
  
<script>
export default {
    props: ['activeItem'],
    data() {
        return {
            links: [{ 'name': 'Databases', 'icon': 'mdi-database' },
            { 'name': 'History', 'icon': 'mdi-history' },
            { 'name': 'Other', 'icon': 'mdi-dots-horizontal' }
            ],
            selectedItem: 'connections'
        }
    },
    components: {},
    computed: {
    },
    methods: {
        click(item) {
            if (this.activeItem === item) {
                this.$emit('toggleSidebar')
            } else {
                this.$emit('selected', item)
            }
        }
    }
}
</script>