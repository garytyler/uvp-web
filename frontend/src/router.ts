import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
Vue.use(VueRouter);

export const routes = [
  {
    path: "",
    component: () => import("@/views/Start.vue"),
    children: [
      {
        path: "",
        component: () => import("@/views/Home.vue"),
        props: true,
      },
      {
        path: "account",
        component: () => import("@/views/Account.vue"),
      },
      {
        path: "live",
        component: () => import("@/views/Live.vue"),
        children: [
          {
            path: ":featureSlug",
            component: () => import("@/views/LiveFeature.vue"),
            children: [
              {
                path: "lobby",
                component: () => import("@/views/LiveFeatureLobby.vue"),
              },
              {
                path: "interact",
                component: () => import("@/views/LiveFeatureInteract.vue"),
              },
              {
                path: "not-found",
                props: { code: 404, message: "Feature not found." },
                component: () => import("@/views/errors/ErrorMessage.vue"),
              },
            ],
          },
        ],
      },
    ],
  },
  {
    path: "*",
    // redirect: "/", // Consider for deployment
    component: () => import("@/views/errors/Error404PageNotFound.vue"),
  },
];

export const createRouter = () => {
  return new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes: routes,
  });
};

export default createRouter();
