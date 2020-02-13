<template>
  <div>
    <b-button v-b-modal.modal-display-name-editor>Edit Name</b-button>
    <b-modal
      id="modal-display-name-editor"
      size="sm"
      ref="modal"
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
        <b-card-title class="mx-auto my-0 text-center">
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
            :placeholder="displayName || 'Enter your name'"
            id="name-input"
            v-model="displayName"
            :state="nameState"
            required
          ></b-form-input>
        </b-form-group>
      </form>
      <div v-if="loading">
        <b-spinner></b-spinner>
      </div>
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
  name: "ModalDisplayNameEditor",
  props: {
    callback: { required: false, type: Function }
  },
  data() {
    return {
      loading: false,
      displayName: null,
      nameState: null
    };
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
      bvModalEvt.preventDefault();
      this.handleSubmit();
    },
    handleSubmit() {
      if (!this.checkFormValidity()) {
        return;
      }
      this.$store
        .dispatch("interactor/setDisplayName", this.displayName)
        .then(() => {
          this.$bvModal.hide("modal-display-name-editor");
          this.$emit("display-name-updated");
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  created() {
    this.$store
      .dispatch("interactor/loadDisplayName")
      .then(displayName => {
        console.log(displayName);
        if (!displayName) {
          this.$bvModal.show("modal-display-name-editor");
        } else {
          this.$bvModal.hide("modal-display-name-editor");
          this.$emit("display-name-updated");
        }
        this.displayName = displayName;
      })
      .catch(error => {
        console.log(error);
        this.$bvModal.show("modal-display-name-editor");
        this.$emit("display-name-updated");
      });
  }
};
</script>

<style scoped></style>
