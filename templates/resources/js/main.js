const Vue = require("vue");

// Vue.component('hello-world', require('./components/HelloWorld.vue'))
Vue.component('survey-builder', require('./components/SurveyFormBuilder.vue').default)


const app = new Vue({
    el: '#app'
})