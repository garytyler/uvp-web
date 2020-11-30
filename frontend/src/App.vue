<template>
  <v-app>
    <div>
      <!-- <v-main v-if="loggedIn === null">
      <v-container fill-height>
        <v-layout align-center justify-center>
          <v-flex>
            <div class="text-xs-center">
              <div class="headline my-5">Loading...</div>
              <v-progress-circular
                size="100"
                indeterminate
                color="primary"
              ></v-progress-circular>
            </div>
          </v-flex>
        </v-layout>
      </v-container>
    </v-main> -->
      <router-view />
      <NotificationsManager></NotificationsManager>
    </div>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import NotificationsManager from "@/components/NotificationsManager.vue";
import { readIsLoggedIn } from "@/store/main/getters";
import { dispatchCheckLoggedIn } from "@/store/main/actions";

export default Vue.extend({
  components: {
    NotificationsManager,
  },
  computed: {
    loggedIn() {
      return readIsLoggedIn(this.$store);
    },
  },
  methods: {
    async created() {
      await dispatchCheckLoggedIn(this.$store);
    },
  },
});
</script>

<style>
/* Unset background-color change on app-bar buttons when active */
.v-app-bar .v-btn--active:before {
  background-color: unset;
}
</style>
