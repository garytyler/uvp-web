import App from "@/App.vue";
import vuetify from "@/plugins/vuetify";
import { routes } from "@/router.ts";
import store from "@/store";
import Home from "@/views/Home.vue";
import "@testing-library/jest-dom";
import { render } from "@testing-library/vue";
import { createLocalVue, mount } from "@vue/test-utils";
import VueRouter from "vue-router";
const localVue = createLocalVue();
localVue.use(VueRouter);

beforeEach(() => {
  process.env.NODE_ENV = "production";
});

test("Home w/ testing-library", async () => {
  let routerRef: VueRouter | string[];
  const { getByText } = render(
    App,
    { vuetify, routes },
    (vue, store, router) => {
      routerRef = router;
    }
  );
  // @ts-ignore
  await routerRef.push("/");
  expect(getByText("[Home]")).toBeTruthy();
});

test("Home w/ vue test utils", async () => {
  const router = new VueRouter({ mode: "history", routes: routes });
  const wrapper = mount(App, {
    localVue,
    vuetify,
    router,
    store,
  });
  await router.push("/");
  await wrapper.vm.$nextTick();
  expect(wrapper.find(Home).exists()).toBe(true);
});
