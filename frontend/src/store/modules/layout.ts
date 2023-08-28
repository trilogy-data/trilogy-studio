const state = {
    activeSidebar: 'connections',
};

const getters = {
    activeSidebar: state => state.activeSidebar,
    sidebarHeight: state => {
        const height = document.documentElement.clientHeight;
        return height - 20;
    }
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
