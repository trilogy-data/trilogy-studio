
import { ConnectionHistory, HistoryEvent } from '/src/models/History';


import Store from 'electron-store'

const storageName = 'history';

const store = new Store<Record<string, Object>>({
    name: storageName,
    watch: true,
});

const storageAPI = {
    setHistory(value: Array<ConnectionHistory>) {
        // const buffer = safeStorage.encryptString(value);
        store.set(storageName, value);
        // store.set(key, buffer.toString(encoding));
    },


    getHistory(): Array<ConnectionHistory> {
        const data = store.get(storageName, []) as Array<any>
        const parsed = data.map(dict => {
            return ConnectionHistory.fromJSON(dict)
        });
        return parsed
    },
};

const state = {
    history: storageAPI.getHistory(),
};

const getters = {
    history: state => state.history,
    getHistoryByName: (state) => (name) => {
        return state.history.find(conn => conn.name === name)
    },
};


const actions = {
    async addHistory({ commit, }, data) {
        commit('addHistory', data)
    },

};


const mutations = {
    async addHistory(state, data) {
        let index = state.history.find(c => c.name === data.connection)
        if (!index) {
            index = new ConnectionHistory(data.connection, [])
            state.history.push(index)
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
        storageAPI.setHistory(state.history)
    }
};

export default {
    state,
    getters,
    actions,
    mutations
};