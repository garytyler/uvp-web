<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="10">
        <v-row rows="3">
          <v-btn
            block
            align="stretch"
            style="height: 100px"
            :disabled="!isFeaturePresenterOnline"
            :color="isSending ? 'accent' : 'primary'"
            @click="
              isSending ? stopSendingDeviceMotion() : startSendingDeviceMotion()
            "
          >
            <span class="headline">{{ isSending ? "Stop" : "Start" }}</span>
          </v-btn>
        </v-row>
      </v-col>
    </v-row>

    <v-row justify="center" class="mt-12">
      <v-col cols="6">
        <v-row>
          <v-btn
            block
            align="stretch"
            color="accent darken-4"
            @click="onExitButtonPressed()"
            >Exit</v-btn
          >
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { store } from "@/store";
import { readIsFeaturePresenterOnline, readGuest } from "@/store/live/getters";
import { dispatchDeleteGuest } from "@/store/live/actions";
import device from "@/services/device";

export default Vue.extend({
  data() {
    return {
      isSending: false,
      dialog: true,
    };
  },
  computed: {
    isFeaturePresenterOnline() {
      return readIsFeaturePresenterOnline(this.$store);
    },
  },
  methods: {
    startSendingDeviceMotion() {
      device.motionSender.start(Vue.prototype.$socket, 30);
      this.isSending = device.motionSender.isSending;
    },
    stopSendingDeviceMotion() {
      device.motionSender.stop();
      this.isSending = device.motionSender.isSending;
    },
    handleDeviceError(message) {
      alert(message);
    },
    onExitButtonPressed() {
      const guest = readGuest(store);
      if (guest) {
        dispatchDeleteGuest(store, { guestId: guest.id });
      }
      this.stopSendingDeviceMotion();
    },
  },
});
</script>

<style scoped>
.v-btn {
  width: 100%;
}
</style>
