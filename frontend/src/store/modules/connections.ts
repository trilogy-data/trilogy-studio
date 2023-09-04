// Temporary store for stitching together dev functionality
// not intended for long-term use

// import instance from '/src/api/instance'

import { Connection } from '/src/models/Connection'
import { Model, LocalModel } from '/src/models/Model'
import Store from 'electron-store'
import instance from '/src/api/instance'
import NewConnectionPopupVue from '/src/components/sidebar/connections/NewConnectionPopup.vue';

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

// function findMatchingValue(arr, condition) {
//     const foundElement = arr.find(element => condition(element));
//     return foundElement !== undefined ? foundElement : null;
// }


const state = {
    connections: [new Connection('duckdb_demo', 'duck_db', false, 'duckdb_demo'),
    new Connection('bigquery_demo', 'bigquery', false, 'bigquery_demo')],
};

const getters = {
    connections: state => state.connections,
    getConnectionByName: (state) => (name) => {
        return state.connections.find(todo => todo.name === name)
    }
};

function getConnectionArgument(rootGetters, data) {
    let modelArgs = {
        model: data.model,
        full_model: null
    } as { model: any; full_model: any; }
    let model = rootGetters.getModelByName(data.model)
    if (model instanceof LocalModel) {
        modelArgs = {
            model: data.model,
            full_model: { name: data.model, sources: [] }
        }
    }
    return {
        type: data.type,
        name: data.name, dialect: data.type, extra: data.extra, ...modelArgs
        //let session = context.rootState.instance.session;
    }
}

const actions = {
    async connectConnection({ commit }, connection) {
        instance.post('/connection', {
            name: connection.name,
            dialect: connection.type,
            model: connection.model,
            extra: connection.extra
        }).then(() => {
            commit('setConnectionActive', connection)
        })

    },
    async setConnectionInactive({ commit }, connection) {
        commit('setConnectionInactive', connection)
    },
    async addConnection({ commit, rootGetters }, data) {
        const apiArgs = getConnectionArgument(rootGetters, data)
        return instance.post('/connection', apiArgs).then(() => {
            const connection = new Connection(apiArgs.name, apiArgs.type,
                true, apiArgs.model, apiArgs.extra)
            commit('addConnection', connection)
        })

    },
    async editConnection({ commit, rootGetters }, data) {
        const apiArgs = getConnectionArgument(rootGetters, data)
        return instance.put('/connection', apiArgs).then(() => {
            const connection = new Connection(apiArgs.name, apiArgs.type,
                true, apiArgs.model, apiArgs.extra)
            console.log(connection)
            commit('editConnection', connection)
        })
    },
    async removeConnection({ commit }, data) {
        commit('removeConnection', data)
    },
    async loadConnections({ commit }, _) {
        commit('setConnections', storageAPI.getConnections())
    }

};


const mutations = {
    async setConnectionActive(state, connection) {
        const index = state.connections.findIndex(c => c.name === connection.name)
        state.connections[index].active = true
    },
    async setConnectionInactive(state, connection) {
        const index = state.connections.findIndex(c => c.name === connection.name)
        if (!index) {
            return
        }
        state.connections[index].active = false
    },
    async editConnection(state, connection) {
        const index = state.connections.findIndex(c => c.name === connection.name)
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
