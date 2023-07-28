// Temporary store for stitching together dev functionality
// not intended for long-term use

// import instance from '/src/api/instance'

const state = {
  activeConnection: 'duckdb_demo',
};

const getters = {
  activeConnection: state => state.activeConnection,
};

const actions = {
  async setActiveConnection({commit}, data) {
    commit('setActiveConnection', data);
  },
};


const mutations = {
  setActiveConnection(state, data) {
    state.activeConnection = data;
  },
};

export default {
  state,
  getters,
  actions,
  mutations
};
