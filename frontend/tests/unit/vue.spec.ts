import App from "@/App.vue";
import { createVuetify } from "@/plugins/vuetify";
import { createRouter } from "@/router.ts";
import { createStore } from "@/store";
import Home from "@/views/Main.vue";
import { createLocalVue, mount } from "@vue/test-utils";
import VueRouter from "vue-router";
import Vuex from "vuex";

const createTestVue = () => {
  const localVue = createLocalVue();
  localVue.use(VueRouter);
  localVue.use(Vuex);
  const store = createStore();
  const router = createRouter();
  const vuetify = createVuetify();
  return { vuetify, store, router, localVue };
};

const createWrapper = () => {
  const { localVue, store, router, vuetify } = createTestVue();
  const wrapper = mount(App, {
    localVue,
    router,
    store,
    vuetify,
  });
  return wrapper;
};

it("Home w/ vue test utils", async () => {
  const wrapper = createWrapper();
  await wrapper.vm.$router.push("/");
  await wrapper.vm.$nextTick();
  expect(wrapper.find(Home).exists()).toBe(true);
});
