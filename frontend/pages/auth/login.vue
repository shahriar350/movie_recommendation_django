<template>
  <div>
    <v-card>
      <v-card-title>
        User Login
      </v-card-title>
      <v-card-subtitle v-if="Object.keys(serverErrors).length > 0">
        <div type="error" v-for="(errors,vind,key) in serverErrors" :key="key">
          <p v-for="(error,index) in errors" :key="index">{{ error }}</p>
        </div>
      </v-card-subtitle>
      <v-form @submit.prevent="submit_now()" ref="form" v-model="valid" lazy-validation>
        <v-card-text>
          <v-text-field filled v-model="form.phone_number" :rules="[v => !!v || 'Phone number required!']"
                        name="phone_number"
                        label="Phone number" required></v-text-field>
          <v-text-field filled v-model="form.password"
                        :append-icon="show3 ? 'mdi-eye' : 'mdi-eye-off'"
                        :rules="[
                          v => !!v || 'Password is required!',
                          v =>  !!v && v.length >= 6 || 'Minimum 6 character is needed!'
                          ]"
                        :type="show3 ? 'text' : 'password'"
                        name="input-10-2"
                        label="Password"
                        value="wqfasds"
                        class="input-group--focused"
                        @click:append="show3 = !show3"
          ></v-text-field>

        </v-card-text>
        <v-card-actions>

          <v-btn type="submit" color="primary">Login</v-btn>
          <v-btn to="/auth/register" :nuxt="true" outlined>Register</v-btn>

        </v-card-actions>

      </v-form>

    </v-card>

  </div>
</template>

<script>
export default {
  data() {
    return {
      valid: false,
      form: {
        name: 'saifull',
        phone_number: '',
        password: ''
      },
      serverErrors: {},
      show3: false,
    }
  },
  head() {
    return {
      title: 'Login'
    }
  },
  methods: {
    submit_now() {
      if (this.$refs.form.validate()) {
        this.$axios.post('/api/auth/login/', this.form)
          .then(res => {
            this.$toast.success("Successfully Login.")
            this.serverErrors = {}
          }).catch(err => {
          this.serverErrors = err.response.data
        })
      }
    }
  }
}
</script>
