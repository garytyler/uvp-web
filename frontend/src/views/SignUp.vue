<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs14 sm10 md6>
        <v-card>
          <v-card-title> Create Account </v-card-title>
          <v-card-text>
            <template>
              <v-form v-model="valid" ref="form" lazy-validation>
                <v-text-field
                  label="Full Name"
                  v-model="name"
                  required
                ></v-text-field>
                <v-text-field
                  label="Email"
                  type="email"
                  v-model="email"
                  v-validate="'required|email'"
                  data-vv-name="email"
                  :error-messages="errors.collect('email')"
                  required
                ></v-text-field>
                <v-layout align-center>
                  <v-flex>
                    <v-text-field
                      type="password"
                      ref="password"
                      label="Password"
                      data-vv-name="password"
                      data-vv-delay="100"
                      v-validate="{ required: true }"
                      v-model="password1"
                      :error-messages="errors.first('password')"
                    >
                    </v-text-field>
                    <v-text-field
                      type="password"
                      label="Confirm Password"
                      data-vv-name="password_confirmation"
                      data-vv-delay="100"
                      data-vv-as="password"
                      v-validate="{ required: true, confirmed: 'password' }"
                      v-model="password2"
                      :error-messages="errors.first('password_confirmation')"
                    >
                    </v-text-field>
                  </v-flex>
                </v-layout>
              </v-form>
            </template>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="submit" :disabled="!valid"> Submit </v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { IUserProfileCreate } from "@/interfaces";
import { dispatchGetUsers, dispatchCreateUser } from "@/store/admin/actions";

export default Vue.extend({
  data: () => {
    return {
      valid: false,
      name: "",
      email: "",
      isActive: true,
      isSuperuser: false,
      setPassword: false,
      password1: "",
      password2: "",
    };
  },
  methods: {
    reset() {
      this.password1 = "";
      this.password2 = "";
      this.name = "";
      this.email = "";
      this.isActive = true;
      this.isSuperuser = false;
      this.$validator.reset();
    },
    async submit() {
      if (await this.$validator.validateAll()) {
        const updatedProfile: IUserProfileCreate = {
          email: this.email,
        };
        if (this.name) {
          updatedProfile.name = this.name;
        }
        if (this.email) {
          updatedProfile.email = this.email;
        }
        updatedProfile.isActive = this.isActive;
        updatedProfile.isSuperuser = this.isSuperuser;
        updatedProfile.password = this.password1;
        await dispatchCreateUser(this.$store, updatedProfile);
        this.$router.push("/account/admin/users");
      }
    },
  },
  async mounted() {
    await dispatchGetUsers(this.$store);
    this.reset();
  },
});
</script>
