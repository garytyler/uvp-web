import LiveFeatureSessionInteracting from "@/components/LiveFeatureSessionInteracting.vue";
import LiveFeatureSessionWaiting from "@/components/LiveFeatureSessionWaiting.vue";
import Error404PageNotFound from "@/views/errors/Error404PageNotFound.vue";
// import ErrorMessage from "@/views/errors/ErrorMessage.vue";
import LiveFeature from "@/views/LiveFeature.vue";
import Vue from "vue";
import VueRouter from "vue-router";
// import AccountApp from "./views/AccountApp.vue";

Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "user",
      // component: AccountApp,
      component: () =>
        import(/* webpackChunkName: "account-app" */ "./views/AccountApp.vue"),

      props: true,
    },
    {
      path: "/live/:featureSlug/",
      component: LiveFeature,
      props: true,
      children: [
        {
          path: "waiting",
          component: LiveFeatureSessionWaiting,
        },
        {
          path: "interacting",
          component: LiveFeatureSessionInteracting,
        },
      ],
    },
    {
      path: "*",
      name: "not-found",
      component: Error404PageNotFound,
    },
  ],
});

// router.onError((err) => {
//   router.push({
//     name: "not-found",
//     component: ErrorMessage,
//     params: { message: err.message, heading: "ERROR" },
//   });
// });

export default router;
