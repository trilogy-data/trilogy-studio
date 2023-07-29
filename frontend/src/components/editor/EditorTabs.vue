<template>
    <v-tabs class="editor-tabs pa-0 ba-0" v-model="selectedEditor" @update:modelValue="setActiveEditor(selectedEditor)">
        <v-tab class="editor-tab" v-for="n in editors" :key="n.name" :value="n.name">
            {{ n.name }}
        </v-tab>
        <v-tab class="editor-tab editor-tab-add">
            <v-btn class="tab-btn pa-0 ba-0" density="compact" block icon="mdi-plus" @click="handleButtonClick">
                +
            </v-btn>
        </v-tab>
    </v-tabs>
    <template v-for="editor in editors">
        <EditorComponent key="editor.name" v-if="editor.name == activeEditor.name" :editorData="editor">
        </EditorComponent>
    </template>
</template>
<style>
.editor-tabs {
    height: 30px;
    background-color: var(--main-bg-color);

}

.editor-tab-add.v-slide-group {
    width:20px
}
.editor-tab.v-slide-group {
    height: 30px;
}

.tab-icon {
    height:20px;
}
.tab-btn {
    height: 30px;
    text-transform: none;
    color: var(--text-lighter);
    background-color: var(--main-bg-color);
}

.editor-tab.v-btn {
    height: 30px;
    text-transform: none;
    color: var(--text-lighter);
}

.editor-tab {
    height: 10px;
    font-size: .8rem;
    color: var(--text-lighter);
}
</style>
<script>
import EditorComponent from './EditorComponent.vue'
import { computed } from 'vue'
import { useStore } from 'vuex'
// import { Component, Prop, Vue } from 'vue-property-decorator'
export default {
    components: { EditorComponent },
    setup() {

        const store = useStore()
        const selectedEditor = store.getters['editors'];
        const editors = computed(() => store.getters['editors'])
        const activeEditor = computed(() => store.getters['activeEditor'])
        const setActiveEditor = (tab) => store.dispatch('setActiveEditor', tab)
        return {
            editors,
            selectedEditor,
            activeEditor,
            setActiveEditor
        }


    }
}
</script>