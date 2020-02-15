import "es6-promise/auto";
// import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import router from "./router";
import store from "./store";

// Vue.use(BootstrapVue);
// Vue.use(IconsPlugin);

// import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.config.productionTip = false;

new Vue({
  vuetify,
  router,
  store,
  render: h => h(App)
}).$mount("#app");
