<template>
  <v-card class="ma-3 pa-3">
    <v-card-title class="headline"> Create New Feature </v-card-title>
    <v-card-text>
      <template>
        <v-form v-model="valid" ref="form" lazy-validation>
          <v-text-field label="Title" v-model="title" required></v-text-field>
          <v-text-field label="Slug" v-model="slug" required></v-text-field>
        </v-form>
      </template>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <div class="flex-row">
        <v-btn class="ma-1" @click="submit" :disabled="!valid"> Create </v-btn>
      </div>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import { IFeatureCreate } from "@/interfaces";
import { readUserProfile } from "@/store/main/getters";
import { dispatchCreateFeature } from "@/store/main/actions";

export default Vue.extend({
  data: () => {
    return {
      valid: true,
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
      // eslint-disable-next-line
      if ((this.$refs.form as any).validate()) {
        const newFeature: IFeatureCreate = {
          title: this.title,
          slug: this.slug,
          turnDuration: 180,
          userId: this.userProfile.id,
        };
        await dispatchCreateFeature(this.$store, newFeature);
      }
    },
  },
});
</script>
