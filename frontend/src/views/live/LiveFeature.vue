<template>
  <div>
    <v-sheet>
      <div class="text-center">
        <div class="pt-3">
          <p class="display-1 teal--text">{{ currentFeatureTitle }}</p>
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

    <v-main>
      <router-view></router-view>
    </v-main>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { store } from "@/store";
import { urlPathToWsUrl } from "@/services/urls.js";
import {
  dispatchGetCurrentFeature,
  dispatchGetCurrentGuest,
} from "@/store/live/actions";
import {
  readFeature,
  readGuest,
  readIsFeaturePresenterOnline,
  readIsCurrentGuestInteractingGuest,
} from "@/store/live/getters";

export default Vue.extend({
  computed: {
    currentFeatureTitle() {
      const feature = readFeature(this.$store);
      return feature ? feature.title : "";
    },
    currentFeature() {
      return readFeature(this.$store);
    },
    isFeaturePresenterOnline() {
      return readIsFeaturePresenterOnline(this.$store);
    },
  },
  async beforeCreate() {
    this.$store.watch(
      () => readIsCurrentGuestInteractingGuest(store),
      () => {
        const basePath = `/live/${this.$route.params.featureSlug}`;
        let targetPath;
        if (readIsCurrentGuestInteractingGuest(store)) {
          targetPath = basePath + "/interact";
        } else {
          targetPath = basePath + "/lobby";
        }
        this.$router.push(targetPath);
      }
    );
    if (!this.$store.state.socket.isConnected) {
      const featureSlug = this.$route.params.featureSlug;
      Vue.prototype.$connect(urlPathToWsUrl(`/ws/guest/${featureSlug}`));
    }
  },
  async beforeRouteEnter(to, from, next) {
    await dispatchGetCurrentFeature(store, { slugOrId: to.params.featureSlug });
    await dispatchGetCurrentGuest(store);

    const feature = readFeature(store);
    const guest = readGuest(store);

    next(() => {
      let targetChild = {};
      if (!feature) {
        targetChild = {
          path: `/live/${to.params.featureSlug}/not-found`,
        };
      } else if (guest && readIsCurrentGuestInteractingGuest(store)) {
        targetChild = { path: `/live/${to.params.featureSlug}/interact` };
      } else {
        targetChild = { path: `/live/${to.params.featureSlug}/lobby` };
      }
      if (targetChild["path"] !== to.path) next(targetChild);
    });
  },
});
</script>

<style></style>
