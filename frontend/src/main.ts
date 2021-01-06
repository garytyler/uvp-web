import Vue from "vue";
import App from "./App.vue";
import { vuetify } from "./plugins/vuetify";
import { ValidationProvider } from "./plugins/vee-validate";
import { router } from "./router";
import { store } from "./store";

Vue.config.productionTip = false;

Vue.component("ValidationProvider", ValidationProvider);

new Vue({
  vuetify,
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
