<template>
  <div>
    ASDFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    <v-dialog
      persistent
      class="elevation-12"
      hide-overlay
      v-model="dialog"
      max-width="400px"
    >
      <v-card>
        <v-card-title>
          <v-flex text-center>
            <span class="headline text--info">{{ featureTitle }}</span>
          </v-flex>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-flex text-center text--secondary>
              <v-icon color="darker-5" v-for="n in numFeatureGuests" :key="n">
                person
              </v-icon>
              <p v-if="numFeatureGuests === 1">
                There is 1 guest ahead of you.
              </p>
              <p v-else>
                There are {{ numFeatureGuests }} guests ahead of you.
              </p>
            </v-flex>
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
    {{ status }}
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import device from "@/utils/device.js";

export default {
  data: () => ({
    dialog: false,
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
      "isPresenterOnline"
    ]),
    numFeatureGuests() {
      return isNaN(this.featureGuests?.length) ? 0 : this.featureGuests.length;
    }
  },
  methods: {
    async handleSignUpSubmit() {
      const permissions = await device.getOrientationPermissions();
      if (permissions === true) {
        this.dialog = false;
        this.$emit("session-guest-set");
      } else {
        this.dialog = true;
      }

      if (
        this.editedItem.name &&
        this.editedItem.name === this.sessionGuestName
      ) {
        this.dialog = false;
      } else {
        this.$store
          .dispatch("guest_app/setSessionGuest", {
            name: this.editedItem.name,
            feature_slug: this.featureSlug
          })
          .then(() => {
            this.$emit("session-guest-set");
            this.dialog = false;
          })
          .catch(() => {
            this.dialog = true;
          });
      }
    }
  },
  async mounted() {
    this.$store
      .dispatch("guest_app/loadSessionGuest")
      .then(data => {
        if (data.name && this.featureGuests.some(i => i.id === data.id)) {
          this.dialog = false;
          this.$emit("session-guest-set");
        } else {
          this.dialog = true;
        }
      })
      .catch(() => {
        this.dialog = true;
      });
  }
};
</script>

<style scoped></style>
