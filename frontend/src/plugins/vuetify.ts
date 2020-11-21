import "material-design-icons-iconfont/dist/material-design-icons.css";
import Vue from "vue";
import Vuetify from "vuetify";
import "vuetify/dist/vuetify.min.css";

Vue.use(Vuetify);

export const createVuetify = () => {
  return new Vuetify({
    theme: {
      dark: true,
    },
  });
};

export default createVuetify();
