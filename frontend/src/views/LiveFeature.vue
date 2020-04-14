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
  dispatchGetFeature,
  dispatchGetCurrentGuest
} from "../store/live/actions";
import {
  readFeature,
  readGuest,
  readIsFeaturePresenterOnline,
  readIsCurrentGuestInteractingGuest
} from "../store/live/getters";

const beforeRouteEnterRoutine = async (to, from, next) => {
  await dispatchGetFeature(store, { slugOrId: to.params.featureSlug });
  await dispatchGetCurrentGuest(store);

  const feature = readFeature(store);
  const guest = readGuest(store);

  if (!feature) {
    console.error("NO FEATURE!"); // TODO
  } else {
    const sessionPhase =
      !guest || !readIsCurrentGuestInteractingGuest(store)
        ? "lobby"
        : "interact";
    next(() => {
      const targetPath = `/live/${to.params.featureSlug}/${sessionPhase}`;
      if (targetPath !== to.path) next(targetPath);
    });
  }
};

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
    this.$store.watch(
      () => readIsCurrentGuestInteractingGuest(store),
      () => {
        const basePath = `/live/${this.$route.params.featureSlug}`;
        if (readIsCurrentGuestInteractingGuest(store)) {
          this.$router.push(basePath + "/interact");
        } else {
          this.$router.push(basePath + "/lobby");
        }
      }
    );
    if (!this.$store.state.socket.isConnected) {
      const featureSlug = this.$route.params.featureSlug;
      Vue.prototype.$connect(urlPathToWsUrl(`/ws/guest/${featureSlug}`));
    }
  },
  async beforeRouteEnter(to, from, next) {
    await beforeRouteEnterRoutine(to, from, next);
  }
});
</script>

<style></style>
