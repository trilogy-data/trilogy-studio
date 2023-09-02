
import { Model } from '/src/models/Model'
import Store from 'electron-store'
import instance from '/src/api/instance'


const storageName = 'models';

const store = new Store<Record<string, Object>>({
  name: storageName,
  watch: true,
});


const storageAPI = {
  setConnections(value: Array<Model>) {
    // const buffer = safeStorage.encryptString(value);
    store.set(storageName, value);
    // store.set(key, buffer.toString(encoding));
  },


  getModels(): Array<Model> {
    const data = store.get(storageName, []) as Array<any>
    const parsed = data.map(dict => {
      return Model.fromJSON(dict)
    });
    return parsed
  },
};

const state = {
  localModels: storageAPI.getModels(),
  communityModels: [],
};

const getters = {
  models: state => state.localModels.concat(state.communityModels),
  getModelByName: (_, getters) => (name) => {
    return getters.models.find(todo => todo.name === name)
  }
};

const actions = {
  async getCommunityModels({ commit }) {
    const { data } = await instance.get('models');
    const parsed = data.models.map(dict => {
      return Model.fromJSON(dict)
    });
    console.log(parsed)
    commit('setCommunityModels', parsed);
  },
};


const mutations = {
  setModels(state, models) {
    state.models = models;
  },
  setCommunityModels(state, models) {
    state.communityModels = models;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
