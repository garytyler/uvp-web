<template>
  <!-- <v-system-bar v-show="systemBarVisible" app dark>
      {{ featureTitle }}
      <v-spacer></v-spacer>
      <v-container>
        <div v-if="isFeaturePresenterOnline">
          <v-icon dense color="success" text>lens</v-icon>
        </div>
        <div v-else>
          <v-icon dense color="error" text>error_outline</v-icon>
        </div>
      </v-container>
  </v-system-bar>-->

  <v-content>
    <router-view></router-view>
  </v-content>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({});
</script>
