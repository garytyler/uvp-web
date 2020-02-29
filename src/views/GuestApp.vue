<template>
  <v-container>
    <p class="text-center display-1 info--primary">{{ featureTitle }}</p>
    <GuestSession />

    <div v-if="isInteractingGuest && isPresenterOnline">
      <GuestInteractControls />
    </div>
    <div v-else>
      <router-view />
    </div>
  </v-container>
</template>

<script>
import GuestSession from "@/components/GuestSession.vue";
import GuestInteractControls from "@/components/GuestInteractControls.vue";
import { mapGetters } from "vuex";
import { urlPathToWsUrl } from "@/utils/urls.js";

export default {
  name: "GuestApp",
  components: {
    GuestSession,
    GuestInteractControls
  },
  computed: {
    ...mapGetters("guest_app", [
      "featureTitle",
      "featureSlug",
      "interactingGuestId",
      "sessionGuestId",
      "featurePresenterChannel",
      "featureGuests"
    ]),
    isInteractingGuest() {
      return (
        this.interactingGuestId !== null &&
        this.interactingGuestId === this.sessionGuestId
      );
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
