<template>
  <AppContext>
    <template v-slot:app-bar>
      <div class="hidden-xs-only">
        <v-btn
          v-for="item in menuItems"
          :key="item.title"
          :to="item.path"
          :text="!item.rounded"
          :rounded="item.rounded"
          :class="item.rounded ? 'ma-1' : ''"
          :color="item.color ? item.color : ''"
        >
          {{ item.title }}
        </v-btn>
      </div>
    </template>

    <template v-slot:left-nav-drawer>
      <v-list>
        <v-list-item
          v-for="item in menuItems"
          :key="item.title"
          :to="item.path"
        >
          <v-list-item-content>{{ item.title }}</v-list-item-content>
        </v-list-item>
      </v-list>
    </template>
  </AppContext>
</template>

<script lang="ts">
import AppContext from "@/components/AppContext.vue";
import { appName } from "@/env";
import { readIsLoggedIn } from "@/store/main/getters";
import { store } from "@/store";
import Vue from "vue";

export default Vue.extend({
  components: { AppContext },
  data: () => ({
    appName: appName,
    rightNavDrawerVisible: false,
    leftNavDrawerVisible: false,
  }),
  computed: {
    menuItems(this) {
      const publicMenuItems = [
        {
          title: "About",
          path: "/about",
          rounded: false,
          color: "" as string,
        },
      ];
      if (readIsLoggedIn(store)) {
        return publicMenuItems.concat([
          {
            title: "My Dashboard",
            path: "/account",
            rounded: true,
            color: "secondary",
          },
        ]);
      } else {
        return publicMenuItems.concat([
          {
            title: "Sign up",
            path: "/signup",
            rounded: true,
            color: "accent darken-2",
          },
          {
            title: "Login",
            path: "/login",
            rounded: true,
            color: "secondary",
          },
        ]);
      }
    },
  },
});
</script>
