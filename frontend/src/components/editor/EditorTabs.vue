<template>
    <div class="editor-entry pa-0 ba-0">
        <!-- <div ref="editor" class="debug"> EDITOR HERE</div> -->
        <div ref="editor">
            <v-tabs class="editor-tabs pa-0 ba-0" v-model="selectedEditor"
                @update:modelValue="setActiveEditor(selectedEditor)">
                <v-tab class="editor-tab" v-for="n in editors" :key="n.name" :value="n.name">
                    {{ n.name }}
                </v-tab>
                <v-tab class="editor-tab editor-tab-add">
                    <v-btn class="tab-btn pa-0 ba-0" 
                    density="compact"
                     block icon="mdi-plus" @click.stop="addNewTab">
                        +
                    </v-btn>
                </v-tab>
            </v-tabs>
            <template v-for="editor in editors">
                <EditorEditor class="editor-entry" key="editor.name" 
                v-if="editor.name == activeEditor.name" 
                :editorData="editor">
                </EditorEditor>
            </template>
        </div>
        <div class="editor-results editor" ref="results">
            <template v-for="editor in editors">
                <EditorResults key="editor.name" 
                v-if="editor.name == activeEditor.name" 
                :editorData="editor">
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
    height:100px;
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
import EditorEditor from './EditorEditor.vue'
import EditorResults from './EditorResults.vue'
import { computed, ref, onMounted, getCurrentInstance} from 'vue'
import { useStore } from 'vuex'
import Split from 'split.js'
// import { Component, Prop, Vue } from 'vue-property-decorator'
export default {
    components: {  EditorEditor, EditorResults },
    setup() {
        const editor = ref(null);
        const results = ref(null);
        const store = useStore()
        const selectedEditor = store.getters['editors'];
        const editors = computed(() => store.getters['editors'])
        const activeEditor = computed(() => store.getters['activeEditor'])
        const setActiveEditor = (tab) => store.dispatch('setActiveEditor', tab)

        const addNewTab = () => {
            console.log('clicked new tab')

        };
        onMounted(() => {
        const self = getCurrentInstance().proxy;
        console.log(self)
        console.log("refEditor")
        console.log(self.$refs)
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
            selectedEditor,
            activeEditor,
            setActiveEditor,
            // functions
            addNewTab,
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