import Vue from "vue";
import VueRouter from "vue-router";
import UserApp from "@/views/UserApp.vue";
import GuestApp from "@/views/GuestApp.vue";

Vue.use(VueRouter);

export default new VueRouter({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "user",
      component: UserApp,
      props: true
    },
    {
      path: "/:slug",
      name: "guest",
      props: true,
      component: GuestApp
    }
  ]
});
