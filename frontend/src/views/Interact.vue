<template>
  <div>
    <h4>Feature: {{ feature }}</h4>
    <h2>Display Name: {{ displayName }}</h2>

    <ModalDisplayNameEditor />
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import ModalDisplayNameEditor from "@/components/ModalDisplayNameEditor.vue";

export default {
  name: "Interact",
  components: { ModalDisplayNameEditor },
  computed: {
    ...mapGetters("interact", {
      feature: "getFeature",
      displayName: "getDisplayName"
    })
  }
};
</script>

<style></style>
