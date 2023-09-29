
import { ConnectionHistory, HistoryEvent } from '/src/models/history';


import Store from 'electron-store'
import instance from '/src/api/instance'


const storageName = 'history';

const store = new Store<Record<string, Object>>({
    name: storageName,
    watch: true,
});

const state = {
    history: [],
};

const getters = {
    history: state => state.history,
    getHistoryByName: (state) => (name) => {
        return state.history.find(conn => conn.name === name)
    },
};


const actions = {
    async addHistory({ commit, rootGetters }, data) {
        commit('addHistory', data)
    },

};


const mutations = {
    async addHistory(state, data) {
        let index = state.connections.findIndex(c => c.name === data.name)
        if (!index) {
            index = new ConnectionHistory(data.name, [])
        }
        // text: string;
        // editor: string;
        // timestamp: Date;
        // duration: number | null;
        // executed: boolean;
        // error: string | null;
        const event = new HistoryEvent(
            data.text,
            data.editor,
            data.timestamp,
            data.duration,
            data.executed,
            data.error
        )
        index.events.push(event)
    }
};

export default {
    state,
    getters,
    actions,
    mutations
};