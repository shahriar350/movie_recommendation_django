<template>
  <div>
    <v-dialog v-model="dialog" persistent max-width="600px">
      <v-card v-if="loginCard">
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
            <div class="d-flex justify-space-between" style="width: 100%">
              <div>
                <v-btn type="submit" color="primary">Login</v-btn>
                <v-btn @click="loginCard=false" outlined>Register</v-btn>
              </div>
              <div>
                <v-btn @click="dialog=false">Reset</v-btn>
              </div>
            </div>


          </v-card-actions>

        </v-form>

      </v-card>

      <v-card v-else>
        <v-card-title>
          User Registrations
        </v-card-title>
        <v-card-subtitle v-if="Object.keys(serverErrors).length > 0">
          <div type="error" v-for="(errors,vind,key) in serverErrors" :key="key">
            <p v-for="(error,index) in errors" :key="index">{{ error }}</p>
          </div>
        </v-card-subtitle>
        <v-form @submit.prevent="register_now()" ref="regform" v-model="valid" lazy-validation>
          <v-card-text>
            <v-text-field filled v-model="regForm.name" :rules="[v => !!v || 'Name is required!']" label="Name"
                          name="name"
                          required></v-text-field>

            <v-text-field filled v-model="regForm.phone_number" :rules="[v => !!v || 'Phone number required!']"
                          name="phone_number"
                          label="Phone number" required></v-text-field>
            <v-text-field filled v-model="regForm.password"
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


            <div class="d-flex justify-space-between" style="width: 100%">
              <div>
                <v-btn type="submit" color="primary">Register now</v-btn>
                <v-btn @click="loginCard = true" outlined>Login</v-btn>
              </div>
              <div>
                <v-btn @click="dialog=false">Reset</v-btn>
              </div>
            </div>

          </v-card-actions>

        </v-form>

      </v-card>


    </v-dialog>
  </div>

</template>

<script>
export default {
  props: {
    dialog: {
      type: Boolean,
      default: false,
    }
  },
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
      loginCard: true,
      regForm: {
        name: '',
        phone_number: '',
        password: ''
      },
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
            this.$store.commit('user_set', res.data)
          }).catch(err => {
          this.serverErrors = err.response.data
        })
      }
    },
    register_now() {

      console.log(this.$refs.regform.validate())
      if (this.$refs.regform.validate()) {
        this.$axios.post('/api/auth/register/', this.form)
          .then(res => {
            this.$toast.success("Successfully registered.")
            this.serverErrors = {}
          }).catch(err => {
          this.serverErrors = err.response.data
        })
      }
    }
  }
}
</script>
