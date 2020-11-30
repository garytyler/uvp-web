<template>
  <v-main>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card elevation="12" class="ma-3 pa-3">
            <v-card-title class="headline"> Login </v-card-title>
            <v-card-text>
              <v-form @keyup.enter="submit">
                <v-text-field
                  @keyup.enter="submit"
                  v-model="email"
                  prepend-icon="mdi-account"
                  name="login"
                  label="Email"
                  type="text"
                ></v-text-field>
                <v-text-field
                  @keyup.enter="submit"
                  v-model="password"
                  prepend-icon="mdi-key"
                  name="password"
                  label="Password"
                  id="password"
                  type="password"
                ></v-text-field>
              </v-form>
              <div v-if="loginError">
                <v-alert
                  :value="loginError"
                  transition="fade-transition"
                  type="error"
                >
                  Incorrect email or password
                </v-alert>
              </div>
              <v-flex class="caption text-xs-right"
                ><router-link to="/access/recover-password"
                  >Forgot your password?</router-link
                ></v-flex
              >
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click.prevent="submit">Login</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-main>
</template>

<script lang="ts">
import Vue from "vue";
import { appName } from "@/env";
import { readLoginError } from "@/store/main/getters";
import { dispatchLogIn } from "@/store/main/actions";

export default Vue.extend({
  data: () => {
    return {
      email: "",
      password: "",
      appName: appName,
    };
  },
  computed: {
    loginError() {
      return readLoginError(this.$store);
    },
  },
  methods: {
    submit() {
      dispatchLogIn(this.$store, {
        username: this.email,
        password: this.password,
      });
    },
  },
});
</script>

<style>
</style>
