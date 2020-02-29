<template>
  <div>
    <v-system-bar app>
      <v-spacer></v-spacer>
      <span>Status: {{ isPresenterOnline ? "Online" : "Offline" }}</span>
    </v-system-bar>
    <v-content>
      <v-container>
        <p class="text-center display-1 info--primary">{{ featureTitle }}</p>
        <router-view />
      </v-container>
    </v-content>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "InteractApp",
  computed: {
    ...mapGetters("interact", [
      "featureTitle",
      "featureSlug",
      "interactingGuestId",
      "sessionGuestId",
      "featurePresenterChannel",
      "featureGuests"
    ]),
    isPresenterOnline() {
      return (
        this.featurePresenterChannel && this.featurePresenterChannel.length > 0
      );
    }
  }
};
</script>

<style></style>
