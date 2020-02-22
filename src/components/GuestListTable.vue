<template>
  <v-data-table
    no-data-text="Queue is empty."
    item-key="name"
    ref="table"
    mobile-breakpoint="0"
    :headers="headers"
    :items="featureGuests"
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
                <v-btn text color="primary" @click="handleSubmit">
                  Save
                </v-btn>
              </v-flex>
            </v-container>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </template>

    <template v-slot:item.name="{ item }">
      <v-chip
        v-if="featureGuests.indexOf(item) === 0"
        color="green"
        text-color="white"
      >
        <v-avatar left class="green darken-4">
          {{ featureGuests.indexOf(item) }}
        </v-avatar>
        {{ item.name }}
      </v-chip>

      <v-chip v-if="featureGuests.indexOf(item) !== 0">
        <v-avatar left class="green darken-4">
          {{ featureGuests.indexOf(item) }}
        </v-avatar>
        {{ item.name }}
      </v-chip>
    </template>

    <template v-slot:item.handle="{ item }">
      <div v-if="featureGuests.indexOf(item) > 0">
        <div class="handle">
          <v-icon small>
            drag_handle
          </v-icon>
        </div>
      </div>
    </template>

    <template v-slot:item.delete-action="{ item }">
      <v-icon @click="deleteItem(item)">
        delete
      </v-icon>
    </template>

    <template v-slot:item.edit-action="{ item }">
      <div v-if="featureOwner || sessionGuestId === item.id">
        <v-icon class="mr-2" @click="initEditDialog(item)">
          edit
        </v-icon>
      </div>
    </template>
  </v-data-table>
</template>

<script>
import Sortable from "sortablejs";
import { mapGetters } from "vuex";

export default {
  props: {
    featureOwner: {
      required: false,
      type: Boolean,
      default: true // Set to false before deployment
    }
  },
  data: () => ({
    dialog: false,
    editedItem: {}
  }),
  computed: {
    headers() {
      let result = [
        {
          text: "Name",
          align: "start",
          sortable: false,
          value: "name"
        },
        {
          text: "Edit",
          value: "edit-action",
          align: "end",
          sortable: false
        }
      ];
      if (this.featureOwner === true) {
        return [
          {
            text: "Move",
            value: "handle",
            align: "start",
            sortable: false
          },
          ...result,
          {
            text: "Delete",
            align: "end",
            sortable: false,
            value: "delete-action"
          }
        ];
      } else {
        return result;
      }
    },
    ...mapGetters("guest_app", ["featureGuests", "sessionGuestId"])
  },
  methods: {
    initEditDialog(item) {
      console.log(item);
      this.editedIndex = this.featureGuests.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },
    deleteItem(item) {
      confirm("Are you sure you want to delete this item?") &&
        this.$store
          .dispatch("guest_app/deleteGuest", item)
          .then(() => {
            this.dialog = false;
            this.$emit("session-guest-set");
          })
          .catch(() => {
            this.dialog = true;
          });
    },
    handleSubmit() {
      this.$store
        .dispatch("guest_app/updateGuest", this.editedItem)
        .then(() => {
          this.dialog = false;
          this.$emit("session-guest-set");
        })
        .catch(() => {
          this.dialog = true;
        });
    }
  },
  mounted() {
    let table = this.$refs.table.$el.querySelector("tbody");
    const _self = this;
    Sortable.create(table, {
      handle: ".handle", // Use handle so user can select text
      onEnd({ newIndex, oldIndex }) {
        try {
          const rowSelected = _self.featureGuests.splice(oldIndex, 1)[0]; // Get the selected row and remove it
          _self.featureGuests.splice(newIndex, 0, rowSelected); // Move it to the new index
        } catch {
          console.error(
            `Reordering not implemented. - newIndex=${newIndex} oldIndex=${oldIndex}`
          );
        }
      }
    });
  }
};
</script>
<style scoped>
.handle {
  cursor: move !important;
  cursor: -webkit-grabbing !important;
}
</style>
