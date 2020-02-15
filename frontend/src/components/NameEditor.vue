<template>
  <div>
    <b-card no-body class="rounded-0" size="sm" bg-variant="light">
      <b-card-text class="mx-2 mt-2" id="display-name-label">
        <!-- <span class="text-secondary">Your Name</span> -->
        Your Name
        <p class="h2 text-wrap">
          {{ displayName }}
          <b-button
            class="m-0 p-0"
            id="edit-button"
            pill
            size="lg"
            variant="secondary-outline"
            v-b-modal.modal-display-name-editor
          >
            <p class="h2 m-0 p-0" style="font-size:1.5em;">
              <b-icon
                class="m-0 p-0"
                icon="pencil"
                variant="secondary"
              ></b-icon>
            </p>
          </b-button>
        </p>
      </b-card-text>
    </b-card>

    <b-modal
      id="modal-display-name-editor"
      size="sm"
      ref="modal"
      return-focus="body"
      title="What's your name?"
      centered
      no-close-on-backdrop
      no-close-on-esc
      hide-header-close
      cancel-disabled
      ok-disabled
      no-stacking
      @show="resetModal"
      @hidden="resetModal"
      @ok="handleOk"
      no-footer-border
      footer-border-variant="light"
      header-border-variant="light"
    >
      <template slot="modal-header">
        <b-card-title class="mx-auto my-0" id="text-center">
          What's your name?
        </b-card-title>
      </template>

      <form ref="form" @submit.stop.prevent="handleSubmit">
        <b-form-group
          class="my-0"
          :state="nameState"
          label-for="name-input"
          invalid-feedback="Name is required"
        >
          <b-form-input
            autofocus
            ref="displayNameInput"
            :placeholder="displayName || 'Enter your name'"
            id="name-input"
            v-model="displayName"
            :state="nameState"
            required
          ></b-form-input>
        </b-form-group>
      </form>

      <template slot="modal-footer" slot-scope="{ ok, cancel }">
        <b-row cols="1" class="mx-auto">
          <b-button
            size="lg"
            class="guest-signin-begin-btn my-1"
            variant="success"
            @click="ok()"
          >
            <strong>Submit</strong>
          </b-button>
          <b-button
            size="small"
            class="guest-signin-cancel-btn my-1"
            variant="secondary"
            @click="cancel()"
          >
            <strong>Cancel</strong>
          </b-button>
        </b-row>
      </template>
    </b-modal>
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
      displayName: null,
      nameState: null
    };
  },
  computed: {
    featureSlug() {
      return this.$store.getters["guest_app/feature"].slug;
    }
  },
  methods: {
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      this.nameState = valid;
      return valid;
    },
    resetModal() {
      this.nameState = null;
    },
    handleOk(bvModalEvt) {
      bvModalEvt.preventDefault("modal-display-name-editor");
      this.handleSubmit();
    },
    handleSubmit() {
      if (!this.checkFormValidity()) {
        return;
      }
      let profile = { name: this.displayName, feature_slug: this.featureSlug };
      this.$store
        .dispatch("guest_app/setDisplayName", profile)
        .then(() => {
          this.$nextTick(() => {
            this.$bvModal.hide("modal-display-name-editor");
          });
          this.$emit("display-name-updated");
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  created() {
    this.$store
      .dispatch("guest_app/loadDisplayName")
      .then(displayName => {
        if (!displayName) {
          this.$nextTick(() => {
            this.$bvModal.show("modal-display-name-editor");
          });
        } else {
          this.$nextTick(() => {
            this.$bvModal.hide("modal-display-name-editor");
          });
          this.$emit("display-name-updated");
        }
        this.displayName = displayName;
      })
      .catch(error => {
        console.log(error);
        this.$bvModal.show("modal-display-name-editor");
      });
  }
};
</script>

<style scoped></style>
