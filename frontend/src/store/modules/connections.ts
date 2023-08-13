// Temporary store for stitching together dev functionality
// not intended for long-term use

// import instance from '/src/api/instance'

import { Connection } from '/src/models/Connection'
import Store from 'electron-store'
import instance from '/src/api/instance'

const store = new Store<Record<string, Object>>({
    name: 'connections',
    watch: true,
});


const storageAPI = {
    setConnections(value: Array<Connection>) {
        // const buffer = safeStorage.encryptString(value);
        store.set('connections', value);
        // store.set(key, buffer.toString(encoding));
    },


    getConnections(): Array<Connection> {
        const data = store.get('connections', []) as Array<any>
        const parsed = data.map(dict => {
            return Connection.fromJSON(dict)
        });
        return parsed
    },
};

function findMatchingValue(arr, condition) {
    const foundElement = arr.find(element => condition(element));
    return foundElement !== undefined ? foundElement : null;
}


const state = {
    connections: [new Connection('duckdb_demo', 'duckdb'),
    new Connection('bigquery_demo', 'bigquery')],
};

const getters = {
    connections: state => state.connections,
    getConnectionByName: (state) => (name) => {
        return state.connections.find(todo => todo.name === name)
    }
};

const actions = {
    async connectConnection({ commit }, data) {
        instance.post('/connection', { name: data.connection.name, dialect:data.connection.type, model: data.connection.model }).then((response) => {
            commit('setConnectionActive', data.connection)
        })

    },
    async addConnection({ commit }, data) {
        instance.post('/connection', { name: data.name, dialect: data.type, model: data.model }).then((response) => {
            const connection = new Connection(data.name, data.type, true, data.model)
            commit('addConnection', connection)
        })

    },
    async removeConnection({ commit }, data) {
        commit('removeConnection', data.connection)
    },

};


const mutations = {
    async setConnectionActive(state, connection) {
        const index = state.connections.findIndex(c => c.name === connection.name)
        state.connections[index].active = true
    },
    async addConnection(state, connection) {
        state.connections.push(connection)
        storageAPI.setConnections(state.connections)
    },
    async removeConnection(state, connection) {
        state.connections = state.connections.filter(c => c.name !== connection.name)
        storageAPI.setConnections(state.connections)
    }
};

export default {
    state,
    getters,
    actions,
    mutations
};
