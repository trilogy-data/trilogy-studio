import { createApp } from 'vue'
import './style.css'
import App from '/src/App.vue'
import vuetify from './plugins/vuetify'
// import { loadFonts } from './plugins/webfontloader'
import apexCharts from './plugins/apexcharts'
import router from './router'
import store from './store'

// loadFonts()

createApp(App).use(store).use(router)
.use(vuetify)
.use(apexCharts).mount('#app').$nextTick(() => postMessage({ payload: 'removeLoading' }, '*'))
