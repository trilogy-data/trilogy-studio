<template>
    <div :key="editorData.name" ref="editor" id="editor" class="editor-fix-styles">
        <!-- <div id="editor" > </div> -->
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
import { mapGetters, mapActions } from 'vuex';
import editorMap from '/src/store/modules/monaco';
import axiosHelpers from '/src/api/helpers.ts';
import { Editor, RawEditor } from '/src/models/Editor'
import * as monaco from 'monaco-editor';


export default defineComponent({
    name: 'EditorEditor',
    props: {
        editorData: {
            type: [Editor, RawEditor],
        }
    },
    data() {
        return {
            // result: null,
            // error: null,
            // loading: false,
            last_passed_query_text: null,
            form: null,
            prompt: '',
            generatingPrompt: false,
            info: 'Query processing...',
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
        ...mapGetters(['getConnectionByName', 'activeGenAIConnection']),
        connection() {
            return this.getConnectionByName(this.editorData.connection)
        },
        error() {
            return this.editorData.error
        },
        loading() {
            return this.editorData.loading
        },
        result() {
            return this.editorData.results
        },
        passedQuery() {
            return this.editorData.contents === this.last_passed_query_text
        },
        generateOverlayVisible() {
            return this.prompt.length > 1 || this.generatingPrompt
        }

    },
    methods: {
        ...mapActions(['saveEditors', 'saveEditorText', 'formatEditorText', 'connectConnection', 'addMonacoEditor',
            'setConnectionInactive', 'addHistory', 'setEditorError']),
        async submitGenAI(selection: String) {
            this.info = 'Generating Trilogy query from prompt...'
            let response = await this.editorData.runGenAIQuery(this.$store, this.activeGenAIConnection.name, selection);
            return response
        },
        async submit() {
            // this.loading = true;
            this.info = 'Executing query...'
            const start = new Date()
            // todo: set this in a action
            this.editorData.loading = true;
            // this.error = null;
            let current_query = this.editorData.contents;
            if (!this.connection) {
                this.setEditorError({ name: this.editorData.name, error: 'No connection selected for this editor.' })
                return
            }
            // invalidation of logic
            if (!this.connection.active) {
                try {
                    await this.connectConnection(this.connection)
                }
                catch (error) {
                    this.setEditorError({ name: this.editorData.name, error: 'Error with connection.' })

                }

            }

            await this.editorData.runQuery(this.$store);

            this.addHistory({
                connection: this.editorData.connection,
                text: this.editorData.contents,
                editor: this.editorData.name,
                timestamp: start,
                duration: this.editorData.duration,
                executed: this.editorData.executed,
                error: this.editorData.error
            })

            this.last_passed_query_text = current_query;
        },
        createEditor() {
            let editorElement = document.getElementById('editor')
            if (!editorElement) {
                return
            }
            const editor = monaco.editor.create(editorElement, {
                value: this.editorData.contents,
                language: 'sql',
                automaticLayout: true,
            })
            this.editor = editor;
            editorMap.set(this.editorData.name, editor)
            // this.addMonacoEditor({ editor: editor, name: this.editorData.name })
            // editor.layout({ height: 400, width:400 });
            monaco.editor.defineTheme('trilogyStudio', {
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
            monaco.editor.setTheme('trilogyStudio');
            editor.onDidChangeModelContent(() => {
                this.editorData.contents = editor.getValue();
            });

            editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
                if (!this.loading) {
                    this.submit();
                }
            });

            editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyG, () => {

                if (!this.loading && this.$store.getters.hasGenAIConnection) {
                    // this.submit();
                    var selected: monaco.Selection | monaco.Range | null = editor.getSelection();
                    let range: monaco.Range;
                    if (!selected) {
                        var line = editor.getPosition();
                        if (!line) {
                            return
                        }
                        let lineLength = editor.getModel()?.getLineLength(line.lineNumber)
                        range = new monaco.Range(line.lineNumber, 1, line.lineNumber, lineLength ? lineLength + 1 : 1,);

                    }
                    else {
                        range = new monaco.Range(selected.startLineNumber, selected.startColumn, selected.endLineNumber, selected.endColumn)
                    }
                    // run our async call
                    Promise.all([this.submitGenAI(editor.getModel()?.getValueInRange(range))]).then(() => {
                        var op = { range: range, text: this.editorData.generated_sql, forceMoveMarkers: true };
                        editor.executeEdits("gen-ai-prompt-shortcut", [op]);
                        this.saveEditors()
                        this.editorData.runQuery(this.$store);
                    }).catch((error) => {
                        this.setEditorError({ name: this.editorData.name, error: axiosHelpers.getErrorMessage(error) });
                    }
                    )
                }
            });
            let editorData = this.editorData;
            editor.addAction({
                id: 'format-preql',
                label: 'Format Trilogy',
                keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyI],
                run: function () {
                    editorData.formatText(editor.getValue()).then((response) => {
                        editor.setValue(response)
                    })
                }
            });

            editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
                this.saveEditorText({
                    contents: editor.getValue(), name: this.editorData.name,
                    connection: this.editorData.connection
                }).then(() => {
                    this.saveEditors()
                }).catch((error) => {
                    this.setEditorError({ name: this.editorData.name, error: axiosHelpers.getErrorMessage(error) });

                })

            });

            // loader.init().then((monaco) => {
            //     const editorOptions = {
            //         language: "python",
            //         minimap: { enabled: false },
            //     };

            //     monaco.editor.create(document.getElementById("editor"), editorOptions);

            // });

            //   monaco.editor.create(document.getElementById("editor"),   editorOptions);
            //     loader.init().then(monaco => {

            //         var editor = monaco.editor.create(document.getElementById('editor'), {
            //             value: this.editorData.contents,
            //             language: 'sql',
            //             theme: 'myCustomTheme',
            //             automaticLayout: true,
            //             minimap: {
            //                 enabled: false
            //             }
            //         });
            //         editor.onDidChangeModelContent(() => {
            //             this.editorData.contents = editor.getValue();
            //         });
            //     });

        }
    }
})
</script>