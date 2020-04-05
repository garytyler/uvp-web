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
          <p class="display-1 teal--text">{{ featureTitle }}</p>
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
<script>
import { mapGetters } from "vuex";
import { urlPathToWsUrl } from "@/utils/urls.js";

export default {
  props: {
    featureSlug: {
      type: String,
      required: true
    }
  },
  computed: {
    ...mapGetters("live", [
      "feature",
      "featureTitle",
      "isFeaturePresenterOnline",
      "sessionGuestIsInteractingGuest"
    ])
  },
  beforeRouteEnter(to, from, next) {
    next(vm => {
      Promise.all([
        vm.$store.dispatch("live/loadFeature", vm.featureSlug).catch(error => {
          return error;
        }),
        vm.$store
          .dispatch("live/loadSessionGuest", vm.featureSlug)
          .catch(error => {
            return error;
          })
      ]).then((feature, guest) => {
        if (!vm.$store.state.socket.isConnected) {
          vm.$connect(urlPathToWsUrl(`/ws/guest/${vm.featureSlug}/`));
        }
        let targetPath = `/live/${vm.featureSlug}/${
          !guest || !vm.sessionGuestIsInteractingGuest
            ? "waiting"
            : "interacting"
        }`;
        if (targetPath !== to.path) vm.$router.push(targetPath);
      });
    });
  }
};
</script>

<style></style>
