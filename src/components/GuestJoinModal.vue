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
              <v-icon color="darker-5" v-for="n in numFeatureGuests" :key="n">
                person
              </v-icon>
              <p v-if="numFeatureGuests === 1">
                There is 1 guest ahead of you.
              </p>
              <p v-else>
                There are {{ numFeatureGuests }} guests ahead of you.
              </p>
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
              >
              </v-text-field>
            </v-flex>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-container>
            <v-flex text-center>
              <v-btn color="primary" large @click="handleSignUpSubmit()">
                Join
              </v-btn>
            </v-flex>
          </v-container>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import device from "@/utils/device.js";

export default {
  data: () => ({
    sessionGuestLoaded: false,
    editedItem: {},
    nameState: null,
    status: "NO STATUS"
  }),
  computed: {
    ...mapGetters("guest_app", [
      "featureTitle",
      "featureGuests",
      "featureSlug",
      "sessionGuestName",
      "sessionGuestId",
      "isPresenterOnline"
    ]),
    numFeatureGuests() {
      return isNaN(this.featureGuests?.length) ? 0 : this.featureGuests.length;
    },
    sessionGuestIsInFeatureGuests() {
      return this.featureGuests.some(i => i.id === this.sessionGuestId);
    },
    showSignupModal() {
      if (!this.sessionGuestLoaded) {
        return false;
      } else {
        return !this.sessionGuestIsInFeatureGuests;
      }
    }
  },
  methods: {
    async handleSignUpSubmit() {
      await device.getOrientationPermissions();
      this.$store.dispatch("guest_app/setSessionGuest", {
        name: this.editedItem.name,
        feature_slug: this.featureSlug
      });
    }
  },
  beforeCreate() {
    if (!this.$store.sessionGuest) {
      this.$store
        .dispatch("guest_app/loadSessionGuest")
        .then(() => {
          this.sessionGuestLoaded = true;
        })
        .catch(() => {
          this.sessionGuestLoaded = true;
        });
    }
  }
};
</script>

<style scoped></style>
