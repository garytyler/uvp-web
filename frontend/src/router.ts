import RouterComponent from "@/components/RouterComponent.vue";
import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

export const routes = [
  {
    path: "/",
    component: () => import("@/views/Start.vue"),
    children: [
      {
        path: "",
        component: () => import("@/views/Home.vue"),
        props: true,
        children: [
          {
            path: "signup",
            component: () => import("@/views/SignUp.vue"),
          },
          {
            path: "login",
            component: () => import("@/views/Login.vue"),
          },
          {
            path: "access/recover-password",
            component: () => import("@/views/access/RecoverPassword.vue"),
          },
          {
            path: "access/reset-password",
            component: () => import("@/views/access/ResetPassword.vue"),
          },
        ],
      },
      {
        path: "account",
        component: () => import("@/views/account/Account.vue"),
        children: [
          {
            path: "",
            redirect: "/account/dashboard",
          },
          {
            path: "dashboard",
            component: () => import("@/views/account/Dashboard.vue"),
          },
          {
            path: "profile",
            component: RouterComponent,
            redirect: "profile/view",
            children: [
              {
                path: "view",
                component: () =>
                  import("@/views/account/profile/UserProfile.vue"),
              },
              {
                path: "edit",
                component: () =>
                  import("@/views/account/profile/UserProfileEdit.vue"),
              },
              {
                path: "password",
                component: () =>
                  import("@/views/account/profile/UserProfileEditPassword.vue"),
              },
            ],
          },
          {
            path: "admin",
            component: () => import("@/views/account/admin/Admin.vue"),
            redirect: "admin/users/all",
            children: [
              {
                path: "users",
                redirect: "users/all",
              },
              {
                path: "users/all",
                component: () => import("@/views/account/admin/AdminUsers.vue"),
              },
              {
                path: "users/edit/:id",
                name: "main-admin-users-edit",
                component: () => import("@/views/account/admin/EditUser.vue"),
              },
              {
                path: "users/create",
                name: "main-admin-users-create",
                component: () => import("@/views/account/admin/CreateUser.vue"),
              },
            ],
          },
        ],
      },
      {
        path: "/live",
        component: () => import("@/views/live/Live.vue"),
        children: [
          {
            path: ":featureSlug",
            component: () => import("@/views/live/LiveFeature.vue"),
            children: [
              {
                path: "lobby",
                component: () => import("@/views/live/LiveFeatureLobby.vue"),
              },
              {
                path: "interact",
                component: () => import("@/views/live/LiveFeatureInteract.vue"),
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

export const router = createRouter();
