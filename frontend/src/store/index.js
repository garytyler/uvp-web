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
  plugins: debug ? [createLogger()] : [],
  // Provide low-level state management and logging for websocket activity.
  // https://github.com/nathantsoi/vue-native-websocket#vuex-store-integration
  state: {
    socket: {
      isConnected: false,
      message: "",
      reconnectError: false
    }
  },
  mutations: {
    SOCKET_ONOPEN(state, event) {
      Vue.prototype.$socket = event.currentTarget;
      state.socket.isConnected = true;
    },
    SOCKET_ONCLOSE(state, event) {
      console.info(state, event);
      state.socket.isConnected = false;
    },
    SOCKET_ONERROR(state, event) {
      console.error(state, event);
    },
    SOCKET_ONMESSAGE(state, message) {
      state.socket.message = message;
    },
    SOCKET_RECONNECT(state, count) {
      console.info(state, count);
    },
    SOCKET_RECONNECT_ERROR(state) {
      state.socket.reconnectError = true;
    }
  }
});

// VueNativeSock requires url string first arg.
// Actual url is passed to $connect call in code.
Vue.use(VueNativeSock, "ws://example.com", {
  connectManually: true,
  store: store,
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
