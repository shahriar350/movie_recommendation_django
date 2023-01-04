<template>
  <div>
    <v-card :loading="$fetchState.pending">
      <v-card-title>
        Hello, {{ auth.name }}. Here are your recommended movies.
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col
            v-if="movies.length > 0"
            md="3"
            sm="4"
            cols="6"
            v-for="(movie, index) in movies"
            :key="index"
          >
            <v-card :to="`/movie/${movie.id}`" :nuxt="true">
              <v-img :src="movie.poster" :lazy-src="movie.poster"></v-img>
              <v-card-title>{{ movie.name }}</v-card-title>
              <v-card-subtitle>
                <span
                  v-for="(genre, index) in movie.genre"
                  class="mr-2 d-block"
                  >{{ genre.name }}</span
                >
              </v-card-subtitle>
              <v-card-text>
                <p>Release Date: {{ movie.release_year }}</p>
                <p>Budget: {{ movie.budget }} Million Dollar</p>
                <p>{{ movie.description.substring(0, 20) + ".." }}</p>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col v-else> No movie is recommended for you. </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  middleware: "authenticated",
  data() {
    return {
      auth: {},
      movies: [],
    };
  },
  fetchOnServer: false,
  async fetch() {
    await this.$axios.get(`/api/auth/check/`).then((res) => {
      this.auth = res.data;
    });
    await this.$axios.get(`/api/movie/recommend/`).then((res) => {
      this.movies = res.data;
    });
  },
};
</script>
