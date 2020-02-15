import Vue from "vue";
import Vuetify from "vuetify";
import "vuetify/dist/vuetify.min.css";
import "material-design-icons-iconfont/dist/material-design-icons.css";
import { preset } from "vue-cli-plugin-vuetify-preset-rally/preset";
Vue.use(Vuetify);

export default new Vuetify({
  preset,
  theme: {
    dark: true
  }
});
