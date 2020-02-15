<template>
  <div>
    <div>
      <p class="text-center h2">{{ featureTitle }}</p>
    </div>
    <NameEditor v-on:display-name-updated="connectWebsocket()" />
    <br />
    <GuestListTable />
  </div>
</template>

<script>
import NameEditor from "@/components/NameEditor.vue";
import GuestListTable from "@/components/GuestListTable.vue";

export default {
  name: "InteractorApp",
  components: { NameEditor, GuestListTable },
  computed: {
    featureSlug() {
      return this.$store.getters["interactor/feature"].slug;
    },
    featureTitle() {
      return this.$store.getters["interactor/feature"].title;
    }
  },
  methods: {
    connectWebsocket() {
      if (!this.$store.state.socket.isConnected) {
        this.$connect(`ws://localhost:8000/ws/interactor/${this.featureSlug}/`);
      }
    }
  }
};
</script>

<style></style>
