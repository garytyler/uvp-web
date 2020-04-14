import Vue from "vue";
import VueRouter from "vue-router";

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
              path: "lobby",
              component: () =>
                import(
                  /* webpackChunkName: "live-feature-session-waiting" */ "./views/LiveFeatureLobby.vue"
                )
            },
            {
              path: "interact",
              component: () =>
                import(
                  /* webpackChunkName: "live-feature-session-interacting" */ "./views/LiveFeatureInteract.vue"
                )
            }
          ]
        },
        {
          path: "*",
          name: "not-found",
          component: () =>
            import(
              /* webpackChunkName: "live-feature-session-interacting" */ "./views/errors/Error404PageNotFound.vue"
            )
        },
        {
          path: "*",
          name: "error-message",
          component: () =>
            import(
              /* webpackChunkName: "live-feature-session-interacting" */ "./views/errors/Error404PageNotFound.vue"
            )
        }
      ]
    }
  ]
});

// router.onError(err => {
//   router.push({
//     name: "error-message",
//     // component: ErrorMessage,
//     params: { message: err.message, heading: "ERROR" }
//   });
// });

export default router;
