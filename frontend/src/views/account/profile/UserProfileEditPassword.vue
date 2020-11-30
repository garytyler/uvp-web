<template>
  <v-card class="ma-3 pa-3">
    <v-card-title class="headline"> Change Password </v-card-title>
    <v-card-text>
      <template>
        <div class="my-3">
          <div class="subheading secondary--text text--lighten-2">User</div>
          <div
            class="title primary--text text--darken-2"
            v-if="userProfile.name"
          >
            {{ userProfile.name }}
          </div>
          <div class="title primary--text text--darken-2" v-else>
            {{ userProfile.email }}
          </div>
        </div>
        <v-form ref="form">
          <v-text-field
            type="password"
            ref="password"
            label="Password"
            data-vv-name="password"
            data-vv-delay="100"
            data-vv-rules="required"
            v-validate="'required'"
            v-model="password1"
            :error-messages="errors.first('password')"
          >
          </v-text-field>
          <v-text-field
            type="password"
            label="Confirm Password"
            data-vv-name="password_confirmation"
            data-vv-delay="100"
            data-vv-rules="required|confirmed:$password"
            data-vv-as="password"
            v-validate="'required|confirmed:password'"
            v-model="password2"
            :error-messages="errors.first('password_confirmation')"
          >
          </v-text-field>
        </v-form>
      </template>
    </v-card-text>
    <v-card-actions>
      <div class="flex-row">
        <v-spacer></v-spacer>
        <v-btn class="ma-1" @click="cancel">Cancel</v-btn>
        <v-btn class="ma-1" @click="reset">Reset</v-btn>
        <v-btn class="ma-1" @click="submit" :disabled="!valid">Save</v-btn>
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
      password1: "",
      password2: "",
    };
  },
  computed: {
    userProfile() {
      return readUserProfile(this.$store);
    },
  },
  methods: {
    reset() {
      this.password1 = "";
      this.password2 = "";
      this.$validator.reset();
    },
    cancel() {
      this.$router.back();
    },
    async submit() {
      if (await this.$validator.validateAll()) {
        const updatedProfile: IUserProfileUpdate = {};
        updatedProfile.password = this.password1;
        await dispatchUpdateUserProfile(this.$store, updatedProfile);
        this.$router.push("/account/profile");
      }
    },
  },
});
</script>
