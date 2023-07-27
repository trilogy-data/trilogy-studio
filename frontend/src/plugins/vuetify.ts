// Styles
// import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import * as components from 'vuetify/components';
import * as labs from 'vuetify/labs/components'
import  "tabulator-tables/dist/css/tabulator.min.css";
import "tabulator-tables/dist/css/tabulator_midnight.css"

// Vuetify
import { createVuetify } from 'vuetify'


export default createVuetify({
  components: { ...components, ...labs, }
}
  // https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
)
