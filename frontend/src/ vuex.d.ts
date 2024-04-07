import { Store } from "vuex";
import { GenAiConnection } from "./models/GenAIConnection";

declare module "@vue/runtime-core" {
  // declare your own store states
  interface State {
    getters: {
      genAIConnections: Array<GenAIConnection>;
    };
  }

  // provide typings for `this.$store`
  interface ComponentCustomProperties {
    $store: Store<State>;
  }
}
