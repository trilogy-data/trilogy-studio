<template>
    <div class="connection-manager py-0">
        <!-- <v-select class="connection-selector"  density="compact" v-model="selectedConnection"
            :items="connections" item-value="name" item-title="name">
        </v-select> -->
        <div class="header">
            Connections
        </div>
        <div class="connection-list">

            <v-expansion-panels theme="dark" variant="accordion">
                <v-expansion-panel v-for="connection in connections" :key="connection.name" >
                    <v-expansion-panel-title>
                        <GlowingDot v-if="connection.active" />    {{ connection.name }}
                    </v-expansion-panel-title>
                 <div @click="setActiveEditor(editor.name)" v-for="editor in editors[connection.name]" 
                 class="editor-list">
                    {{ editor.name }}
                 </div>
                </v-expansion-panel>
            </v-expansion-panels>
        </div>
        <div class="footer">
            <v-btn class="tab-btn pa-0 ba-0" v-bind="props" density="compact" block>Add Connection</v-btn>
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

.connection-button .v-field {
    color: var(--text-lighter);
    font-size: 16px;
    height: 10px;
}

.v-field {
    color: var(--text-lighter);
    font-size: 14px;
    background-color: var(--light-bg-color-2);
    height: 44px;
    border-radius: 0;
}

/* vuetify select customizations */
.v-input {
    color: var(--text-lighter);
    font-size: 14px;
    background-color: var(--light-bg-color-2);
    /* height: 30px; */
}

.v-list-item__title {
    color: blue;
}

.v-menu {
    color: var(--text-lighter);
    /* background-color: var(--light-bg-color-2);  */
    font-size: 14px;
}

.connection-selector {
    color: var(--text-lighter) !important;
    background-color: var(--light-bg-color-2);
    /* height:10px; */
    font-size: 80%;
    align-items: left;
    text-align: left;
    border-radius: 0px;

}

.editor-list {
    align-items: right;
    text-align: right;
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



.title {
    color: var(--text-lighter);
    font-size: 95%;
    margin-bottom: 5px;
}

.connection-list {
    background-color: var(--main-bg-color);
}
</style>
<script>
import GlowingDot from '/src/components/generic/GlowingDot.vue';

import instance from '../../api/instance';
import { mapActions, mapGetters } from 'vuex';
export default {
    name: "ConnectionManager",
    components: {
        GlowingDot
    },
    data() {
        return {
            selectedConnection: "duckdb_demo"
        };
    },
    computed: {
        ...mapGetters(['activeEditor', 'connections']),
        editors() {
            let editors = {}
            this.connections.forEach((conn) => {
                editors[conn.name] = this.$store.getters.editors.filter((editor) => {
                    return editor.connection == conn.name
                })
            })
            return editors
        }
    },
    methods: {
        ...mapActions(['setActiveConnection', 'setActiveEditor']),
        setConnection(conn) {
            this.setActiveConnection(conn.name)
            console.log(`connection set to ${conn.name}`)
        },
        addConnection() {
            let local = this;
            return instance.post('connection', {
            }).then(() => {
                console.log('add connection')

            })
        },
        removeConnection() {
            let local = this;
            return instance.post('connection', {
            }).then(() => {
                console.log('add connection')

            })
        },
        loadConnections() {
            let local = this;
            return instance.get('connections', {
            }).then((response) => {
                this.connections = response.connections

            })
        },
    },
    mounted() {
        //    this.loadConnections()
    },
};
</script>
