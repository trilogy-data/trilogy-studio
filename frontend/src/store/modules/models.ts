import instance from '/src/api/instance'

const state = {
  models: []
};

const getters = {
  stateModels: state => state.models,
};

const actions = {
  async getModels({commit}) {
    const {data} = await instance.get('models');
    commit('setModels', data.models);
  },
};


const mutations = {
  setModels(state, models) {
    state.models=models;
  },
};

export default {
  state,
  getters,
  actions,
  mutations
};
