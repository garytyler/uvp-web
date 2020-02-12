<template>
  <div>
    <h4>Feature: {{ feature }}</h4>
    <h2>Display Name: {{ displayName }}</h2>

    <ModalDisplayNameEditor v-on:display-name-is-set="connectWebsocket" />
  </div>
</template>

<script>
import { mapState } from "vuex";
import ModalDisplayNameEditor from "@/components/ModalDisplayNameEditor.vue";

export default {
  name: "InteractorApp",
  components: { ModalDisplayNameEditor },
  computed: {
    ...mapState("interactor", {
      feature: "feature",
      displayName: "displayName"
    })
  },
  methods: {
    connectWebsocket() {
      if (!this.$store.state.socket.isConnected) {
        this.$connect(
          `ws://localhost:8000/ws/interactor/${this.feature.slug}/`
        );
      }
    }
  }
};
</script>

<style></style>
