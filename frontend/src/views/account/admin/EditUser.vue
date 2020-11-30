<template>
  <v-card class="ma-3 pa-3">
    <v-card-title primary-title>
      <div class="headline primary--text">Edit User</div>
    </v-card-title>
    <v-card-text>
      <template>
        <div class="my-3">
          <div class="subheading secondary--text text--lighten-2">Username</div>
          <div class="title primary--text text--darken-2" v-if="user">
            {{ user.email }}
          </div>
          <div class="title primary--text text--darken-2" v-else>-----</div>
        </div>
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
            <v-flex shrink>
              <v-checkbox v-model="setPassword" class="mr-2"></v-checkbox>
            </v-flex>
            <v-flex>
              <v-text-field
                :disabled="!setPassword"
                type="password"
                ref="password"
                label="Set Password"
                data-vv-name="password"
                data-vv-delay="100"
                v-validate="{ required: setPassword }"
                v-model="password1"
                :error-messages="errors.first('password')"
              >
              </v-text-field>
              <v-text-field
                v-show="setPassword"
                type="password"
                label="Confirm Password"
                data-vv-name="password_confirmation"
                data-vv-delay="100"
                data-vv-as="password"
                v-validate="{ required: setPassword, confirmed: 'password' }"
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
import { IUserProfileUpdate } from "@/interfaces";
import { dispatchGetUsers, dispatchUpdateUser } from "@/store/admin/actions";
import { readAdminOneUser } from "@/store/admin/getters";

export default Vue.extend({
  data: () => {
    return {
      valid: true,
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
      this.setPassword = false;
      this.password1 = "";
      this.password2 = "";
      this.$validator.reset();
      if (this.user) {
        this.name = this.user.name;
        this.email = this.user.email;
        this.isActive = this.user.isActive;
        this.isSuperuser = this.user.isSuperuser;
      }
    },
    cancel() {
      this.$router.back();
    },
    async submit() {
      if (await this.$validator.validateAll()) {
        const updatedProfile: IUserProfileUpdate = {};
        if (this.name) {
          updatedProfile.name = this.name;
        }
        if (this.email) {
          updatedProfile.email = this.email;
        }
        updatedProfile.isActive = this.isActive;
        updatedProfile.isSuperuser = this.isSuperuser;
        if (this.setPassword) {
          updatedProfile.password = this.password1;
        }
        await dispatchUpdateUser(this.$store, {
          // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
          id: this.user!.id,
          user: updatedProfile,
        });
        this.$router.push("/account/admin/users");
      }
    },
  },
  computed: {
    user() {
      return readAdminOneUser(this.$store)(
        +this.$router.currentRoute.params.id
      );
    },
  },
  async mounted() {
    await dispatchGetUsers(this.$store);
    this.reset();
  },
});
</script>
