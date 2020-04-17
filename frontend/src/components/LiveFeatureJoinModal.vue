<template>
  <div v-cloak>
    <v-dialog
      persistent
      class="elevation-12"
      hide-overlay
      max-width="400px"
      v-model="showSignupModal"
    >
      <v-card>
        <v-card-title>
          <v-flex text-center>
            <span class="headline text--info">{{ featureTitle }}</span>
          </v-flex>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row justify="center" class="text--secondary">
              <v-icon color="darker-5" v-for="n in numFeatureGuests" :key="n">person</v-icon>
              <p v-if="numFeatureGuests === 1">There is 1 guest ahead of you.</p>
              <p v-else>There are {{ numFeatureGuests }} guests ahead of you.</p>
            </v-row>
          </v-container>
          <v-container>
            <v-flex text-center>
              <v-text-field
                outlined
                autofocus
                required
                label="Your Name"
                placeholder="What's your name?"
                v-model="editedItem.name"
                @keyup.native.enter="handleSignUpSubmit()"
              ></v-text-field>
            </v-flex>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-container>
            <v-flex text-center>
              <v-btn color="primary" large @click="handleSignUpSubmit()">Join</v-btn>
            </v-flex>
          </v-container>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { readGuest, readFeature } from "../store/live/getters";
import {
  dispatchCreateCurrentGuest,
  dispatchGetCurrentGuest
} from "../store/live/actions";
import device from "@/services/device.js";
export default {
  name: "live-feature-join-modal",
  data: () => ({
    currentGuestLoaded: false,
    editedItem: {},
    nameState: null,
    status: "NO STATUS"
  }),
  computed: {
    feature() {
      return readFeature(this.$store);
    },
    featureTitle() {
      return this.feature ? this.feature.title : "...";
    },
    currentGuest() {
      return readGuest(this.$store);
    },
    numFeatureGuests() {
      const feature = readFeature(this.$store);
      return isNaN(feature.guests?.length) ? 0 : this.feature.guests.length;
    },
    currentGuestIsInFeatureGuests() {
      if (!this.currentGuest) return false;
      return this.feature.guests.some(i => i.id === this.currentGuest.id);
    },
    showSignupModal() {
      return !(this.currentGuest && this.currentGuestIsInFeatureGuests);
    }
  },
  methods: {
    async handleSignUpSubmit() {
      await device.getOrientationPermissions();
      await dispatchCreateCurrentGuest(this.$store, {
        name: this.editedItem.name,
        featureId: this.feature.id
      });
    }
  },
  async beforeCreate() {
    if (!readGuest(this.$store)) {
      await dispatchGetCurrentGuest(this.$store);
    }
  }
};
</script>

<style scoped></style>
