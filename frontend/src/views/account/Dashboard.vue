<template>
  <v-card class="ma-3 pa-3">
    <v-card-title primary-title>
      <div class="headline">Dashboard</div>
    </v-card-title>
    <v-card-text>
      <div class="headline font-weight-light ma-5">
        Welcome {{ currentUserName() }}
      </div>
    </v-card-text>
    <v-card-actions>
      <div class="flex-row">
        <v-btn class="ma-1" to="/account/profile/view"> View Profile </v-btn>
        <v-btn class="ma-1" to="/account/profile/edit"> Edit Profile </v-btn>
        <v-btn class="ma-1" to="/account/profile/password">
          Change Password
        </v-btn>
      </div>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { readUserProfile } from "@/store/main/getters";
import Vue from "vue";

export default Vue.extend({
  methods: {
    currentUserName() {
      const userProfile = readUserProfile(this.$store);
      if (userProfile) {
        if (userProfile.name) {
          return userProfile.name;
        } else {
          return userProfile.email;
        }
      }
    },
  },
});
</script>
