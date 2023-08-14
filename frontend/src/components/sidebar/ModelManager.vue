<template>
    <div class="connection-manager py-0">
        <div class="header">
            Models
        </div>
        <div class="connection-list">
            <ModelConceptList v-if="activeModelFromConnection"  class="px-0" 
            :model="activeModelFromConnection.name" 
            :editor="activeEditor.name"
            :height="sidebarHeight - 160"/>
            <div class = "connection-list-item" v-else>No active model</div>
            <!-- <v-expansion-panels  theme="dark" variant="accordion">
                <v-expansion-panel class="px-0" v-for="model in models" :key="model.name">
                    <v-expansion-panel-title>
                        <div class="pl-4">{{ model.name }} </div>
                    </v-expansion-panel-title>
                    <v-expansion-panel-text class="px-0">
                        <ModelConceptList  class="px-0" :model="model.name" height="400"/>
                    </v-expansion-panel-text>
                </v-expansion-panel>
            </v-expansion-panels> -->
        </div>
        <div class="footer">
            <!-- <NewConnectionPopup /> -->
            <!-- <v-btn class="tab-btn pa-0 ba-0" v-bind="props" density="compact" block>Add Connection</v-btn> -->
        </div>
    </div>
</template>
<style local>
.header {
    color: var(--text-lighter);
    font-size: 1.0rem;
    height: 30px;
    min-height: 30px;
    line-height: 30px;
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



.editor-list {
    align-items: right;
    text-align: center;
    height: 25px;

}

.connection-list {
    display: 'flex';
    align-items: left;
    text-align: left;
    width: 100%;
    height: 100%;
    background-color: var(--light-bg-color-2);

}

.connection-list-item {
    height: 10px;
    font-size: 80%;
}

.connection-manager {
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

.connection-list {
    background-color: var(--main-bg-color);
}
</style>
<script>
import ModelConceptList from '/src/components/sidebar/model/ModelConceptList.vue'
import instance from '../../api/instance';
import { mapActions, mapGetters } from 'vuex';
export default {
    name: "ModelManager",
    components: {
        ModelConceptList
    },
    data() {
        return {
        };
    },
    computed: {
        ...mapGetters(['models', 'getConnectionByName', 'activeEditor', 'sidebarHeight']),
        activeConnection() {
            return this.getConnectionByName(this.activeEditor.connection)
        },
        activeModelFromConnection() {
            console.log(this.activeConnection)
            return this.models.find(todo => todo.name === this.activeConnection.model)

        }
    },
    methods: {
        ...mapActions([]),
    },
};
</script>
