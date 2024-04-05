<template>
    <div class="history-manager py-0">
        <div class="sidebar-header">
            GenAI Connections
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
export default {
    name: "GenAIManager",
    components: {
        GlowingDot,
    },
    data() {
        return {
            modalVisible: false,
        };
    },
    computed: {
    },
    methods: {
    },
    mounted() {
    },
};
</script>
