<template>
  <div>
    <div class="row">
      <button
        class="btn btn-link"
        v-on:click="setVisibility('all')"
        :class="{ selected: getVisibility == 'all' }"
      >
        All
      </button>
      <button
        class="btn btn-link"
        v-on:click="setVisibility('completed')"
        :class="{ selected: getVisibility == 'completed' }"
      >
        Completed
      </button>
      <button
        class="btn btn-link"
        v-on:click="setVisibility('not_completed')"
        :class="{ selected: getVisibility == 'not_completed' }"
      >
        Not Completed
      </button>
    </div>
    <table class="table">
      <thead>
        <th>Bethel ID</th>
        <th>Card ID</th>
        <th>Datetime</th>
      </thead>
      <Checkin
        v-for="checkin in filteredCheckins"
        :checkin="checkin"
        :key="checkin.id"
      >
      </Checkin>
    </table>
  </div>
</template>

<script>
import Checkin from "./Checkin";
export default {
  name: "CheckinList",
  components: {
    Checkin,
  },
  props: ["checkins", "filters", "visibility"],
  methods: {
    setVisibility(newVisibility) {
      this.$emit("set-visibility", newVisibility);
    },
  },
  computed: {
    filteredCheckins: function () {
      return this.filters[this.visibility](this.checkins);
    },
    getVisibility: function () {
      return this.visibility;
    },
  },
};
</script>

<style scoped></style>
