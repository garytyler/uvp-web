<template>
  <div>
    <div>
      <p class="text-center h2">{{ featureTitle }}</p>
    </div>
    <div>
      <DisplayNameEditor v-on:display-name-updated="connectWebsocket()" />
    </div>
    <div>
      <h4>Guest List: {{ guestList }}</h4>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import DisplayNameEditor from "@/components/DisplayNameEditor.vue";

export default {
  name: "InteractorApp",
  components: { DisplayNameEditor },
  computed: {
    ...mapGetters("interactor", {
      featureTitle: "featureTitle",
      guestList: "guestList"
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
