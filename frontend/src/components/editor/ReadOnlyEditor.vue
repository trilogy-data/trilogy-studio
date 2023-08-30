<template>
    <div id="ro-editor" class="editor-fix-styles">
    </div>
</template>

<style scoped>
.editor-fix-styles {
    text-align: left;
    border: none;
}
</style>
<script lang="ts">
import { defineComponent } from 'vue';
import * as monaco from 'monaco-editor';

export default defineComponent({
    name: 'ReadOnlyEditorDisplay',
    props: {
        content: { type: String }
    },
    data() {
        return {
            editor: null,
            editorX: 400,
            editorY: 400,
            
        }
    },
    components: {
    },
    mounted() {
        this.createEditor()
    },
    computed: {

    },
    methods: {
        createEditor() {
            const editor = monaco.editor.create(document.getElementById('ro-editor'), {
                value: this.content,
                language: 'sql',
                automaticLayout: true,
            })
            this.editor = editor;
            monaco.editor.defineTheme('preqlStudio', {
                base: 'vs-dark', // can also be vs-dark or hc-black
                inherit: true, // can also be false to completely replace the builtin rules
                rules: [
                    { token: 'comment', foreground: 'ffa500', fontStyle: 'italic underline' },
                    { token: 'comment.js', foreground: '008800', fontStyle: 'bold' },
                    { token: 'comment.css', foreground: '0000ff' } // will inherit fontStyle from `comment` above
                ],
                colors: {
                    // 'editor.foreground': '#F8F8F8',
                    // 'editor.background': '#000000',
                    // 'editorCursor.foreground': '#8B0000',
                    // 'editor.lineHighlightBackground': '#0000FF20',
                    // 'editorLineNumber.foreground': '#008800',
                    // 'editor.selectionBackground': '#88000030',
                    // 'editor.inactiveSelectionBackground': '#88000015'
                }
            });
            monaco.editor.setTheme('preqlStudio');
            // editor.onDidChangeModelContent(() => {
            //     this.content = editor.getValue();
            // });
            

        }
    }
})
</script>
  