<template>
  <div>
    <v-card :loading="$fetchState.pending">
      <v-row class="justify-center">
        <v-col cols="6">
          <v-img :src="movie.image" />
        </v-col>
      </v-row>

      <v-card-title>{{ movie.name }}</v-card-title>
      <v-card-subtitle>
        <span v-for="(genre, index) in movie.genre" class="mr-3">{{
          genre.name
        }}</span>
      </v-card-subtitle>
      <v-card-text>
        <p>Release Date: {{ movie.release_year }}</p>
        <p>{{ movie.description }}</p>
      </v-card-text>
    </v-card>
    <v-card class="mt-3" v-if="Object.keys(auth).length > 0">
      <v-card-title> {{ movie.name }} Rating </v-card-title>
      <v-card-text>
        <v-form
          @submit.prevent="updateRating()"
          ref="form"
          v-model="valid"
          v-if="Object.keys(auth).length > 0"
        >
          <v-slider
            v-model="rating"
            :rules="rules"
            label="Your rating"
            step="1"
            thumb-label="always"
            ticks
            max="10"
            min="0"
          ></v-slider>
          <v-btn color="primary" type="submit">Submit</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
    <div v-else>
      <v-btn @click="dialogTog">Do you want to review??</v-btn>

      <login_comp :dialog="authON"></login_comp>
    </div>
  </div>
</template>

<script>
import login_comp from "@/components/login_comp";
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      movie: {},
      ratingData: {},
      valid: false,
      rating: 0,
      authON: false,
      rules: [(v) => v <= 10 || "Maximum rating is 10"],
    };
  },
  components: {
    login_comp,
  },
  watch: {
    auth(newValue) {
      if (Object.keys(newValue).length > 0) {
        this.authON = false;
      }
    },
  },
  computed: {
    ...mapGetters({
      auth: "userGet",
    }),
  },
  async fetch() {
    await this.$axios
      .get(`/api/movie/list/create/${this.$route.params.slug}/`)
      .then((res) => {
        this.movie = res.data;
      });

    await this.$axios
      .get(`/api/movie/rating/${this.$route.params.slug}/`)
      .then((res) => {
        this.ratingData = res.data;
        if ("rating" in res.data && res.data.rating > 0) {
          this.rating = res.data.rating;
        }
      });
  },
  methods: {
    dialogTog() {
      this.authON = !this.authON;
    },
    updateRating() {
      this.$axios.post(`/api/movie/rating/${this.$route.params.slug}/`, {
        rating: this.rating,
      });
    },
  },
  fetchOnServer: false,
};
</script>
