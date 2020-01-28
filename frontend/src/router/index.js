import Vue from "vue";
import VueRouter from "vue-router";
import UserApp from "@/views/UserApp.vue";
import GuestApp from "@/views/GuestApp.vue";
// import Error404ResourceNotFound from "@/views/Error404ResourceNotFound.vue";
// import Error404PageNotFound from "@/views/Error404PageNotFound.vue";
import Error404NotFound from "@/views/Error404NotFound.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "user",
    component: UserApp,
    props: true
  },

  {
    path: "/feature/:feature_slug",
    name: "guest",
    component: GuestApp,
    props: route => ({ feature_slug: route.query.feature_slug })
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
