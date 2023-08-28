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
        console.log(data)
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
    connections: [new Connection('duckdb_demo', 'duck_db'),
    new Connection('bigquery_demo', 'bigquery')],
};

const getters = {
    connections: state => state.connections,
    getConnectionByName: (state) => (name) => {
        return state.connections.find(todo => todo.name === name)
    }
};

const actions = {
    async connectConnection({ commit }, connection) {
        instance.post('/connection', { name: connection.name, 
            dialect:connection.type, 
            model: connection.model }).then((response) => {
            commit('setConnectionActive', connection)
        })

    },
    async setConnectionInactive({ commit }, connection) {
        commit('setConnectionInactive', connection)
    },
    async addConnection({ commit }, data) {
        instance.post('/connection', { name: data.name, dialect: data.type, model: data.model}).then((response) => {
            const connection = new Connection(data.name, data.type, true, data.model)
            commit('addConnection', connection)
        })

    },
    async editConnection({ commit }, data) {
        console.log(data.model)
        instance.put('/connection', { name: data.name, dialect: data.type, model: data.model }).then((response) => {
            const connection = new Connection(data.name, data.type, true, data.model)
            commit('editConnection', connection)
        })
    },
    async removeConnection({ commit }, data) {
        commit('removeConnection', data)
    },
    async loadConnections({commit }, data) {
        commit('setConnections', storageAPI.getConnections())
    }

};


const mutations = {
    async setConnectionActive(state, connection) {
        const index = state.connections.findIndex(c => c.name === connection.name)
        state.connections[index].active = true
    },
    async setConnectionInactive(state, connection) {
        console.log(connection)
        const index = state.connections.findIndex(c => c.name === connection.name)
        if (!index) {
            return
        }
        state.connections[index].active = false
    },
    async editConnection(state, connection) {
        const index = state.connections.findIndex(c => c.name === connection.name)
        console.log(connection)
        state.connections[index] = connection
        storageAPI.setConnections(state.connections)
    },
    async addConnection(state, connection) {
        state.connections.push(connection)
        storageAPI.setConnections(state.connections)
    },
    async removeConnection(state, connection) {
        state.connections = state.connections.filter(c => c.name !== connection.name)
        storageAPI.setConnections(state.connections)
    },
    async setConnections(state, connections) {
        state.connections = connections
    }
};

export default {
    state,
    getters,
    actions,
    mutations
};
