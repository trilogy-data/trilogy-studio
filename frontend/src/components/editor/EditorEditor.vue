<template>
        <div ref="editor" id="editor" class="editor-fix-styles">
            <!-- <div id="editor" > </div> -->
        </div>
</template>

<style scoped>
.results {
    display: flex;
    flex-direction: column;
    flex-grow: 0;
    flex-shrink: 1;
    /* flex-wrap: wrap; */
    height: 100%;
}

.editor {
    background-color: var(--main-bg-color);
    filter: brightness(85%);
}

.editor-fix-styles {
    text-align: left;
    border: none;
}

.split {
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    flex: 1 1 100%;
    height: 100%;
}
</style>
<script>
import { defineComponent } from 'vue';
import { mapGetters, mapActions } from 'vuex';

// import ModelConceptList from '@/components/model/ModelConceptList.vue';
import QueryResultsV2 from './QueryResult.vue';
import HintsComponent from './HintsComponent.vue';
import ErrorComponent from './ErrorComponent.vue';
import axiosHelpers from '/src/api/helpers';
import colorHelpers from '/src/helpers/color';
import instance from '/src/api/instance';
import * as monaco from 'monaco-editor';
import Split from 'split.js'
import EditorFooter from './EditorFooter.vue';
import { Editor } from '/src/models/Editor'

export default defineComponent({
    name: 'EditorComponent',
    props: {
        editorData: {
            type: Object,
            default: () => new Editor()
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
            editorY: 400
        }
    },
    components: {
        // ModelConceptList, 
        HintsComponent,
        QueryResultsV2,
        ErrorComponent,
        EditorFooter
    },
    mounted() {
        this.createEditor()
    },
    computed: {
        ...mapGetters(['getConnectionByName']),
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
        splitElements() {
            return [
                this.$refs.editor,
                this.$refs.results
            ];
        },
        passedQuery() {
            return this.editorData.contents === this.last_passed_query_text
        },
        defaultRows() {
            if (this.$vuetify.display.mobile) {
                return 10;
            }
            return 20;
        },
        generateOverlayVisible() {
            return this.prompt.length > 1 || this.generatingPrompt
        }

    },
    methods: {
        ...mapActions(['saveEditors', 'saveEditorText', 'connectConnection']),
        async runQuery(rquery) {
            let local = this;

            await instance.post('query', rquery).then(function (response) {

                local.result = response.data;
            })
        },
        async generate() {
            this.loading = true;
            this.info = 'Generating query from prompt...'
            this.error = null;
            var self = this;
            await instance.post('parse_question', {
                model: this.query.model,
                text: this.prompt
            }).then(function (resp) {
                self.query.query = '# generated from prompt: ' + self.prompt + '\n' + resp.data.query_text;
                self.prompt = '';
                self.submit();
            }).catch((error) => {
                self.error = axiosHelpers.getErrorMessage(error);
                self.loading = false;
                self.generatingPrompt = false;
            })
        },
        async submit() {
            // this.loading = true;
            this.info = 'Executing query...'
            // this.error = null;
            let current_query = this.editorData.contents;
            let local = this;
            if (!this.connection.active) {
                await this.connectConnection(this.connection)
            }
            await this.editorData.runQuery();
            this.last_passed_query_text = current_query;
        },
        async format() {
            this.loading = true;
            this.info = 'Formatting query...'
            this.error = null;
            var self = this;
            await instance.post('format_query', { model: this.query.model, query: this.editorData.contents, id: this.query.id }).then(function (resp) {
                self.query.query = resp.data.new_text;
                self.loading = false;
            }).catch((error) => {
                self.error = axiosHelpers.getErrorMessage(error);
                self.loading = false;
            })
        },
        appendModelToQuery(obj) {
            this.editorData.contents = this.editorData.contents + "\n\t" + (obj || '') + ",";
        },
        querySaveComplete() {
            this.$emit('querySaveComplete')
        },
        clearPrompt() {
            this.prompt = '';
        },
        createEditor() {
            const editor = monaco.editor.create(document.getElementById('editor'), {
                value: this.editorData.contents,
                language: 'sql',
                automaticLayout: true,
            })
            this.editor = editor;
            // editor.layout({ height: 400, width:400 });
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
            editor.onDidChangeModelContent(() => {
                this.editorData.contents = editor.getValue();
            });

            editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
                if (!this.loading) {
                    this.submit();
                }
            });

            editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
                this.saveEditorText({contents: editor.getValue(), name: this.editorData.name})
                this.saveEditors()
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
  