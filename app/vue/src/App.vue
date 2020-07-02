<template>
  <div>
    <CheckinList
      v-bind:checkins="checkins"
      v-bind:filters="filters"
      v-bind:visibility="visibility"
      v-on:set-visibility="setVisibility"
    >
    </CheckinList>
  </div>
</template>

<script>
import CheckinList from "./components/CheckinList";

var filters = {
  all: function (checkins) {
    return checkins;
  },

  completed: function (checkins) {
    return checkins.filter(function (checkin) {
      return checkin.completed == 1;
    });
  },

  not_completed: function (checkins) {
    return checkins.filter(function (checkin) {
      return checkin.completed == 0;
    });
  },
};

import { mapState } from "vuex";
export default {
  name: "App",
  components: {
    CheckinList,
  },

  methods: {
    setVisibility(visibility) {
      this.$store.dispatch("checkins/setVisibility", visibility);
    },
  },

  computed: {
    ...mapState({
      visibility: (state) => state.checkins.visibility,
      checkins: (state) => state.checkins.checkins,
    }),
  },

  created() {
    this.$store.dispatch("checkins/loadCheckins");
  },

  data() {
    return {
      filters: filters,
      // editedCheckin: null,
    };
  },
};
</script>
