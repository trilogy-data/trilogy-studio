const state = {
    activeSidebar: 'connections',
};

const getters = {
    activeSidebar: state => state.activeSidebar,
};

const actions = {
    async setSidebar({ commit }, data) {
        commit('setSidebar', data);
    },
};


const mutations = {
    setSidebar(state, data) {
        state.activeSidebar = data;
    },
};

export default {
    state,
    getters,
    actions,
    mutations
};
