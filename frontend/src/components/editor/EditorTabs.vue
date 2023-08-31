<template>
    <div class="editor-wrapper pa-0 ba-0">
        <div ref="editor">
            <v-tabs class="editor-tabs pa-0 ba-0" v-model="localEditor" center-active
                @update:modelValue="setActiveEditor()">
                <v-tab class="editor-tab" v-for="n in editors" :key="n.name" :value="n.name">
                    {{ n.name }} <span class="text-light"> ({{ n.syntax }})</span>
                    <div class="editor-tab close-button pl-4">
                        <v-btn size="compact" @click="closeEditor(n)" class="editor-tab close-button pa-0" height="20"
                            width="10">
                            <v-icon class="editor-tab close-button" height="10" width="5">mdi-close</v-icon>
                        </v-btn>
                    </div>
                </v-tab>
                <v-tab class="editor-tab editor-tab-add">
                    <NewEditorPopup></NewEditorPopup>
                </v-tab>
            </v-tabs>
            <template v-for="editor in editors">
                <EditorEditor class="editor-entry" key="editor.name" v-if="editor.name == localEditor" :editorData="editor">
                </EditorEditor>
            </template>
        </div>
        <div class="editor-results editor-color" ref="results">
            <template v-for="editor in editors">
                <EditorResults :key="editor.name" v-if="editor.name == localEditor" :editorData="editor">
                </EditorResults>
            </template>
        </div>
    </div>
</template>
<style scoped>
.close-button {
    width: 10px !important;
    color: var(--text-lighter);
    background-color: var(--main-bg-color);
    display: flex;
    align-items: center;
}

.editor-background {
    background-color: var(--main-bg-color);
    filter: brightness(65%);
    height: 100px;
}

.editor-color {
    background-color: var(--main-bg-color);
    filter: brightness(85%);
}
.editor-wrapper {
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    /* flex: 1 1 100%; */
    height: 100%;
}

.editor-entry {
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    /* flex: 1 1 calc(100%-60px); */
    height: calc(100% - 24x);
}

.editor-results {
    display: flex;
    flex-direction: column;
    flex-grow: 0;
    flex-shrink: 1;
    /* flex-wrap: wrap; */
    height: calc(100%-24px);
}

.editor-tabs {
    height: 24px;
    background-color: var(--main-bg-color);

}

.editor-tab-add.v-slide-group {
    width: 20px
}

.editor-tab.v-slide-group {
    height: 30px;
}

.tab-icon {
    height: 20px;
}

.editor-tab.v-btn {
    height: 24px;
    text-transform: none;
    color: var(--text-lighter);
    background-color: var(--main-bg-color);

}

.editor-tab {
    height: 10px;
    font-size: .7rem;
    color: var(--text-lighter);
}
</style>
<script lang="ts">
import EditorEditor from './EditorEditor.vue'
import EditorResults from './EditorResults.vue'
import NewEditorPopup from './NewEditorPopup.vue'
import { computed, ref, onMounted, getCurrentInstance } from 'vue'
import { useStore, } from 'vuex'
import Split from 'split.js'
// import { Component, Prop, Vue } from 'vue-property-decorator'
export default {
    components: { EditorEditor, EditorResults, NewEditorPopup },
    setup() {
        const editor = ref(null);
        const results = ref(null);
        const localEditor = ref("");
        const store = useStore()
        localEditor.value = store.getters['activeEditor'];
        const editors = computed(() => store.getters['editors'])
        const setActiveEditor = () => store.dispatch('setActiveEditor', localEditor.value)
        const closeEditor = (editor) => store.dispatch('closeEditor', editor)
        store.watch(
            (state) => state.activeEditor,
            (newValue) => {
                localEditor.value = newValue;
            }
        );

        store.watch((_, getters) => getters.activeEditor, () => {
            localEditor.value = store.getters['activeEditor'].name
        })
        onMounted(() => {
            const instance = getCurrentInstance();
            if (!instance) {
                return
            }
            const self = instance.proxy;
            // @ts-ignore
            self.split = Split([self.$refs.editor, self.$refs.results], {
                // elementStyle: (_dimension, size) => ({
                //     "flex-basis": `calc(${size}%)`,
                // }),
                direction: 'vertical',
                sizes: [50, 50],
                minSize: 200,
                expandToMin: true,
                gutterSize: 0
            });
            // this.createEditor()
        })

        return {
            editors,
            setActiveEditor,
            closeEditor,
            localEditor,
            // functions
            // refs
            editor,
            results
        }


    },
    // splitElements() {
    //         return [
    //             this.$refs.editor,
    //             this.$refs.results
    //         ];
    //     },

}
</script>