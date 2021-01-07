<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md6>
        <v-card>
          <v-card-title class="headline"> Request Password Reset </v-card-title>
          <v-card-text>
            <p class="subheading">
              A password reset email will be sent to the registered account
              email.
            </p>
            <validation-observer ref="observer" v-slot="{ invalid }">
              <v-form @submit.prevent="submit" @keyup.native.enter="submit">
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
                    required
                  ></v-text-field>
                </validation-provider>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn @click="cancel">Cancel</v-btn>
                  <v-btn @click.prevent="submit" :disabled="invalid">
                    Send
                  </v-btn>
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
import { dispatchSendPasswordResetEmail } from "@/store/main/actions";
import { ValidationObserver, ValidationProvider } from "vee-validate";

export default Vue.extend({
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  data: () => {
    return {
      email: "",
    };
  },
  methods: {
    cancel() {
      this.$router.back();
    },
    async submit() {
      await this.$refs.observer
        .validate()
        .catch()
        .then(async () => {
          dispatchSendPasswordResetEmail(this.$store, { email: this.email })
            .catch()
            .then(() => {
              this.$router.push("/login");
            });
        });
    },
  },
});
</script>

<style>
</style>
