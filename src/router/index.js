import Vue from "vue";
import VueRouter from "vue-router";
import AccountApp from "@/views/AccountApp.vue";
import GuestApp from "@/views/GuestApp.vue";
import Error404NotFound from "@/views/errors/Error404NotFound.vue";
import store from "@/store";
import GuestListTable from "@/components/GuestListTable.vue";
import GuestInteractControls from "@/components/GuestInteractControls.vue";

Vue.use(VueRouter);

function loadFeatureBeforeRouterEnter(to, from, next) {
  let featureSlug = to.params.featureSlug;
  store
    .dispatch("guest_app/loadFeature", featureSlug)
    .then(() => {
      next();
    })
    .catch(() => {
      next(`/not-found/?message=Feature not found: ${featureSlug}`);
    });
}

const routes = [
  {
    path: "/",
    name: "user",
    component: AccountApp,
    props: true
  },
  {
    path: "/feature/:featureSlug",
    component: GuestApp,
    beforeEnter: loadFeatureBeforeRouterEnter,
    children: [
      {
        path: "",
        component: GuestListTable
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
