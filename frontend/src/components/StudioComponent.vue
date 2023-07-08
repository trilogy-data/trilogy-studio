<template>
    <splitpanes class="default-theme">
        <pane min-size="10" max-size="30">
            <span>tools</span>
        </pane>
        <pane min-size="30">
            <EditorComponent />
        </pane>
    </splitpanes>
</template>
<script>
import instance from '../api/instance';
import EditorComponent from './query/EditorComponent.vue'
export default {
    name: "StudioView",
    data() {
        return {
            queryText: '',
            form: false,
            loading: false,
            error: '',
            results: [],
            models: [],
            tab: 'models',
        };
    },
    components: { EditorComponent },
    methods: {
        getModels() {
            return instance.get('models', {
            }).then((results) => {
                console.log(results)
                this.models = results.data.models
            })
        },
        runQuery() {

            return instance.post('http://localhost:5678/query', {
                query: this.queryText,
                model: 'stack_overflow'
            }).then((results) => {
                this.results = results.data

            })
        },
    },
    mounted() {
        this.getModels()
    },
};
</script>
