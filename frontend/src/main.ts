import { createApp } from 'vue'
import './style.css'
import './theme.css'
import App from '/src/App.vue'
import vuetify from './plugins/vuetify';
import Tabulator from './plugins/tabulator';
// import { loadFonts } from './plugins/webfontloader'
import apexCharts from './plugins/apexcharts'
import router from './router'
import store from './store'
// loadFonts()

createApp(App).use(store).use(router)
    .use(vuetify)
    .use(require('vue3-shortkey'))
    .use(apexCharts).mount('#app').$nextTick(() => postMessage({ payload: 'removeLoading' }, '*'))
