import Vue from "vue";
import VueRouter from "vue-router";
import AccountApp from "@/views/AccountApp.vue";
import GuestApp from "@/views/GuestApp.vue";
import Error404NotFound from "@/views/errors/Error404NotFound.vue";
import store from "@/store";

Vue.use(VueRouter);

var loadFeatureBeforeRouterEnter = function(to, from, next) {
  store
    .dispatch("guest_app/loadFeature", to.params.feature_slug)
    .then(function() {
      next();
    })
    .catch(error => {
      let message = `Feature not found: ${error.config.url}`;
      next(`/not-found/?message=${message}`);
    });
};

const routes = [
  {
    path: "/",
    name: "user",
    component: AccountApp,
    props: true
  },
  {
    path: "/feature/:feature_slug",
    name: "guest-app",
    component: GuestApp,
    beforeEnter: loadFeatureBeforeRouterEnter
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
