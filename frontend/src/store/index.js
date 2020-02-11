import Vue from "vue";
import Vuex from "vuex";
import createLogger from "vuex/dist/logger";
import interact from "./modules/interact";
Vue.use(Vuex);

const debug = process.env.NODE_ENV !== "production";

const store = new Vuex.Store({
  modules: {
    interact
  },
  strict: debug,
  plugins: debug ? [createLogger()] : []
});

if (module.hot) {
  module.hot.accept(["./modules/interact"], () => {
    const newInteractModule = require("./modules/interact").default;
    store.hotUpdate({
      modules: {
        interact: newInteractModule
      }
    });
  });
}

export default store;
