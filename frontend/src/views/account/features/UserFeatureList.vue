<template>
  <v-container fluid>
    <v-card>
      <v-card-title> Features </v-card-title>
      <v-card-text>
        <!-- <v-layout align-center justify-center> -->
        <v-flex xs12 sm6 md4>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-flex>
        <!-- </v-layout> -->
      </v-card-text>
      <v-data-table
        :headers="headers"
        :items="features"
        :items-per-page="10"
        class="elevation-1"
      ></v-data-table>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { readUserProfile, readCurrentUserFeatures } from "@/store/main/getters";
import { dispatchGetUserFeatures } from "@/store/main/actions";

export default Vue.extend({
  props: {},
  data: () => {
    return {
      headers: [
        {
          text: "Title",
          align: "start",
          sortable: false,
          value: "title",
        },
        {
          text: "Slug",
          align: "start",
          sortable: false,
          value: "slug",
        },
        {
          text: "Turn Duration",
          align: "start",
          sortable: false,
          value: "turnDuration",
        },
      ],
    };
  },
  computed: {
    userProfile() {
      return readUserProfile(this.$store);
    },
    features() {
      return readCurrentUserFeatures(this.$store);
    },
  },
  methods: {
    async refresh() {
      await dispatchGetUserFeatures(this.$store);
    },
  },
  async mounted() {
    await this.refresh();
  },
});
</script>
