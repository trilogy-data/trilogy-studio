<template>
    <div class="split editor">
        <div ref="editor" id="editor" class="revert">
            <!-- <div id="editor" > </div> -->
        </div>
        <div ref="results">
            <v-progress-linear v-if="loading" height="10" indeterminate color="primary"></v-progress-linear>
            <ErrorComponent v-else-if="error"></ErrorComponent>
            <HintsComponent v-else-if="!result"></HintsComponent>
            <QueryResultsV2 v-else :headers="result.headers" :results="result.results" :columns="result.columns">
            </QueryResultsV2>
        </div>
    </div>
</template>

<style>
.editor {
    background-color: var(--main-bg-color);
    filter: brightness(85%);
}

.revert {
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

.page-content {
    flex: 1 1 auto;
    min-width: 350px;
    z-index: 1;
}
</style>
<script>
import { defineComponent } from 'vue';
import { mapGetters } from 'vuex';

// import ModelConceptList from '@/components/model/ModelConceptList.vue';
import QueryResultsV2 from './QueryResult.vue';
import HintsComponent from './HintsComponent.vue'
import ErrorComponent from './ErrorComponent.vue'
import axiosHelpers from '/src/api/helpers';
import colorHelpers from '/src/helpers/color';
import instance from '/src/api/instance';
import * as monaco from 'monaco-editor';
import Split from 'split.js'

export default defineComponent({
    name: 'EditorComponent',
    data() {
        return {
            query: {
                query: 'SELECT 1 -> echo;',
                model: 'bigquery.thelook_ecommerce',
            },
            result: null,
            error: null,
            loading: false,
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
        ErrorComponent
    },
    created: function () {
        this.$store.dispatch('getModels');

    },
    mounted() {
        this.split = Split(this.splitElements, {
            // elementStyle: (_dimension, size) => ({
            //     "flex-basis": `calc(${size}%)`,
            // }),
            direction: 'vertical',
            // sizes: [75, 25],
            // minSize: 100,
            // expandToMin: true,
            // gutterSize: 25,
        });
        this.createEditor()
    },
    computed: {
        ...mapGetters(['stateModels', 'activeConnection']),
        splitElements() {
            return [
                this.$refs.editor,
                this.$refs.results
            ];
        },
        computedHeight() {
            return `${this.editorY}px`
        },
        computedWidth() {
            return `${this.editorX}px`
        },
        modelNames() {
            return [...this.models.map(item => item.name)]
        },
        passedQuery() {
            return this.query.query === this.last_passed_query_text
        },
        modelColor() {
            return colorHelpers.stringToColor(this.query.model)
        },
        mobile() {
            return this.$vuetify.display.mobile
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
            this.loading = true;
            this.info = 'Executing query...'
            this.error = null;
            let current_query = this.query.query;
            let local = this;
            try {
                let info = { connection: this.activeConnection, query: this.query.query, id: this.query.id };
                await this.runQuery(info);
                this.last_passed_query_text = current_query;
                this.loading = false;
            } catch (error) {
                local.error = axiosHelpers.getErrorMessage(error);
                local.loading = false;
            }
        },
        async format() {
            this.loading = true;
            this.info = 'Formatting query...'
            this.error = null;
            var self = this;
            await instance.post('format_query', { model: this.query.model, query: this.query.query, id: this.query.id }).then(function (resp) {
                self.query.query = resp.data.new_text;
                self.loading = false;
            }).catch((error) => {
                self.error = axiosHelpers.getErrorMessage(error);
                self.loading = false;
            })
        },
        appendModelToQuery(obj) {
            this.query.query = this.query.query + "\n\t" + (obj || '') + ",";
        },
        querySaveComplete() {
            this.$emit('querySaveComplete')
        },
        clearPrompt() {
            this.prompt = '';
        },
        createEditor() {
            const editor = monaco.editor.create(document.getElementById('editor'), {
                value: this.query.query,
                language: 'sql',
                automaticLayout: true,
            })
            this.editor = editor;
            // editor.layout({ height: 400, width:400 });
            monaco.editor.defineTheme('myCustomTheme', {
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
            monaco.editor.setTheme('myCustomTheme');
            editor.onDidChangeModelContent(() => {
                this.query.query = editor.getValue();
            });

            editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
                if (!this.loading) {
                    this.submit();
                }
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
            //             value: this.query.query,
            //             language: 'sql',
            //             theme: 'myCustomTheme',
            //             automaticLayout: true,
            //             minimap: {
            //                 enabled: false
            //             }
            //         });
            //         editor.onDidChangeModelContent(() => {
            //             this.query.query = editor.getValue();
            //         });
            //     });

        }
    }
})
</script>
  