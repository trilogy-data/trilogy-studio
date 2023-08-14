// Temporary store for stitching together dev functionality
// not intended for long-term use

// import instance from '/src/api/instance'

import { Editor, RawEditor } from '/src/models/Editor'
import Store from 'electron-store'

function findMatchingValue(arr, condition) {
    const foundElement = arr.find(element => condition(element));
    return foundElement !== undefined ? foundElement : null;
}

const store = new Store<Record<string, Object>>({
    name: 'editors',
    watch: true,
});

const storageAPI = {
    setEditors(value: Array<Editor | RawEditor>) {
        // const buffer = safeStorage.encryptString(value);
        store.set('editors', value);
        // store.set(key, buffer.toString(encoding));
    },


    getEditors(): Array<Editor | RawEditor> {
        const data = store.get('editors', []) as Array<any>
        const parsed = data.map(dict => {
            if (dict.syntax === 'preql') {return Editor.fromJSON(dict)}
            else if (dict.syntax === 'sql') {
               return  RawEditor.fromJSON(dict)
            } 
        });
        return parsed
    },
};


function getInitialEditors() {
    let editors = storageAPI.getEditors();
    editors = editors.filter(editor => (typeof editor.name === 'string' && editor.connection))
    if (editors.length === 0) { 
        editors = [new Editor('demo-editor', 'duckdb', 'duckdb_demo')]
    }
    return editors
}
const initialEditors: Array<Editor | RawEditor> = getInitialEditors();


const state = {
    editors: initialEditors,
    activeEditor: initialEditors[0].name
};

const getters = {
    editors: state => state.editors,
    activeEditor: state => findMatchingValue(state.editors, (editor) => editor.name === state.activeEditor),
};

const actions = {
    async saveEditorText({commit}, data) {
        commit('saveEditorText', data)
    },
    async setActiveEditor({ commit }, data) {
        if (data) {
            commit('setActiveEditor', data);
        }

    },
    async newEditor({ commit }, data) {
        commit('newEditor', data);
        commit('saveEditors', data)
    },
    async removeEditor({ commit }, data) {
        commit('removeEditor', data)
        commit('saveEditors', data)
    },
    // unique from remove in case we want to prompt for save here 
    async closeEditor({ commit }, data) {
        commit('removeEditor', data)
        commit('saveEditors', data)
    },
    async setActiveConnection({ commit }, data) {
        commit('setActiveConnection', data);
    },
    async saveEditors({ commit }, data) {
        commit('saveEditors', data)
    }
};


const mutations = {
    setActiveEditor(state, data) {
        state.activeEditor = data;
    },
    setActiveConnection(state, data) {
        state.activeConnection = data;
    },
    removeEditor(state, data) {
        const newEditors = state.editors.filter(editor => editor.name !== data.name)
        if (data.name === state.activeEditor) {
            state.activeEditor = newEditors[0].name
        }
        state.editors = newEditors
    },
    saveEditors(state, data) {
        storageAPI.setEditors(state.editors)
    },
    saveEditorText(state, data) {
        const editor = findMatchingValue(state.editors, (editor) => editor.name === data.name)
        editor.contents = data.contents
    },
    loadEditors(state, data) {
        state.editors = storageAPI.getEditors()
    },
    newEditor(state, data) {
        let newEd = null;
        console.log(data)
        if (data.syntax === 'preql') {
            newEd = new Editor(data.name, data.connection.type, data.connection.name,);
        }
        else {
            newEd = new RawEditor(data.name, data.connection.type, data.connection.name,);
        }
        state.editors.push(newEd)
    }
};

export default {
    state,
    getters,
    actions,
    mutations
};
