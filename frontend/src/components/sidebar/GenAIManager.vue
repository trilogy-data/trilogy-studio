<template>
    <div class="history-manager py-0">
        <div class="sidebar-header">
            GenAI Connections
        </div>
        <div class="connection-list">

            <v-expansion-panels v-model="selectedPanel" theme="dark">
                <v-expansion-panel class="square-corner" 
                v-for="connection in genAIConnections" :key="connection.name"
                    :value="connection.name">
                    <v-expansion-panel-title :key="connection.name">
                        <GlowingDot class="" v-if="connection.active" />
                        <div class="pl-4">{{ connection.name }}</div>

                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                        <GenAIPanel :connection="connection"></GenAIPanel>
                        <v-toolbar height="24" extension-height="24" class="sidebar-button-list align-right">
                            <!-- <EditConnectionPopup :connection="connection" />
                    <RemoveConnectionPopup :connection="connection" />
                    <NewEditorPopup :defaultConnection="connection.name" /> -->
                    <v-btn :disabled="true"
                        icon="mdi-pencil"
                        class="sidebar-action-button pa-0 ba-0" density="compact">
                    </v-btn> 
                    <RemoveConnectionPopup :connection="connection" />
                     <v-btn :disabled="true"
                        icon="mdi-refresh"
                        class="sidebar-action-button pa-0 ba-0" density="compact">
                    </v-btn> 
                        </v-toolbar>
                    </v-expansion-panel-text>
                </v-expansion-panel>
            </v-expansion-panels>
        </div>

        <div class="footer">
            <NewConnectionPopup />
            <!-- <v-btn class="tab-btn pa-0 ba-0" v-bind="props" density="compact" block>Add Connection</v-btn> -->
        </div>
    </div>
</template>
<style local>
.failed {
    color: var(--text-error);
}

.footer {
    --height: 20px;
    font-size: 0.8rem;
    background-color: black;
    height: var(--height);
    min-height: var(--height);
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    color: var(--text-lighter);

}

.history-list-item {
    align-items: right;
    text-align: center;
    height: 25px;
}

.history-list {
    display: 'flex';
    align-items: left;
    text-align: left;
    width: 100%;
    height: 100%;
    background-color: var(--light-bg-color-2);
    background-color: var(--main-bg-color);

}


.history-manager {
    height: 100%;
    display: flex;
    flex-direction: column;
    flex-basis: 100%;
    flex-grow: 1;
    flex-shrink: 1;
    flex: 1 1 100%;
    flex-wrap: nowrap;
    width: 100%;
    font-size: .8rem;
}
</style>
<script lang="ts">
// @ts-ignore
import GlowingDot from '/src/components/generic/GlowingDot.vue';
import NewConnectionPopup from '/src/components/sidebar/genai/NewConnectionPopup.vue';
import RemoveConnectionPopup from '/src/components/sidebar/genai/RemoveConnectionPopup.vue';
import GenAIPanel from '/src/components/sidebar/genai/ConnectionSubpanel.vue';
export default {
    name: "GenAIManager",
    components: {
        GlowingDot,
        NewConnectionPopup,
        RemoveConnectionPopup,
        GenAIPanel
    },
    data() {
        return {
            modalVisible: false,
            selectedPanel: '',
        };
    },
    computed: {
        genAIConnections() {
            return this.$store.getters.genAIConnections
        }
    },
    methods: {
    },
    mounted() {
        console.log(this.genAIConnections)
    },
};
</script>
