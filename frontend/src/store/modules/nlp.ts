
import { ChatType, ChatConnection } from '/src/models/ChatConnection';


import Store from 'electron-store'
import instance from '/src/api/instance'


const storageName = 'nlp';

const store = new Store<Record<string, Object>>({
  name: storageName,
  watch: true,
});

const state = {
    chatConnections: [],
};

const getters = {
    chatConnections: state => state.chatConnections,
    getChatConnectionByName: (state) => (name) => {
        return state.chatConnections.find(conn => conn.name === name)
    },
};


const actions = {
    async addChatConnection({ commit, rootGetters }, data) {
        const apiArgs = getConnectionArgument(rootGetters, data)
        instance.post('/connection', apiArgs).then(() => {
            commit('setConnectionActive', data)
        })
    },

};


const mutations = {
    async addChatConnection(state, connection) {
        const index = state.connections.findIndex(c => c.name === connection.name)
        state.chatConnections[index].active = true
    }
};

export default {
    state,
    getters,
    actions,
    mutations
};