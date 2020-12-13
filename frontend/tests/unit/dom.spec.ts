import "@testing-library/jest-dom";
import App from "@/App.vue";
import { vuetify } from "@/plugins/vuetify";
import { routes } from "@/router.ts";
import "@testing-library/jest-dom";
import { render, RenderResult } from "@testing-library/vue";
import VueRouter from "vue-router";

export const renderRoute = async function(
  urlPath: string,
  routerRef?: VueRouter
): Promise<RenderResult> {
  const result: RenderResult = render(
    App,
    { vuetify, routes },
    (vue, store, router) => {
      routerRef = router;
    }
  );
  await routerRef?.push(urlPath); // Might be best to @ts-ignore routerRef here
  return result;
};

it("Home w/ testing-library", async () => {
  const { getByText } = await renderRoute("/");
  expect(getByText("UVP Interactive")).toBeTruthy();
});
