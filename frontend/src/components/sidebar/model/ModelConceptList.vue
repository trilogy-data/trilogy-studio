<template>
  <v-card theme="dark" class="px-0" style="display: flex;">
    <v-card-text class="px-0">
      <v-text-field class="py-0" label="Filter" v-model="search" variant="solo"></v-text-field>
      <v-virtual-scroll :height="height" :items="filteredConcepts" @model-click="propogateModelClick">
        <template v-slot:default="{ item }">
          <ModelConcept :id="item.model + item.namespace + item.concept" density="compact" :concept="item"
            @model-click="propogateModelClick" />
        </template>
      </v-virtual-scroll>
    </v-card-text>
  </v-card>
</template>
  
<script>
import { defineComponent } from 'vue';
import { mapGetters } from 'vuex';
import ModelConcept from './ModelConcept.vue';
import { mapActions } from 'vuex';

export default defineComponent({
  name: 'ModelConceptList',
  props: ['model', 'height', 'editor'],
  data() {
    return {
      search: ''
    };
  },
  components: { ModelConcept },
  // created: function () {
  //   if (this.models === undefined || this.models.length == 0) {
  //     return this.$store.dispatch('getModels');
  //   }
  // },
  methods: {
    ...mapActions(['insertTextInEditor'
    ]),
    propogateModelClick(arg) {

      this.insertTextInEditor({ name: this.editor, text: arg })
    }

  }
  ,
  computed: {
    ...mapGetters(['models', 'sidebarHeight']),
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
      ).sort(function (a, b) {
        return a.key.localeCompare(b.key);
      });

    }



  },

});
</script>
  