<template>
  <div>
    <form @submit.prevent="SearchName">
      <v-row>
        <v-col md="5" cols="6">
          <v-text-field
            v-model="search.name"
            label="Search by name"
            filled
          ></v-text-field>
        </v-col>
        <v-col md="5" cols="6">
          <v-autocomplete
            label="Search by genre"
            :items="genres"
            item-value="id"
            item-text="name"
            clearable
            filled
            v-model="search.genre"
          ></v-autocomplete>
        </v-col>
        <v-col md="2" cols="12">
          <v-btn type="submit">Search</v-btn>
        </v-col>
      </v-row>
    </form>
    <v-row>
      <v-col
        md="3"
        sm="4"
        cols="6"
        v-for="(movie, index) in movies"
        :key="index"
      >
        <v-card
          :loading="$fetchState.pending"
          :to="`/movie/${movie.id}`"
          :nuxt="true"
        >
          <v-img :src="movie.poster" :lazy-src="movie.poster"></v-img>
          <v-card-title class="text-body-1 font-weight-bold">{{
            movie.name
          }}</v-card-title>
          <v-card-subtitle>
            <span v-for="(genre, index) in movie.genre" class="mr-2 d-block">{{
              genre.name
            }}</span>
            <!--            {{ movie.genre }}-->
          </v-card-subtitle>
          <v-card-text>
            <p>Release Date: {{ movie.release_year }}</p>
            <p>Budget: {{ movie.budget }} Million Dollar</p>
            <p>{{ movie.description.substring(0, 20) + ".." }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      movies: [],
      genres: [],
      search: {
        name: "",
        genre: "",
      },
    };
  },
  async fetch() {
    await this.$axios.get("/api/movie/list/create/").then((res) => {
      this.movies = res.data;
    });
    await this.$axios.get("/api/movie/genre/list/").then((res) => {
      this.genres = res.data;
    });
  },
  fetchOnServer: false,
  methods: {
    SearchName() {
      this.$axios
        .get(
          `/api/movie/list/create/?name=${this.search.name}&genre=${this.search.genre}`
        )
        .then((res) => {
          this.movies = res.data;
        });
    },
  },
};
</script>
