<template>
  <div>
    <h4>Feature: {{ feature }}</h4>
    <h2>Display Name: {{ displayName }}</h2>

    <ModalDisplayNameEditor />

    <br />
    <b-button variant="success" @click="connectWebsocket()">Connect</b-button>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import ModalDisplayNameEditor from "@/components/ModalDisplayNameEditor.vue";

export default {
  name: "InteractorApp",
  components: { ModalDisplayNameEditor },
  computed: {
    ...mapGetters("interactor", {
      feature: "feature",
      displayName: "displayName"
    })
  },
  methods: {
    connectWebsocket() {
      this.$connect(`ws://localhost:8000/ws/interactor/${this.feature.slug}/`);
    }
  }
};
</script>

<style></style>
