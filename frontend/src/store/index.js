import Vue from "vue";
import Vuex from "vuex";
import createLogger from "vuex/dist/logger";
import guest_app from "./modules/guest_app";
Vue.use(Vuex);

const debug = process.env.NODE_ENV !== "production";

export default new Vuex.Store({
  modules: {
    guest_app
  },
  strict: debug,
  plugins: [createLogger()]
  // plugins: debug ? [createLogger()] : []
});
