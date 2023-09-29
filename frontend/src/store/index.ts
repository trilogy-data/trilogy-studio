import { createStore } from 'vuex'
// import auth from './modules/auth';
import models from './modules/models';
import dev from './modules/dev';
import editors from './modules/editors';
import connections from './modules/connections';
import layout from './modules/layout';
import history from './modules/history';
import nlp from './modules/nlp';

export default createStore({
  // state: {
  // },
  // getters: {
  // },
  // mutations: {
  // },
  // actions: {
  // },
  modules: {
    // auth,
    models,
    dev,
    editors, 
    connections,
    layout,
    history,
    nlp
  }
})
