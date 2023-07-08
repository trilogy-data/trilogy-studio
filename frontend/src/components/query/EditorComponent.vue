<template>
    <splitpanes class="default-theme" horizontal @resize="logThis('resize', $event)" @resized="resize('resized', $event)"
            @ready="startEditor()">
        <pane min-size="30" size="70" >
            <div :height="editorY + 'px'" class="full-view">
            <div  id="editor" class="fill-parent"></div>
            </div>
        </pane>
        <pane min-size="20" size="25">
            <div v-if="!result">Run query to see results A  {{ editorY }}</div>
            <QueryResultsV2 v-else :headers="result.headers" :results="result.results" :columns="result.columns">
            </QueryResultsV2>
        </pane>
    </splitpanes>
</template>

<style>
.full-view {
    display: flex;
}

.fill-parent {
    flex: 1;
}
</style>
<script>
import { defineComponent } from 'vue';
import { mapGetters } from 'vuex';
// import ModelConceptList from '@/components/model/ModelConceptList.vue';
import QueryResultsV2 from '/src/components/query/QueryResult.vue';
import axiosHelpers from '/src/api/helpers';
import colorHelpers from '/src/helpers/color';
import instance from '/src/api/instance';
import * as monaco from 'monaco-editor';


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

        QueryResultsV2,
    },
    created: function () {
        this.$store.dispatch('getModels');

    },
    computed: {
        ...mapGetters({
            models: 'stateModels',
        }),
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
        // handleKeyDown(event) {
        //     if (event.ctrlKey && event.key === 'Enter') {
        //         // Trigger your action here

        //     }
        // },
        async logThis(type, pane) {
            console.log(type, pane)
        },
        async resize(type, pane) {
            let editorPane = pane[0];
            if (this.editor) {
                console.log(editorPane)
                console.log('resizing')
                // this.editorY = editorPane.clientHeight;
                console.log(this.editorY)
                this.editor.layout({  height: this.editorY, width:400 });
            }
      
            console.log(type, pane);
        },
        async runQuery(rquery) {
            let local = this;
            console.log('testing')
            await instance.post('query', rquery).then(function (response) {
                local.result = response.data;
            })
        },
        async generate() {
            this.loading = true;
            this.info = 'Generating query from prompt...'
            this.error = null;
            var self = this;
            await instance.post('parse_question', { model: this.query.model, text: this.prompt }).then(function (resp) {
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
                let info = { model: this.query.model, query: this.query.query, id: this.query.id };
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
        startEditor() {
            const editor = monaco.editor.create(document.getElementById('editor'), {
            value: this.query.query,
            language: 'sql',
            // automaticLayout: true,

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
  