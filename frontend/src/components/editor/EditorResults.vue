<template>
    <div v-if="loading" class="results-loading"><v-progress-linear height="10" indeterminate
            color="primary"></v-progress-linear>
    </div>
    <ErrorComponent v-else-if="error" :error="error"></ErrorComponent>
    <HintsComponent v-else-if="!editorData.executed"></HintsComponent>
    <QueryResultsV2 v-else :headers="result.headers" :results="result.data">
    </QueryResultsV2>
    <EditorFooter :executed="editorData.executed" :length="result.data.length" :duration="editorData.duration" />
</template>

<style>
.results-loading {
    height: 100%;
}
</style>
<script>
import { defineComponent } from 'vue';
import { mapGetters } from 'vuex';

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
            last_passed_query_text: null,
            form: null,
            prompt: '',
            generatingPrompt: false,
            info: 'Query processing...',
        }
    },
    components: {
        // ModelConceptList, 
        HintsComponent,
        QueryResultsV2,
        ErrorComponent,
        EditorFooter
    },
    created: function () {
        this.$store.dispatch('getModels');

    },
    mounted() {
    },
    computed: {
        ...mapGetters(['stateModels', 'activeConnection']),
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
            return this.editorData.contents === this.last_passed_query_text
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

    }
})
</script>
  