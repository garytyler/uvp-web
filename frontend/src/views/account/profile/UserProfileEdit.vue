<template>
  <v-card class="ma-3 pa-3">
    <v-card-title class="headline"> Edit User Profile </v-card-title>
    <v-card-text>
      <template>
        <v-form v-model="valid" ref="form" lazy-validation>
          <v-text-field
            label="Full Name"
            v-model="name"
            required
          ></v-text-field>
          <v-text-field
            label="E-mail"
            type="email"
            v-model="email"
            v-validate="'required|email'"
            data-vv-name="email"
            :error-messages="errors.collect('email')"
            required
          ></v-text-field>
        </v-form>
      </template>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <div class="flex-row">
        <v-btn class="ma-1" @click="cancel">Cancel</v-btn>
        <v-btn class="ma-1" @click="reset">Reset</v-btn>
        <v-btn class="ma-1" @click="submit" :disabled="!valid"> Save </v-btn>
      </div>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import { IUserProfileUpdate } from "@/interfaces";
import { readUserProfile } from "@/store/main/getters";
import { dispatchUpdateUserProfile } from "@/store/main/actions";

export default Vue.extend({
  data: () => {
    return {
      valid: true,
      name: "",
      email: "",
    };
  },
  computed: {
    userProfile() {
      return readUserProfile(this.$store);
    },
  },
  created() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile) {
      this.name = userProfile.name;
      this.email = userProfile.email;
    }
  },
  methods: {
    reset() {
      const userProfile = readUserProfile(this.$store);
      if (userProfile) {
        this.name = userProfile.name;
        this.email = userProfile.email;
      }
    },
    cancel() {
      this.$router.back();
    },
    async submit() {
      // eslint-disable-next-line
      if ((this.$refs.form as any).validate()) {
        const updatedProfile: IUserProfileUpdate = {};
        if (this.name) {
          updatedProfile.name = this.name;
        }
        if (this.email) {
          updatedProfile.email = this.email;
        }
        await dispatchUpdateUserProfile(this.$store, updatedProfile);
        this.$router.push("/account/profile");
      }
    },
  },
});
</script>
