// Temporary store for stitching together dev functionality
// not intended for long-term use

// import instance from '/src/api/instance'

import { Editor } from '/src/models/Editor'

import { Connection } from '/src/models/Connection'

function findMatchingValue(arr, condition) {
    const foundElement = arr.find(element => condition(element));
    return foundElement !== undefined ? foundElement : null;
}




const state = {
    editors: [new Editor('editor1', 'duckdb', 'duckdb_demo'),
    new Editor('editor2', 'duckdb', 'duckdb_demo')],
    activeEditor: 'editor1'
};

const getters = {
    editors: state => state.editors,
    activeEditor: state => findMatchingValue(state.editors, (editor) => editor.name === state.activeEditor),
};

const actions = {
    async setActiveEditor({ commit }, data) {
        if (data){
            commit('setActiveEditor', data);
        }
        
    },
    async addEditor({ commit }, data) {
    },
    async removeEditor({ commit }, data) {
    },
    async setActiveConnection({ commit }, data) {
        commit('setActiveConnection', data);
    },
};


const mutations = {
    setActiveEditor(state, data) {
        state.activeEditor = data;
    },
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
