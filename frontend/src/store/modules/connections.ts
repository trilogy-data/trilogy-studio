// Temporary store for stitching together dev functionality
// not intended for long-term use

// import instance from '/src/api/instance'

import { Connection } from '/src/models/Connection'

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
    async addConnection({ commit }, data) {
    },
    async removeConnection({ commit }, data) {
    },

};


const mutations = {
};

export default {
    state,
    getters,
    actions,
    mutations
};
