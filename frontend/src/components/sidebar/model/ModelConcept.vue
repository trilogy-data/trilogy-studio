
<script>
import { defineComponent } from 'vue';
import colorHelpers from '/src/helpers/color';

export default defineComponent({
  name: 'ModelConcept',
  props: ['concept', 'density'],
  data() {
    return { force_import: colorHelpers.stringToColor('ED') }
  },
  methods: {
    propogateModelClick() {
      this.$emit('modelClick', this.key)
    },
    convertToColor(input) {
      return colorHelpers.stringToColor(input)
    }
  },
  computed: {
    icon() {
      switch (this.concept.purpose) {
        case "key":
          return "mdi-axis-x-arrow"
        case "property":
          return "mdi-axis-x-arrow"
        default:
          return "mdi-finance"
      }

    },
    iconText() {
      switch (this.concept.purpose) {
        case "key":
          return "Key"
        case "property":
          return "Property"
        case "metric":
          return "Metric"
        case "constant":
          return "Constant"
        default:
          return this.concept.purpose
      }

    },
    key() {
      return this.concept.namespace + '.' + this.concept.name
    }

  },

});
</script>
<style scoped>
.concept-icon {
  font-size:12px
}
</style>


<template>
  <v-list-item v-if="density === 'compact'" class="ma-0 pa-0" :density="density" :key="key" :title="key"
    @click="propogateModelClick">
    <template v-slot:prepend>
      <v-icon class="mr-0 concept-icon"> <v-tooltip > {{ concept.purpose }}</v-tooltip> {{ icon }} </v-icon>
    </template></v-list-item>
  <v-list-item v-else :density="density" :key="key + '2'" @click="propogateModelClick">
    <template v-slot:prepend>
      <!-- <v-icon> 
       {{ icon }}
      </v-icon> -->
      <div  class="ma-0 pr-2"><v-tooltip activator="parent"  location="left"> {{ iconText }}</v-tooltip>
      <v-icon> 
       {{ icon }}
      </v-icon>
    </div>
    </template>
    <v-list-item-title>{{ concept.key }} ({{ concept.datatype }})</v-list-item-title>
    <v-list-item-subtitle>
      {{ concept.description }}
    </v-list-item-subtitle>
    <v-card :density="density" v-if="concept.lineage.length" outlined color="transparent">
      <template v-for="component in concept.lineage" :key="component.token"><v-chip label size="x-small" class="pa-2 ma-1"
          :color="convertToColor((component.depth * 133).toString())">
          {{ component.token }}
        </v-chip></template></v-card>
  </v-list-item>
</template>
