<template>
  <div>
    <v-data-table
      no-data-text="Queue is empty."
      item-key="name"
      ref="table"
      mobile-breakpoint="0"
      :headers="headers"
      :items="currentFeature.guests"
      class="elevation-4"
      hide-default-footer
      hide-default-header
    >
      <template v-slot:top>
        <v-dialog
          persistent
          class="elevation-12"
          hide-overlay
          v-model="dialog"
          max-width="400px"
        >
          <v-card>
            <v-card-title>
              <v-container>
                <v-flex text-left>
                  <span class="headline text--info">Edit Name</span>
                </v-flex>
              </v-container>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-flex text-center>
                  <v-text-field
                    outlined
                    autofocus
                    required
                    label="Your Name"
                    v-model="editedItem.name"
                    @keyup.native.enter="handleSubmit()"
                  >
                  </v-text-field>
                </v-flex>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-container>
                <v-flex text-right>
                  <v-btn text color="accent" @click="dialog = false">
                    Cancel
                  </v-btn>
                  <v-btn text color="primary" @click="handleSubmit()">
                    Save
                  </v-btn>
                </v-flex>
              </v-container>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>

      <template v-slot:[`item.index`]="{ item }">
        <v-chip
          :color="
            (currentGuest ? item.id === currentGuest.id : false)
              ? 'info darken-2'
              : currentFeature.guests.indexOf(item) === 0
              ? 'success darken-2'
              : 'secondary'
          "
          text-color="white"
        >
          <span class="headline text--accent">
            {{ currentFeature.guests.indexOf(item) }}
          </span>
        </v-chip>
      </template>

      <template v-slot:[`item.name`]="{ item }">
        <v-chip
          :color="
            (currentGuest ? item.id === currentGuest.id : false)
              ? 'info darken-2'
              : currentFeature.guests.indexOf(item) === 0
              ? 'success darken-2'
              : 'secondary'
          "
          text-color="white"
        >
          <span class="headline">{{ item.name }}</span>
        </v-chip>
      </template>

      <template v-slot:[`item.handle`]="{ item }">
        <div v-if="currentFeature.guests.indexOf(item) > 0">
          <div class="handle">
            <v-icon small> mdi-drag </v-icon>
          </div>
        </div>
      </template>

      <template v-slot:[`item.delete-action`]="{ item }">
        <v-icon @click="deleteItem(item)"> mdi-delete </v-icon>
      </template>

      <template v-slot:[`item.edit-action`]="{ item }">
        <div v-if="featureOwner || currentGuest.id === item.id">
          <v-icon class="mr-2" @click="initEditDialog(item)">
            mdi-pencil
          </v-icon>
        </div>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import {
  dispatchUpdateGuest,
  dispatchDeleteGuest,
} from "../store/live/actions";
import { readFeature, readGuest } from "../store/live/getters";
import Sortable from "sortablejs";

export default {
  props: {
    featureOwner: {
      required: false,
      type: Boolean,
      default: true, // Set to false before deployment
    },
  },
  data: () => ({
    dialog: false,
    editedItem: {},
  }),
  computed: {
    headers() {
      const _headers = [
        {
          text: "Index",
          align: "start",
          sortable: false,
          value: "index",
        },
        {
          text: "Name",
          align: "start",
          sortable: false,
          value: "name",
        },
        {
          text: "Edit",
          value: "edit-action",
          align: "end",
          sortable: false,
        },
      ];
      if (this.featureOwner === true) {
        return [
          {
            text: "Move",
            value: "handle",
            align: "start",
            sortable: false,
          },
          ..._headers,
          {
            text: "Delete",
            align: "end",
            sortable: false,
            value: "delete-action",
          },
        ];
      } else {
        return _headers;
      }
    },
    currentFeature() {
      return readFeature(this.$store);
    },
    currentGuest() {
      return readGuest(this.$store);
    },
  },
  methods: {
    rowClick: function (item, row) {
      row.select(false);
      row.deselect(item, false);
    },

    async initEditDialog(item) {
      this.editedIndex = this.currentFeature.guests.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },
    async deleteItem(item) {
      if (confirm("Are you sure you want to delete this item?")) {
        await dispatchDeleteGuest(this.$store, { guestId: item.id });
        this.dialog = false;
      }
    },
    async handleSubmit() {
      await dispatchUpdateGuest(this.$store, {
        guestId: this.editedItem.id,
        guest: this.editedItem,
      });
      this.dialog = this.currentGuest
        ? Boolean(this.currentGuest.name == this.editedItem.name)
        : false;
    },
  },
  mounted() {
    const table = this.$refs.table.$el.querySelector("tbody");
    Sortable.create(table, {
      handle: ".handle", // Use handle so user can select text
      onEnd({ newIndex, oldIndex }) {
        try {
          const rowSelected = this.currentFeature.guests.splice(oldIndex, 1)[0]; // Get the selected row and remove it
          this.currentFeature.guests.splice(newIndex, 0, rowSelected); // Move it to the new index
        } catch {
          console.error(
            `Reordering not implemented. - newIndex=${newIndex} oldIndex=${oldIndex}`
          );
        }
      },
    });
  },
};
</script>
<style scoped>
.handle {
  cursor: move !important;
  cursor: -webkit-grabbing !important;
}
</style>
