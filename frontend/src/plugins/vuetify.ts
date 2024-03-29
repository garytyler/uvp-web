import Vue from "vue";
import Vuetify from "vuetify";
import "vuetify/dist/vuetify.min.css";

Vue.use(Vuetify);

export const createVuetify = (): Vuetify => {
  return new Vuetify({
    breakpoint: {
      mobileBreakpoint: "sm",
    },
    theme: {
      dark: false,
      themes: {
        dark: {
          primary: "#21CFF3",
          accent: "#FF4081",
          secondary: "#ffe18d",
          success: "#4CAF50",
          info: "#2196F3",
          warning: "#FB8C00",
          error: "#FF5252",
        },
        light: {
          primary: "#1976D2",
          accent: "#e91e63",
          secondary: "#30b1dc",
          success: "#4CAF50",
          info: "#2196F3",
          warning: "#FB8C00",
          error: "#FF5252",
        },
      },
    },
  });
};

export const vuetify = createVuetify();
