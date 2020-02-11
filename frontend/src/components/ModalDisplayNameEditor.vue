<template>
  <div>
    <b-button v-b-modal.modal-prevent-closing>Edit Name</b-button>

    <b-modal
      id="modal-prevent-closing"
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
      <!-- Guest name form -->
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
            placeholder="Enter your name"
            id="name-input"
            v-model="name"
            :state="nameState"
            required
          ></b-form-input>
        </b-form-group>
      </form>

      <!--  Guest name form buttons -->
      <template slot="modal-footer" slot-scope="{ ok, cancel }">
        <b-row cols="1" class="mx-auto">
          <!-- Begin button -->
          <b-btn
            size="lg"
            class="guest-signin-begin-btn my-1"
            variant="success"
            @click="ok()"
          >
            <strong>Join</strong>
          </b-btn>

          <b-btn
            size="small"
            class="guest-signin-cancel-btn my-1"
            variant="secondary"
            @click="cancel()"
          >
            <strong>Cancel</strong>
          </b-btn>
        </b-row>
      </template>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: "ModalDisplayNameEditor",
  data() {
    return {
      name: "",
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
      this.name = "";
      this.nameState = null;
    },
    handleOk(bvModalEvt) {
      // Prevent modal from closing
      bvModalEvt.preventDefault();
      // Trigger submit handler
      this.handleSubmit();
    },
    handleSubmit() {
      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return;
      }
      this.$store
        .dispatch("interactor/updateDisplayName", this.name)
        .then(() => {
          this.$bvModal.hide("modal-prevent-closing");
        })
        .catch(error => {
          console.log(error);
        });
    }
  }
};
</script>

<style scoped></style>
