<template>
  <AppContext dashboardMode v-on="$listeners">
    <template v-slot:left-nav-drawer>
      <v-list>
        <!-- <v-list-item v-if="$vuetify.breakpoint.mobile">
          <v-list-item-content>
            <v-toolbar-title v-text="appName" class="font-weight-black">
            </v-toolbar-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider v-if="$vuetify.breakpoint.mobile"></v-divider> -->

        <v-list-item to="/account/dashboard">
          <v-list-item-action>
            <v-icon>mdi-view-dashboard</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Dashboard</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-list subheader v-show="hasAdminAccess">
        <v-divider></v-divider>
        <v-list-item to="/account/admin/users/all">
          <v-list-item-action>
            <v-icon>mdi-account-group</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Manage Users</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item to="/account/admin/users/create">
          <v-list-item-action>
            <v-icon>mdi-account-plus</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Create User</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </template>
  </AppContext>
</template>

<script lang="ts">
import Vue from "vue";
import AppContext from "@/components/AppContext.vue";
import { appName } from "@/env";
import { readHasAdminAccess } from "@/store/main/getters";
import { dispatchCheckLoggedIn } from "@/store/main/actions";
import {} from "@/store/main/mutations";
import { store } from "@/store";
import { readIsLoggedIn } from "@/store/main/getters";

const routeGuardAccount = async (to, from, next) => {
  await dispatchCheckLoggedIn(store);
  if (readIsLoggedIn(store)) {
    next();
  } else {
    next("/login");
  }
};

export default Vue.extend({
  components: { AppContext },
  data: () => {
    return {
      appName: appName,
      leftNavDrawerIsMiniature: false,
      leftNavDrawerIsVisible: false,
      rightNavDrawerIsVisible: false,
    };
  },
  computed: {
    hasAdminAccess() {
      return readHasAdminAccess(this.$store);
    },
  },
  beforeRouteEnter(to, from, next) {
    routeGuardAccount(to, from, next);
  },
  beforeRouteUpdate(to, from, next) {
    routeGuardAccount(to, from, next);
  },
});
</script>
