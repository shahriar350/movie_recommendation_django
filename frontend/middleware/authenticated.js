export default function ({store, redirect, $axios}) {
  // If the user is not authenticated
  $axios.get('/api/auth/check/')
    .catch(() => {
      return redirect('/auth/login')
    })

}
