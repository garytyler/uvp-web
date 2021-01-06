<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs14 sm10 md6>
        <v-card>
          <v-card-title> Edit User Profile </v-card-title>
          <v-card-text>
            <validation-observer ref="observer" v-slot="{ invalid }">
              <v-form @keyup.native.enter="submit">
                <validation-provider
                  v-slot="{ errors }"
                  name="Name"
                  rules="required|minUserName|maxUserName"
                >
                  <v-text-field
                    v-model="name"
                    :error-messages="errors"
                    label="Name"
                    :counter="Boolean(name)"
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
                    required
                  ></v-text-field>
                </validation-provider>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn class="ma-1" @click="reset">Reset</v-btn>
                  <v-btn @click.prevent="submit" :disabled="invalid">
                    Save
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
import { IUserProfileUpdate } from "@/interfaces";
import { readUserProfile } from "@/store/main/getters";
import { dispatchUpdateUserProfile } from "@/store/main/actions";
import { ValidationObserver, ValidationProvider } from "vee-validate";

export default Vue.extend({
  components: { ValidationObserver, ValidationProvider },
  data: () => {
    return {
      name: "",
      email: "",
      mounted: false,
    };
  },
  computed: {
    userProfile() {
      return readUserProfile(this.$store);
    },
  },
  created() {
    this.reset();
  },
  methods: {
    reset() {
      const userProfile = readUserProfile(this.$store);
      if (userProfile) {
        this.name = userProfile.name;
        this.email = userProfile.email;
      }
    },

    async submit() {
      if (this.$refs.observer.validate()) {
        const updatedProfile: IUserProfileUpdate = {};
        if (this.name) {
          updatedProfile.name = this.name;
        }
        if (this.email) {
          updatedProfile.email = this.email;
        }
        dispatchUpdateUserProfile(this.$store, updatedProfile)
          .catch()
          .then(this.$router.push("/account/profile"));
      }
    },
  },
});
</script>
