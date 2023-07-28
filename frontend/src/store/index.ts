import { createStore } from 'vuex'
// import auth from './modules/auth';
import models from './modules/models';
import dev from './modules/dev';

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
    dev
  }
})
