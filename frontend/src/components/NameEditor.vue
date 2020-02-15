<template>
  <div>
    <v-row justify="center">
      <v-dialog v-model="dialog" persistent max-width="400px">
        <template v-slot:activator="{ on }">
          <v-btn color="secondary" size="sm" dark v-on="on">Edit Name</v-btn>
        </template>

        <v-card>
          <v-card-title class="align-center">
            <span class="headline">What's your name?</span>
          </v-card-title>

          <v-card-text>
            <v-container>
              <v-row>
                <v-col>
                  <v-text-field
                    outlined
                    autofocus
                    required
                    placeholder="Enter your name"
                    :value="displayName"
                    v-model="submittedDisplayName"
                    @keyup.native.enter="handleSubmit()"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>

          <v-card-actions>
            <v-spacer />
            <div v-if="displayName">
              <v-row dense>
                <v-col>
                  <v-btn
                    color="primary"
                    text-color="green darken-4"
                    @click="handleSubmit()"
                    >Submit</v-btn
                  >
                </v-col>

                <v-col>
                  <v-btn
                    color="accent"
                    @click="dialog = false"
                    v-if="displayName"
                    >Cancel</v-btn
                  >
                </v-col>
              </v-row>
            </div>

            <v-flex v-else text-xs-center align-center>
              <v-col>
                <v-btn color="primary" large @click="handleSubmit()">
                  Submit
                </v-btn>
              </v-col>
            </v-flex>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "NameEditor",
  props: {
    callback: { required: false, type: Function }
  },
  data() {
    return {
      dialog: false,
      submittedDisplayName: null,
      nameState: null
    };
  },
  computed: {
    featureSlug() {
      return this.$store.getters["guest_app/feature"].slug;
    },
    displayName() {
      return this.$store.getters["guest_app/displayName"];
    }
  },
  methods: {
    handleSubmit() {
      if (
        this.submittedDisplayName &&
        this.submittedDisplayName === this.displayName
      ) {
        this.dialog = false;
      } else {
        this.$store
          .dispatch("guest_app/setDisplayName", {
            name: this.submittedDisplayName,
            feature_slug: this.featureSlug
          })
          .then(() => {
            this.dialog = false;
            this.$emit("display-name-updated");
          })
          .catch(() => {
            this.dialog = true;
          });
      }
    }
  },
  created() {
    this.$store
      .dispatch("guest_app/loadDisplayName")
      .then(displayName => {
        if (displayName) {
          console.log("YES");
          console.log(displayName);
          this.dialog = false;
          this.$emit("display-name-updated");
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
