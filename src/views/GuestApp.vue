<template>
  <v-container>
    <p class="text-center display-1 info--primary">{{ featureTitle }}</p>
    <GuestSessionInitializer />

    <div v-if="isInteractingGuest && isPresenterOnline">
      <GuestInteractControls />
    </div>
    <div v-else>
      <router-view />
    </div>
  </v-container>
</template>

<script>
import GuestSessionInitializer from "@/components/GuestSessionInitializer.vue";
import GuestInteractControls from "@/components/GuestInteractControls.vue";
import { mapGetters } from "vuex";
import { urlPathToWsUrl } from "@/utils/urls.js";

export default {
  name: "GuestApp",
  components: {
    GuestSessionInitializer,
    GuestInteractControls
  },
  computed: {
    ...mapGetters("guest_app", [
      "feature",
      "featureTitle",
      "featureSlug",
      "interactingGuestId",
      "sessionGuestId",
      "featurePresenterChannel",
      "featureGuests"
    ]),
    receiveFeatureGuests() {
      return this.featureGuests;
    },
    isInteractingGuest() {
      let result = this.interactingGuestId === this.sessionGuestId;
      return result;
    },
    isPresenterOnline() {
      if (
        this.featurePresenterChannel &&
        this.featurePresenterChannel.length > 0
      ) {
        return true;
      } else {
        return false;
      }
    }
  },
  created() {
    if (!this.$store.state.socket.isConnected) {
      this.$connect(urlPathToWsUrl(`/ws/guest/${this.featureSlug}/`));
    }
  }
};
</script>

<style></style>
