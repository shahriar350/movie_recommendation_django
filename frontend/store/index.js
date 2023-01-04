export const state = () => ({
  user: {},
  apiHost: "http://127.0.0.1:8000",
})
export const getters = {
  userGet(state) {
    return state.user
  }
}
export const mutations = {
  user_set(state, data) {
    state.user = data
  }
}

export const actions = {
  async nuxtServerInit({commit, app}) {
    await this.$axios.get('/api/auth/csrf/')

    await this.$axios.get('/api/auth/check/')
      .then(res => {
        commit('user_set', [true, res.data])
      }).catch(() => {
      })
  }
}
