<template>
  <v-main>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card elevation="12" class="ma-3 pa-3">
            <v-card-title class="headline"> Reset Password </v-card-title>
            <v-card-text>
              <p class="subheading">
                A password recovery email will be sent to the registered account
              </p>
              <v-form
                @keyup.enter="submit"
                v-model="valid"
                ref="form"
                @submit.prevent=""
                lazy-validation
              >
                <v-text-field
                  @keyup.enter="submit"
                  label="Email"
                  type="text"
                  prepend-icon="mdi-account"
                  v-model="username"
                  v-validate="'required'"
                  data-vv-name="username"
                  :error-messages="errors.collect('username')"
                  required
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click="cancel">Cancel</v-btn>
              <v-btn @click.prevent="submit" :disabled="!valid">
                Recover Password
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-main>
</template>

<script lang="ts">
import { appName } from "@/env";
import { dispatchPasswordRecovery } from "@/store/main/actions";
import Vue from "vue";

export default Vue.extend({
  data: () => {
    return { valid: true, username: "", appName: appName };
  },
  methods: {
    cancel() {
      this.$router.back();
    },
    submit() {
      dispatchPasswordRecovery(this.$store, { username: this.username });
    },
  },
});
</script>

<style>
</style>
