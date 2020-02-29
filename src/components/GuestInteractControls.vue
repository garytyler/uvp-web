<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="10">
        <v-row rows="3">
          <v-btn
            block
            align="stretch"
            style="height: 100px;"
            :color="isSending ? 'accent' : 'primary'"
            @click="
              isSending ? stopSendingDeviceMotion() : startSendingDeviceMotion()
            "
          >
            <span class="headline">
              {{ isSending ? "Pause" : "Start" }}
            </span>
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
            @click="stopSendingDeviceMotion()"
          >
            Exit
          </v-btn>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import Vue from "vue";
import device from "@/utils/device.js";

export default {
  data() {
    return {
      isSending: false,
      dialog: true
    };
  },
  computed: {
    ...mapGetters("interact", [
      "featurePresenterChannel",
      "sessionGuestId",
      "featureGuests"
    ])
  },
  methods: {
    startSendingDeviceMotion() {
      device.motionSender.start(Vue.prototype.$socket, 30, true);
      this.isSending = device.motionSender.isSending;
    },
    stopSendingDeviceMotion() {
      device.motionSender.stop();
      this.isSending = device.motionSender.isSending;
    },
    handleDeviceError(message) {
      alert(message);
    }
  }
};
</script>

<style scoped>
.v-btn {
  width: 100%;
}
</style>
