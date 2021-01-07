<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md4>
        <v-card>
          <v-card-title> Reset Password </v-card-title>
          <v-card-text>
            <p class="subheading">Enter your new password below</p>
            <validation-observer ref="observer" v-slot="{ invalid }">
              <v-form @submit.prevent="submit" @keyup.native.enter="submit">
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
                    required
                  ></v-text-field>
                </validation-provider>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn @click="cancel">Cancel</v-btn>
                  <v-btn @click="submit" :disabled="invalid">Save</v-btn>
                </v-card-actions>
              </v-form>
            </validation-observer>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { commitAddNotification } from "@/store/main/mutations";
import { dispatchResetPassword } from "@/store/main/actions";
import { ValidationObserver, ValidationProvider } from "vee-validate";

export default Vue.extend({
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  data: () => {
    return {
      password: "",
    };
  },
  mounted() {
    this.checkToken();
  },
  methods: {
    cancel() {
      this.$router.push("/");
    },
    checkToken() {
      const token = this.$router.currentRoute.query.token as string;
      if (!token) {
        commitAddNotification(this.$store, {
          content:
            "No token provided in the URL, start a new password recovery",
          type: "error",
        });
        this.$router.push("/access/request-password-recovery");
      } else {
        return token;
      }
    },
    async submit() {
      return this.$refs.observer
        .validate()
        .catch()
        .then(() => {
          const token = this.checkToken();
          if (!token) {
            return;
          }
          dispatchResetPassword(this.$store, {
            password: this.password,
            token: token,
          })
            .catch()
            .then(() => this.$router.push("/login"));
        });
    },
  },
});
</script>
