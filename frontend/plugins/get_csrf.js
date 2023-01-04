export default function ({$axios, app}) {

  const csrftoken = app.$cookies.get('csrftoken');
  console.log(csrftoken)
  // if (!csrftoken) {
  //   $axios.get('/api/auth/csrf')
  // }

  $axios.onRequest((config) => {
    $axios.setHeader('X-CSRFToken', csrftoken)
    config.xsrfCookieName = "csrf_bongo"
    config.xsrfHeaderName = "X-CSRFToken"
  })

}
