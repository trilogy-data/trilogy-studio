<template>
    <div class="editor-entry pa-0 ba-0">
        <!-- <div ref="editor" class="debug"> EDITOR HERE</div> -->
        <div ref="editor">
            <v-tabs class="editor-tabs pa-0 ba-0" v-model="localEditor" center-active
                @update:modelValue="setActiveEditor(selectedEditor)">
                <v-tab class="editor-tab" v-for="n in editors" :key="n.name" :value="n.name">
                    {{ n.name }} <span class="text-light"> ({{ n.syntax }})</span>
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
        <div class="editor-results editor" ref="results">
            <template v-for="editor in editors">
                <EditorResults key="editor.name" v-if="editor.name == localEditor" :editorData="editor">
                </EditorResults>
            </template>
        </div>
    </div>
</template>
<style>
.debug {
    height: 500px;
    border: 1px solid red;
}

.editor-background {
    background-color: var(--main-bg-color);
    filter: brightness(65%);
    height: 100px;
}

.editor {
    background-color: var(--main-bg-color);
    filter: brightness(85%);
}

.editor-entry {
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    flex: 1 1 100%;
    height: 100%;
}

.editor-results {
    display: flex;
    flex-direction: column;
    flex-grow: 0;
    flex-shrink: 1;
    /* flex-wrap: wrap; */
    height: 100%;
}

.editor-tabs {
    height: 30px;
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
        store.watch(
            (state) => state.activeEditor,
            (newValue) => {
                console.log(newValue)
                localEditor.value = newValue;
            }
        );

        store.watch((state, getters) => getters.activeEditor, () => {
            console.log('active')
            console.log(store.getters['activeEditor'])
            localEditor.value = store.getters['activeEditor'].name
            console.log(`value changes detected via vuex watch`);
        })
        onMounted(() => {
            const self = getCurrentInstance().proxy;
            self.split = Split([self.$refs.editor, self.$refs.results], {
                // elementStyle: (_dimension, size) => ({
                //     "flex-basis": `calc(${size}%)`,
                // }),
                direction: 'vertical',
                sizes: [50, 50],
                minSize: 200,
                expandToMin: true,
                gutterSize: 0,
            });
            // this.createEditor()
        })

        return {
            editors,
            setActiveEditor,
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