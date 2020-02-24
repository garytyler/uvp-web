<template>
  <v-container>
    <p class="text-center display-1 info--primary">{{ featureTitle }}</p>
    <GuestSessionInitializer v-on:session-guest-set="connectWebsocket()" />
    <div v-if="isInteractingGuest && isPresenterOnline">
      <GuestInteractControls />
    </div>
    <br />
    <GuestListTable />
  </v-container>
</template>

<script>
import GuestSessionInitializer from "@/components/GuestSessionInitializer.vue";
import GuestListTable from "@/components/GuestListTable.vue";
import GuestInteractControls from "@/components/GuestInteractControls.vue";
import { mapGetters } from "vuex";

export default {
  name: "GuestApp",
  components: {
    GuestSessionInitializer,
    GuestListTable,
    GuestInteractControls
  },
  computed: {
    ...mapGetters("guest_app", [
      "feature",
      "featureTitle",
      "featureSlug",
      "interactingGuestId",
      "sessionGuestId",
      "featurePresenterChannel"
    ]),

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
  methods: {
    connectWebsocket() {
      if (!this.$store.state.socket.isConnected) {
        this.$connect(`/ws/guest_app/${this.featureSlug}/`);
      }
    }
  },
  created() {
    this.$store.subscribe((mutation, state) => {
      if (mutation.type === "FEATURE") {
        if (
          state.sessionGuest &&
          state.sessionGuest.id === state.feature?.guests[0].id
        )
          this.interactMode = true;
      }
    });
  }
};
</script>

<style></style>
