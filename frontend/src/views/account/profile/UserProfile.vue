<template>
  <v-card class="ma-3 pa-3">
    <v-card-title class="headline"> User Profile </v-card-title>
    <v-card-text>
      <div class="my-4">
        <div class="subheading secondary--text text--lighten-3">Full Name</div>
        <div
          class="title primary--text text--darken-2"
          v-if="userProfile && userProfile.name"
        >
          {{ userProfile.name }}
        </div>
        <div class="title primary--text text--darken-2" v-else>-----</div>
      </div>
      <div class="my-3">
        <div class="subheading secondary--text text--lighten-3">Email</div>
        <div
          class="title primary--text text--darken-2"
          v-if="userProfile && userProfile.email"
        >
          {{ userProfile.email }}
        </div>
        <div class="title primary--text text--darken-2" v-else>-----</div>
      </div>
    </v-card-text>
    <v-card-actions>
      <div class="flex-row">
        <v-btn class="ma-1" to="/account/profile/edit">Edit</v-btn>
        <v-btn class="ma-1" to="/account/profile/password">
          Change password
        </v-btn>
      </div>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import { readUserProfile } from "@/store/main/getters";

export default Vue.extend({
  computed: {
    userProfile() {
      return readUserProfile(this.$store);
    },
  },
  methods: {
    goToEdit() {
      this.$router.push("/account/profile/edit");
    },

    goToPassword() {
      this.$router.push("/account/profile/password");
    },
  },
});
</script>
