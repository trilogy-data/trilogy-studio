import { GenAIConnection } from "/src/models/GenAIConnection.ts";

import Store from "electron-store";
import instance from "/src/api/instance";

const storageName = "nlp";

const storageAPI = {
  setGenAIConnections(value: Array<GenAIConnection>) {
    // const buffer = safeStorage.encryptString(value);
    store.set(storageName, value);
    // store.set(key, buffer.toString(encoding));
  },

  getGenAIConnections(): Array<GenAIConnection> {
    const data = store.get(storageName, []) as Array<any>;
    const parsed = data.map((dict) => {
      return GenAIConnection.fromJSON(dict);
    });
    console.log(parsed);
    return parsed;
  },
};

const store = new Store<Record<string, Object>>({
  name: storageName,
  watch: true,
});

const state = {
  genAIConnections: storageAPI.getGenAIConnections(),
};

const getters = {
  hasGenAIConnection: (state) => state.genAIConnections.length>0,
  genAIConnections: (state) => state.genAIConnections,
  getGenAIConnectionByName: (state) => (name) => {
    return state.genAIConnections.find((conn) => conn.name === name);
  },
};

const actions = {
  async addGenAIConnection({ commit, rootGetters }, data) {
    console.log(data);
    instance.post("/gen_ai_connection", data).then(() => {
      const connection = GenAIConnection.fromJSON({
        type: data.type,
        name: data.name,
        extra: data.extra,
        apiKey: data.extra,
        active: true,
      });
      commit("addGenAIConnection", connection);
    });
  },
  async setGenAIConnectionState({ commit, rootGetters }, args) {
    commit("setGenAIConnectionState", args);
  },
};

const mutations = {
  async addGenAIConnection(state, connection) {
    state.genAIConnections.push(connection);
    storageAPI.setGenAIConnections(state.genAIConnections);
  },
  async setGenAIConnectionState(state, args) {
    const index = state.genAIConnections.findIndex(
      (c) => c.name === args.connection.name
    );
    state.genAIConnections[index].active = args.active;
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
