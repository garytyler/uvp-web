import Vue from "vue";
import Vuex, { StoreOptions } from "vuex";
import { socketModule } from "./socket";
import { mainModule } from "./main";
import { adminModule } from "./admin";
import { liveModule } from "./live";
import { State } from "./state";
import createLogger from "vuex/dist/logger";
import VueNativeSock from "vue-native-websocket";

const debug = process.env.NODE_ENV !== "production";

Vue.use(Vuex);

const storeOptions: StoreOptions<State> = {
  modules: {
    main: mainModule,
    admin: adminModule,
    live: liveModule,
    socket: socketModule,
  },
  strict: debug,
  plugins: debug ? [createLogger()] : [],
};

export const createStore = () => {
  const store = new Vuex.Store<State>(storeOptions);

  if (module.hot) {
    module.hot.accept(["./main", "./admin", "./live", "./socket"], () => {
      const newMainModule = require("./main").default;
      const newAdminModule = require("./admin").default;
      const newLiveModule = require("./live").default;
      const newSocketModule = require("./socket").default;
      store.hotUpdate({
        modules: {
          account: newMainModule,
          admin: newAdminModule,
          live: newLiveModule,
          socket: newSocketModule,
        },
      });
    });
  }

  // Actual url is passed to $connect call in code.
  Vue.use(VueNativeSock, "ws://example.com", {
    connectManually: true,
    store: store,
    format: "json",
  });

  return store;
};

export const store = createStore();
export default store;
