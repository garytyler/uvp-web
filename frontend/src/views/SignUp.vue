<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs14 sm10 md6>
        <validation-observer v-slot="{ invalid }">
          <v-card>
            <v-card-title> Create Account </v-card-title>
            <v-card-text>
              <validation-provider
                v-slot="{ errors }"
                name="Name"
                rules="required|minUserName|maxUserName"
              >
                <v-text-field
                  v-model="name"
                  :error-messages="errors"
                  label="Name"
                  @keyup.enter="submit"
                  required
                ></v-text-field>
              </validation-provider>

              <validation-provider
                v-slot="{ errors }"
                name="email"
                rules="required|email"
              >
                <v-text-field
                  type="email"
                  v-model="email"
                  :error-messages="errors"
                  label="Email"
                  @keyup.enter="submit"
                  required
                ></v-text-field>
              </validation-provider>

              <validation-provider
                vid="password"
                name="Password"
                rules="required|minPassword|passwordConfirm:@confirmation"
                v-slot="{ errors }"
              >
                <v-text-field
                  type="password"
                  v-model="password"
                  :error-messages="errors"
                  label="Password"
                  @keyup.enter="submit"
                  required
                ></v-text-field>
              </validation-provider>

              <validation-provider
                vid="confirmation"
                name="Password"
                rules="required|minPassword|passwordConfirm:@password"
                v-slot="{ errors }"
              >
                <v-text-field
                  type="password"
                  v-model="confirmation"
                  :error-messages="errors"
                  label="Confirm Password"
                  @keyup.enter="submit"
                  required
                ></v-text-field>
              </validation-provider>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click="submit" :disabled="invalid"> Submit </v-btn>
            </v-card-actions>
          </v-card>
        </validation-observer>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { IUserProfileCreate } from "@/interfaces";
import { dispatchSignUp } from "@/store/main/actions";
import { ValidationObserver, ValidationProvider } from "vee-validate";

export default Vue.extend({
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  data: () => ({
    // env: env,
    name: "",
    email: "",
    password: "",
    confirmation: "",
  }),
  methods: {
    async submit() {
      const newProfile: IUserProfileCreate = {
        email: this.email,
        name: this.name,
        password: this.password,
      };
      dispatchSignUp(this.$store, newProfile)
        .catch()
        .then(() => {
          this.$router.push("/login");
        });
    },
  },
});
</script>
