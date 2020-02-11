import Vue from "vue";
import Vuex from "vuex";
import createLogger from "vuex/dist/logger";
import interactor from "./modules/interactor";
import VueNativeSock from "vue-native-websocket";

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== "production";

const store = new Vuex.Store({
  modules: {
    interactor
  },
  strict: debug,
  plugins: debug ? [createLogger()] : []
});

Vue.use(VueNativeSock, "ws://localhost:9090", {
  connectManually: true,
  format: "json"
});

if (module.hot) {
  module.hot.accept(["./modules/interactor"], () => {
    const newInteractorModule = require("./modules/interactor").default;
    store.hotUpdate({
      modules: {
        interactor: newInteractorModule
      }
    });
  });
}

export default store;
