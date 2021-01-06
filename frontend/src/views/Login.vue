<template>
  <v-container fluid>
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md4>
        <v-card>
          <v-card-title class="headline"> Login </v-card-title>
          <v-card-text>
            <!-- <validation-observer ref="observer" v-slot="{ invalid }"> -->
            <v-form @submit.prevent="submit" @keyup.native.enter="submit">
              <v-text-field
                v-model="email"
                prepend-icon="mdi-account"
                name="login"
                label="Email"
                type="text"
              ></v-text-field>

              <v-text-field
                v-model="password"
                prepend-icon="mdi-key"
                name="password"
                label="Password"
                id="password"
                type="password"
              ></v-text-field>

              <div v-if="loginError">
                <v-alert
                  :value="loginError"
                  transition="fade-transition"
                  type="error"
                >
                  Incorrect email or password
                </v-alert>
              </div>
              <v-flex class="caption text-xs-right">
                <router-link to="/access/request-password-recovery">
                  Forgot your password?
                </router-link>
              </v-flex>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click.prevent="submit">Login</v-btn>
              </v-card-actions>
            </v-form>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { readLoginError } from "@/store/main/getters";
import { dispatchLogIn } from "@/store/main/actions";

export default Vue.extend({
  data: () => {
    return {
      email: "",
      password: "",
    };
  },
  computed: {
    loginError() {
      return readLoginError(this.$store);
    },
  },
  methods: {
    async submit() {
      await dispatchLogIn(this.$store, {
        username: this.email,
        password: this.password,
      });
    },
  },
});
</script>

<style>
</style>
