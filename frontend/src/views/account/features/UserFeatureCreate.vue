<template>
  <v-container fluid>
    <v-layout align-center justify-center>
      <v-flex xs12 sm10 md8>
        <v-card class="ma-3 pa-3">
          <v-card-title class="headline"> Create New Feature </v-card-title>
          <v-card-text>
            <validation-observer ref="observer" v-slot="{ invalid }">
              <v-form @submit.prevent="submit" @keyup.native.enter="submit">
                <validation-provider
                  v-slot="{ errors }"
                  name="Title"
                  rules="required|minFeatureTitle|maxFeatureTitle"
                >
                  <v-text-field
                    type="text"
                    v-model="title"
                    :error-messages="errors"
                    label="Title"
                    :counter="Boolean(name)"
                    required
                  ></v-text-field>
                </validation-provider>

                <validation-provider
                  v-slot="{ errors }"
                  name="Slug"
                  rules="required|alpha_dash|minFeatureSlug"
                >
                  <v-text-field
                    type="text"
                    v-model="slug"
                    :error-messages="errors"
                    label="Slug"
                    :counter="Boolean(name)"
                    required
                  ></v-text-field>
                </validation-provider>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn @click.prevent="submit" :disabled="invalid">
                    Create
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
import { IFeatureCreate } from "@/interfaces";
import { readUserProfile } from "@/store/main/getters";
import { dispatchCreateFeature } from "@/store/main/actions";
import { ValidationObserver, ValidationProvider } from "vee-validate";

export default Vue.extend({
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  data: () => {
    return {
      title: "",
      slug: "",
    };
  },
  computed: {
    userProfile() {
      return readUserProfile(this.$store);
    },
  },
  methods: {
    async submit() {
      return this.$refs.observer
        .validate()
        .catch()
        .then(() => {
          const newFeature: IFeatureCreate = {
            title: this.title,
            slug: this.slug,
            turnDuration: 180,
            userId: this.userProfile.id,
          };
          dispatchCreateFeature(this.$store, newFeature)
            .catch()
            .then(() => {
              const liveUrl = `/live/${newFeature.slug}`;
            });
        });
    },
  },
});
</script>
