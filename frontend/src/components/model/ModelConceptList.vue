<template>
    <v-card class="pa-2" style="display: flex;">
      <v-card-text>
        <v-text-field label="Filter" v-model="search" variant="solo" ></v-text-field>
        <v-virtual-scroll :height="height" :items="filteredConcepts" @model-click="propogateModelClick">
          <template v-slot:default="{ item }">
            <ModelConcept :id="item.model+item.namespace+item.concept" density="compact" :concept="item" @model-click="propogateModelClick" />
          </template>
        </v-virtual-scroll>
      </v-card-text>
    </v-card>
  </template>
  
  <script>
  import { defineComponent } from 'vue';
  import { mapGetters } from 'vuex';
  import ModelConcept from '@/components/model/ModelConcept.vue';
  
  export default defineComponent({
    name: 'ModelConceptList',
    props: ['model', 'height'],
    data() {
      return {
        search: ''
      };
    },
    components: { ModelConcept },
    created: function () {
      if (this.models === undefined || this.models.length == 0) {
        return this.$store.dispatch('getModels');
      }
    },
    methods: {
      propogateModelClick(arg) {
        this.$emit('modelClick', arg)
      }
    }
    ,
    computed: {
      ...mapGetters({ models: 'stateModels' }),
      filteredConcepts() {
        if (this.models === undefined || this.models.length == 0) {
          return []
        }
        var lmodel = this.models.filter(x => x.name === this.model);
  
        if (lmodel.length !== 1) {
          return []
        }
        var fmodel = lmodel[0];
        var textSearch = this.search;
  
        return fmodel.concepts.filter(function (concept) {
  
          return (concept.namespace + '.' + concept.name).toLowerCase().indexOf(textSearch.toLowerCase()) !== -1;
        }
        ).sort(function(a, b) {
     return a.key.localeCompare(b.key);
  });
  
      }
  
  
      
    },
  
  });
  </script>
  