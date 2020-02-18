<template>
  <div>
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
              <v-icon
                color="darker-5"
                v-for="n in featureGuests.length"
                :key="n"
              >
                person
              </v-icon>
              <p v-if="featureGuests.length === 1">
                There is 1 guest ahead of you.
              </p>
              <p v-else>
                There are {{ featureGuests.length }} guests ahead of you.
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
                @keyup.native.enter="handleSubmit()"
              >
              </v-text-field>
            </v-flex>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-container>
            <v-flex text-center>
              <v-btn color="primary" large @click="handleSubmit()">
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
export default {
  data: () => ({
    dialog: false,
    editedItem: {},
    nameState: null
  }),
  computed: {
    featureTitle() {
      return this.$store.getters["guest_app/feature"].title;
    },
    featureGuests() {
      return this.$store.getters["guest_app/feature"].guests;
    },
    featureSlug() {
      return this.$store.getters["guest_app/feature"].slug;
    },
    sessionGuestName() {
      return this.$store.getters["guest_app/sessionGuest"]?.name;
    }
  },
  methods: {
    handleSubmit() {
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
            this.dialog = false;
            this.$emit("session-guest-set");
          })
          .catch(() => {
            this.dialog = true;
          });
      }
    },
    launchDialog(item) {
      console.log(item);
      this.editedIndex = this.featureGuests.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    }
  },
  mounted() {
    this.$store
      .dispatch("guest_app/loadSessionGuest")
      .then(data => {
        if (data.name) {
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
