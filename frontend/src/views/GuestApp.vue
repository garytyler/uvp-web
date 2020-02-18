<template>
  <v-container>
    <p class="text-center display-1 info--primary">{{ featureTitle }}</p>
    <GuestSessionInitializer v-on:session-guest-set="connectWebsocket()" />
    <br />
    <GuestListTable />
  </v-container>
</template>

<script>
import GuestSessionInitializer from "@/components/GuestSessionInitializer.vue";
import GuestListTable from "@/components/GuestListTable.vue";

export default {
  name: "GuestApp",
  components: { GuestSessionInitializer, GuestListTable },
  computed: {
    featureSlug() {
      return this.$store.getters["guest_app/feature"].slug;
    },
    featureTitle() {
      return this.$store.getters["guest_app/feature"].title;
    },
    sessionGuestId() {
      return this.$store.getters["guest_app/sessionGuest"]?.id;
    },
    sessionGuest() {
      return this.$store.getters["guest_app/sessionGuest"];
    }
  },
  methods: {
    connectWebsocket() {
      if (!this.$store.state.socket.isConnected) {
        this.$connect(`ws://localhost:8000/ws/guest_app/${this.featureSlug}/`);
      }
    }
  }
};
</script>

<style></style>
