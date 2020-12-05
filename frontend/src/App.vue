<template>
  <v-app>
    <div>
      <router-view />
      <!-- <NotificationsManager> </NotificationsManager> -->
    </div>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
// import NotificationsManager from "@/components/NotificationsManager.vue";
import { readIsLoggedIn } from "@/store/main/getters";

export default Vue.extend({
  // components: {
  //   NotificationsManager,
  // },
});
</script>

<style>
/* Unset background-color change on app-bar buttons when active */
.v-app-bar .v-btn--active:before {
  background-color: unset;
}
</style>
