const Vue = require("vue");

// Vue.component('hello-world', require('./components/HelloWorld.vue'))
Vue.component('survey-builder', require('./components/SurveyFormBuilder.vue').default)
Vue.component('survey-preview', require('./components/SurveyPreview.vue').default)
import ApiService from './services/api.service'

import Swal from 'sweetalert2'
window.Swal = require('sweetalert2');
//Toast
window.Toast = Swal.mixin({
  toast: true,
  position: 'top-end',
  showConfirmButton: false,
  timer: 3000,
  timerProgressBar: true,
  didOpen: (toast) => {
    toast.addEventListener('mouseenter', Swal.stopTimer)
    toast.addEventListener('mouseleave', Swal.resumeTimer)
  }
});


window.apiservice = ApiService
ApiService.init();
const app = new Vue({
    el: '#app'
})