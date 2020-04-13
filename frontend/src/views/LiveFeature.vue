<template>
  <div>
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
    </v-system-bar> -->

    <v-sheet>
      <div class="text-center">
        <div class="pt-3">
          <p class="display-1 teal--text">{{ currentFeature.title }}</p>
        </div>
        <v-row justify="center">
          <div v-if="isFeaturePresenterOnline">
            <v-alert dense icon="lens" color="success" text>
              <span class="success--text">Online</span>
            </v-alert>
          </div>
          <div v-else>
            <v-alert dense icon="error_outline" color="error" text>
              <span class="error--text">Offline</span>
            </v-alert>
          </div>
        </v-row>
      </div>
    </v-sheet>

    <v-content>
      <router-view> </router-view>
    </v-content>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { store } from "../store";
import { urlPathToWsUrl } from "../services/urls.js";
import {
  readFeature,
  readIsFeaturePresenterOnline,
  readIsCurrentGuestInteractingGuest
} from "../store/live/getters";

export default Vue.extend({
  computed: {
    currentFeature() {
      return readFeature(this.$store);
    },
    isFeaturePresenterOnline() {
      return readIsFeaturePresenterOnline(this.$store);
    }
  },

  async beforeCreate() {
    if (!this.$store.state.socket.isConnected) {
      const featureSlug = this.$route.params.featureSlug;
      Vue.prototype.$connect(urlPathToWsUrl(`/ws/guest/${featureSlug}`));
    }
  },
  async beforeRouteEnter(to, from, next) {
    next(vm => {
      vm.$store.watch(
        () => readIsCurrentGuestInteractingGuest(store),
        () => {
          if (readIsCurrentGuestInteractingGuest(store)) {
            vm.$router.push(`/live/${to.params.featureSlug}/interacting`);
          } else {
            vm.$router.push(`/live/${to.params.featureSlug}/waiting`);
          }
        }
      );
    });
  }
});
</script>

<style></style>
