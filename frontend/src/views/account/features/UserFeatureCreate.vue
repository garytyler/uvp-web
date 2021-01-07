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
                    :counter="Boolean(title)"
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
                    :counter="Boolean(slug)"
                    required
                  ></v-text-field>
                </validation-provider>

                <validation-provider
                  v-slot="{ errors }"
                  name="Turn Duration"
                  rules="required|integer"
                >
                  <v-select
                    v-model="turnDuration"
                    :items="durationItems"
                    :error-messages="errors"
                    label="Turn Duration"
                    type="number"
                    required
                  ></v-select>
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
  props: {},
  data: () => {
    return {
      title: "" as string,
      slug: "" as string,
      turnDuration: Number,
      durationItems: [
        {
          text: "30 seconds",
          value: 30,
        },
        {
          text: "1 minute",
          value: 60,
        },
        {
          text: "1 min. 30 sec.",
          value: 90,
        },
        {
          text: "2 minutes",
          value: 120,
        },
        {
          text: "2 min. 30 sec.",
          value: 150,
        },
        {
          text: "3 minutes",
          value: 180,
        },
        {
          text: "3 min. 30 sec.",
          value: 210,
        },
        {
          text: "4 minutes",
          value: 240,
        },
        {
          text: "4 min. 30 sec.",
          value: 270,
        },
        {
          text: "5 minutes",
          value: 300,
        },
      ],
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
            turnDuration: this.turnDuration,
            userId: this.userProfile.id,
          };
          dispatchCreateFeature(this.$store, newFeature)
            .catch()
            .then(() => this.$router.push("/account/dashboard"));
        });
    },
  },
});
</script>
