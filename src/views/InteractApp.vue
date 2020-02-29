<template>
  <div>
    <v-system-bar v-show="systemBarVisible" app dark>
      {{ featureTitle }}
      <v-spacer></v-spacer>
      <div v-if="isPresenterOnline">
        <v-icon dense color="success" text>lens</v-icon>
      </div>
      <div v-else>
        <v-icon dense color="error" text>error_outline</v-icon>
      </div>
    </v-system-bar>

    <v-sheet>
      <div class="text-center">
        <div class="pt-3">
          <p class="display-1 teal--text">{{ featureTitle }}</p>
        </div>
        <v-row justify="center">
          <div v-if="isPresenterOnline">
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
      <router-view />
    </v-content>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "InteractApp",
  data() {
    return {
      systemBarVisible: false
    };
  },
  computed: {
    ...mapGetters("interact", [
      "featureTitle",
      "featureSlug",
      "interactingGuestId",
      "sessionGuestId",
      "featurePresenterChannel",
      "featureGuests",
      "isPresenterOnline"
    ])
  }
};
</script>

<style></style>
