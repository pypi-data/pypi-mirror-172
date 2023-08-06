<template>
  <article v-if='state.$debug' class='container'>
    <div class='article'>
      <h5>Vuex State</h5>
      <ul id='vuex-state'>
        <div v-for='[k, v] in Object.entries(state)' :key='k'>
          <li class='mb-0' v-if="k != 'context' && k != '$apispecs'"><b>{{ k }}</b>: {{ v }}</li>
        </div>
        <li><b>$apispecs</b>
          <ul>
            <li class='mb-0' v-for='[k, v] of Object.entries(state.$apispecs)' :key='k'>
              <b>{{ k }}</b>: {{ v }}
            </li>
          </ul>
        </li>
        <li v-if="!!state.context"><b>context</b>
          <ul>
            <li class='mb-0' v-for='[k, v] of Object.entries(state.context)' :key='k'>
              <b>{{ k }}</b>: {{ v }}
            </li>
          </ul>
        </li>
      </ul>
    </div>
    <div class='router'>
      <h5>Vue Router</h5>
      <ul>
        <li class='mb-0'>route: {{route}} } </li>
        <li class='mb-0'>router.options.base: "{{ router.options.base }}" </li>
        <li class='mb-0'>router.options.routes
          <ul>
            <li v-for='r of router.options.routes' :key='r.name'>{{ r }}</li>
          </ul>
        </li>
      </ul>
    </div>
  </article>
</template>

<style scoped>
  .article {
    color: #4904b3;
    word-break: break-all;
    margin-right: 32px;
  }
  .router {
    color: #138535;
    word-break: break-all;
    margin-right: 32px;
  }
</style>

<script>
  import { useStore, useRoute, useRouter, ref } from '/vue/composition-api.js'

  export default {
    setup () {
      const { state } = useStore ()
      const router = useRouter ()
      const route = useRoute ()

      return {state, router, route }
    }
  }
</script>
