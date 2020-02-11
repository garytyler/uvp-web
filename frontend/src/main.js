import "es6-promise/auto";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
import Vue from "vue";
import App from "@/App";
import store from "./store";
import router from "./router";

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
