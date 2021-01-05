<template>
  <v-parallax dark src="https://cdn.vuetifyjs.com/images/parallax/material.jpg">
    <v-row align="center" justify="center">
      <v-col class="text-center" cols="12">
        <h1 class="display-1 font-weight-thin mb-4">{{ appName }}</h1>
        <h4 class="subheading">{{ appDescription }}</h4>
      </v-col>
    </v-row>
  </v-parallax>
</template>

<script lang="ts">
import { appName, appDescription } from "@/env";
import Vue from "vue";

export default Vue.extend({
  data: () => {
    return {
      appName: appName as string,
      appDescription: appDescription as string,
    };
  },
});
</script>
