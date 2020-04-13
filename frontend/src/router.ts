// import LiveFeatureSessionInteracting from "@/components/LiveFeatureSessionInteracting.vue";
// import LiveFeatureSessionWaiting from "@/components/LiveFeatureSessionWaiting.vue";
import Error404PageNotFound from "@/views/errors/Error404PageNotFound.vue";
// import ErrorMessage from "@/views/errors/ErrorMessage.vue";
// import LiveFeature from "@/views/LiveFeature.vue";
import Vue from "vue";
import VueRouter from "vue-router";
// import AccountApp from "./views/AccountApp.vue";

Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      component: () =>
        import(/* webpackChunkName: "start" */ "./views/Start.vue"),
      children: [
        {
          path: "/account",
          name: "user",
          // component: AccountApp,
          component: () =>
            import(
              /* webpackChunkName: "account-app" */ "./views/AccountApp.vue"
            ),

          props: true
        },
        {
          path: "/live/:featureSlug/",
          component: () =>
            import(
              /* webpackChunkName: "live-feature" */ "./views/LiveFeature.vue"
            ),
          props: true,
          children: [
            {
              path: "waiting",
              component: () =>
                import(
                  /* webpackChunkName: "live-feature-session-waiting" */ "./views/LiveFeatureSessionWaiting.vue"
                )
            },
            {
              path: "interacting",
              component: () =>
                import(
                  /* webpackChunkName: "live-feature-session-interacting" */ "./views/LiveFeatureSessionInteracting.vue"
                )
            }
          ]
        },
        {
          path: "*",
          name: "not-found",
          component: Error404PageNotFound
        }
      ]
    }
  ]
});

// router.onError((err) => {
//   router.push({
//     name: "not-found",
//     component: ErrorMessage,
//     params: { message: err.message, heading: "ERROR" },
//   });
// });

export default router;
