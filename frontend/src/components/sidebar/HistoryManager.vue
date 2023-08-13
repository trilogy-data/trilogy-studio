<template>
    <div class="connection-manager py-0">
        <div class="header">
            History
        </div>
        <div class="connection-list">

            <v-expansion-panels theme="dark" variant="accordion">
                <v-expansion-panel v-for="connection in connections" :key="connection.name">
                    <v-expansion-panel-title>
                        <GlowingDot class="" v-if="connection.active" />
                        <div class="pl-4">{{ connection.name }}</div>
                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                        TODO
                        <!-- <div @click="setActiveEditor(editor.name)" v-for="editor in editors[connection.name]"
                            class="editor-list">
                            {{ editor.name }}
                        </div>
                        <div>
                            <NewEditorPopup :defaultConnection="connection.name" />
                        </div> -->
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
import GlowingDot from '/src/components/generic/GlowingDot.vue';
import NewConnectionPopup from '/src/components/sidebar/NewConnectionPopup.vue';
import NewEditorPopup from '/src/components/editor/NewEditorPopup.vue'
import instance from '../../api/instance';
import { mapActions, mapGetters } from 'vuex';
export default {
    name: "ConnectionManager",
    components: {
        GlowingDot,
        NewConnectionPopup,
        NewEditorPopup
    },
    data() {
        return {
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
        ...mapActions(['setActiveConnection', 'setActiveEditor', 'loadConnections']),
        setConnection(conn) {
            this.setActiveConnection(conn.name)
        },
    },
    mounted() {
        this.loadConnections()
    },
};
</script>
