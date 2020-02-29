import Vue from "vue";
import VueRouter from "vue-router";
import AccountApp from "@/views/AccountApp.vue";
import InteractApp from "@/views/InteractApp.vue";
import Error404NotFound from "@/views/errors/Error404NotFound.vue";
import store from "@/store";
import GuestWaitingMonitor from "@/components/GuestWaitingMonitor.vue";
import GuestInteractControls from "@/components/GuestInteractControls.vue";
import { urlPathToWsUrl } from "@/utils/urls.js";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "user",
    component: AccountApp,
    props: true
  },
  {
    path: "/feature/:feature_slug",
    redirect: to => {
      return {
        path: "/feature",
        query: { feature_slug: to.params.feature_slug }
      };
    }
  },
  {
    path: "/feature",
    component: InteractApp,
    beforeEnter: function(to, from, next) {
      let feature_slug = to.query.feature_slug;
      store
        .dispatch("interact/loadFeature", feature_slug)
        .then(() => {
          next(vm => {
            if (!vm.$store.state.socket.isConnected) {
              vm.$connect(urlPathToWsUrl(`/ws/guest/${vm.featureSlug}/`));
            }
          });
        })
        .catch(() => {
          next(`/not-found/?message=Feature not found: ${feature_slug}`);
        });
    },
    children: [
      {
        path: "",
        component: GuestWaitingMonitor
      },
      {
        path: "interact",
        component: GuestInteractControls
      }
    ]
  },
  {
    path: "/not-found",
    name: "resource-not-found",
    component: Error404NotFound,
    props: route => ({ message: route.query.message })
  },
  {
    path: "*",
    name: "page-not-found",
    component: Error404NotFound,
    props: { message: "Page Not Found" }
  }
];

const router = new VueRouter({
  mode: "history",
  routes
});

export default router;
