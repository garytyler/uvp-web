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
    path: "/feature/:featureSlug",
    component: InteractApp,
    beforeEnter: function(to, from, next) {
      let featureSlug = to.params.featureSlug;
      store
        .dispatch("interact/loadFeature", featureSlug)
        .then(() => {
          next(vm => {
            if (!vm.$store.state.socket.isConnected) {
              vm.$connect(urlPathToWsUrl(`/ws/guest/${vm.featureSlug}/`));
            }
          });
        })
        .catch(() => {
          next(`/not-found/?message=Feature not found: ${featureSlug}`);
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
