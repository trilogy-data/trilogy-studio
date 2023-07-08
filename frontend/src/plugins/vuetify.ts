// Styles
// import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { Splitpanes, Pane } from 'splitpanes';
import * as components from 'vuetify/components';
import * as labs from 'vuetify/labs/components'
// Vuetify
import { createVuetify } from 'vuetify'
import 'splitpanes/dist/splitpanes.css'

export default createVuetify({
  components: { ...components, ...labs, Splitpanes, Pane }
}
  // https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
)
