<template>
    <div
      id="interface"
      class="interface"
      v-hotkey="keymap"
    >
      <div
        class="interface-wrap row"
      >
        <div
          ref="sidebar"
          :class="{hide: !sidebarShown, sidebar: true}"
          
        >
          <SidebarComponent/>
        </div>
        <div
          ref="content"
          class="page-content flex-col"
          id="page-content"
        >
          <EditorComponent/>
        </div>
      </div>
    </div>
  </template>
<style>
.page-content {
  width: 100%;
  overflow: hidden;
}
.interface {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}
.interface-wrap {
display: flex;
flex-wrap: nowrap;
flex: 1 1 100%;
}
.sidebar {
width:  400px;
min-width:  200px;
max-width: 90%;
}
.page-content {
flex: 1 1 auto;
min-width: 350px;
z-index: 1;
}

</style>
<script>
import instance from '../api/instance';
import EditorComponent from './editor/EditorComponent.vue'
import SidebarComponent from './connections/SidebarComponent.vue'
import Split from 'split.js'
export default {
    name: "StudioView",
    data() {
        return {
            split: null,
            queryText: "",
            form: false,
            loading: false,
            error: "",
            results: [],
            models: [],
            tab: "models",
        };
    },
    components: { EditorComponent, SidebarComponent },
    computed: {
        splitElements() {
            return [
                this.$refs.sidebar,
                this.$refs.content
            ];
        }
    },
    methods: {
        getModels() {
            return instance.get("models", {}).then((results) => {
                console.log(results);
                this.models = results.data.models;
            });
        },
        runQuery() {
            return instance.post("http://localhost:5678/query", {
                query: this.queryText,
                model: "stack_overflow"
            }).then((results) => {
                this.results = results.data;
            });
        },
    },
    beforeDestroy() {
        if (this.split) {
            this.split.destroy();
        }
    },
    mounted() {
        this.getModels();
        this.split = Split(this.splitElements, {
            elementStyle: (_dimension, size) => ({
                "flex-basis": `calc(${size}%)`,
            }),
            sizes: [25, 75],
            minSize: 200,
            expandToMin: true,
            gutterSize: 5,
        });
    },
    components: { EditorComponent }
};
</script>
