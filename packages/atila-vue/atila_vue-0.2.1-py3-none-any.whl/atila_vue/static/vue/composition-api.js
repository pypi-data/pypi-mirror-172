// vue & vuex Shorcuts ----------------------------------------
exports.ref = Vue.ref;
exports.computed = Vue.computed
exports.watch = Vue.watch
exports.watchEffect = Vue.watchEffect
exports.getCurrentInstance = Vue.getCurrentInstance
exports.inject = Vue.inject
exports.provide = Vue.provide
exports.InjectionKey = Vue.InjectionKey
exports.onBeforeMount = Vue.onBeforeMount
exports.onMounted = Vue.onMounted
exports.onBeforeUpdate = Vue.onBeforeUpdate
exports.onUpdated = Vue.onUpdated
exports.onBeforeUnmount = Vue.onBeforeUnmount
exports.onUnmounted = Vue.onUnmounted
exports.onErrorCaptured = Vue.onErrorCaptured
exports.onRenderTracked = Vue.onRenderTracked
exports.onRenderTriggered = Vue.onRenderTriggered
exports.onActivated = Vue.onActivated
exports.onDeactivated = Vue.onDeactivated

exports.useStore = Vuex.useStore
exports.mapState = Vuex.mapState
exports.mapGetters = Vuex.mapGetters
exports.mapActions = Vuex.mapActions
exports.mapMutations = Vuex.mapMutations

exports.useRouter = VueRouter.useRouter
exports.useRoute = VueRouter.useRoute
exports.useLink = VueRouter.useLink
exports.RouterLink = VueRouter.RouterLink
exports.onBeforeRouteLeave = VueRouter.onBeforeRouteLeave
exports.onBeforeRouteUpdate = VueRouter.onBeforeRouteUpdate

// vuex mappers for coposition API -----------------------------
// https://gist.github.com/ub3rb3457/586467f2cbd54d0c96d60e16b247d151
// ex) const { countUp, countDown } = useState ()
const useState = () => {
  const store = Vuex.useStore()
  return Object.fromEntries(Object.keys(store.state).map(key => [key, Vue.computed(() => store.state[key])]))
}

const useGetters = () => {
  const store = Vuex.useStore()
  return Object.fromEntries(Object.keys(store.getters).map(getter => [getter, Vue.computed(() => store.getters[getter])]))
}

const useMutations = () => {
  const store = Vuex.useStore()
  return Object.fromEntries(Object.keys(store._mutations).map(mutation => [mutation, value => store.commit(mutation, value)]))
}

const useActions = () => {
  const store = Vuex.useStore()
  return Object.fromEntries(Object.keys(store._actions).map(action => [action, value => store.dispatch(action, value)]))
}

exports.useState = useState
exports.useGetters = useGetters
exports.useMutations = useMutations
exports.useActions = useActions
