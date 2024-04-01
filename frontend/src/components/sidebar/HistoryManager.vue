<template>
    <div class="history-manager py-0">
        <div class="header">
            History
        </div>
        <modal v-if="modalVisible" @close="modalVisible = false" :data="modalData"/>
        <div class="history-list">

            <v-expansion-panels theme="dark" variant="accordion">
                <v-expansion-panel v-for="connection in history" :key="connection.name">
                    <v-expansion-panel-title>
                        <div class="pl-4">{{ connection.name }}</div>
                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                        <div @click="setActiveEditor(event.editor)"
                         v-for="event in connection.events"
                            :class="{ failed: event.error }"
                            class="history-list-item">
                            <span v-if="event.duration">{{ event.editor }} ({{event.duration}} ms)</span>
                            <span v-else>{{ event.editor }}</span>
                        </div>
                        <!-- <div>
                            <NewEditorPopup :defaultConnection="connection.name" />
                        </div> -->
                    </v-expansion-panel-text>
                </v-expansion-panel>
            </v-expansion-panels>
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
import { mapActions, mapGetters } from 'vuex';
export default {
    name: "HistoryManager",
    components: {
        GlowingDot,
    },
    data() {
        return {
            modalVisible: false,
        };
    },
    computed: {
        ...mapGetters(['activeEditor', 'connections', 'history']),
    },
    methods: {
        ...mapActions(['setActiveEditor']),
    },
    mounted() {
    },
};
</script>
