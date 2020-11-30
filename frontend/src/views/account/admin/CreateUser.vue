<template>
  <v-card class="ma-3 pa-3">
    <v-card-title primary-title>
      <div class="headline primary--text">Create User</div>
    </v-card-title>
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
          <div class="subheading secondary--text text--lighten-2">
            User is superuser
            <span v-if="isSuperuser">(currently is a superuser)</span
            ><span v-else>(currently is not a superuser)</span>
          </div>
          <v-checkbox label="Is Superuser" v-model="isSuperuser"></v-checkbox>
          <div class="subheading secondary--text text--lighten-2">
            User is active <span v-if="isActive">(currently active)</span
            ><span v-else>(currently not active)</span>
          </div>
          <v-checkbox label="Is Active" v-model="isActive"></v-checkbox>
          <v-layout align-center>
            <v-flex>
              <v-text-field
                type="password"
                ref="password"
                label="Set Password"
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
      <v-btn @click="cancel">Cancel</v-btn>
      <v-btn @click="reset">Reset</v-btn>
      <v-btn @click="submit" :disabled="!valid"> Save </v-btn>
    </v-card-actions>
  </v-card>
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
    cancel() {
      this.$router.back();
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
