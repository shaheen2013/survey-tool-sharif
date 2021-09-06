<template>
  <div class="container">
    <div class="row">
    <div class="col-4">
      <h3>Available list</h3>
      <div v-if="is_error" class="alert alert-danger" role="alert"> {{this.error_msg}}</div>
      <draggable
        class="dragArea list-group"
        :list="list1"
        :group="{ name: 'people', pull: 'clone', put: false }"
        :clone="cloneDog"
        @change="log"
      >
        <div class="list-group-item" v-for="element in list1" :key="element.id">
          {{ element.title }}
        </div>
      </draggable>
    </div>

    <div class="col-8 bg-light">
      <h6>Survey name</h6>
      <input v-model="survey_title" type="text" class="form-control">
      <h3>Questions</h3>
      <form @submit.prevent="submit_btn" method="POST">
        <draggable
          class="dragArea list-group"
          :list="list2"
          group="people"
          @change="log"
        >
          <div class="list-group-item border-2" v-for="(element,index) in list2" :key="element.id">
                <div class="d-flex justify-content-between mb-2">
                   Add question No {{ index+1 }}
                  <span @click="removeQue(index)" class="btn btn-danger">X</span>
                </div>
                <input v-model="element.title" class="form-control" type="element.type">
                <div v-if ="element.type === 'radio'">
                  Options
                  <textarea v-model="element.options" class="form-control"></textarea>
                </div>
                <div v-if="element.type === 'select'" >
                  <p>Options</p>
                 <textarea v-model="element.options" class="form-control"></textarea>
                </div>
                <div v-if="element.type === 'checkbox'" >
                  <p>Options</p>
                  <textarea v-model="element.options" class="form-control"></textarea>
                </div>
          </div>
        </draggable>
          <div class="mt-3">
            <button class="btn btn-primary" type="submit"> Save </button>
          </div>
        </form>
    </div>
  </div>
  </div>
</template>

<script>
import draggable from "vuedraggable";
import axios from 'axios'
let idGlobal = 1;
export default {
  name: "SurveyFormBuilder",
  display: "Custom Clone",
  order: 3,
  components: {
    draggable
  },
  data() {
    return {
      list1: [],
      list2: [],
      survey_title:"",
      is_error: false,
      error_msg:""
    };
  },
  methods: {
    submit_btn(){
      let url = '/survey-save/'
      this.list2.push({"survey_title":this.survey_title})
      axios.post(url,this.list2).then(
          res=>{
            console.log(res.data)
            if(res.data == "save"){
              this.survey_title = ""
              this.list2 = []
              this.is_error = false
              this.error_msg = ""
            }{
              this.is_error = true
              this.error_msg = res.data
              this.list2.pop()
            }

          }
      ).catch(error=>{
            console.log(error)

      })
    },
    log: function(evt) {
      if(evt.added)
        ++idGlobal
      console.log(this.list2)
    },
    cloneDog({ id }) {
      return {
        id:idGlobal,
        type: `${this.list1[id-1].type}`,
        title:"",
        options:""
      };
    },
    removeQue(index){
      this.list2.splice(index,1)
    }
  },
  mounted() {
    let url = '/question-type'
    axios.get(url)
        .then(res=>{
            this.list1 = res.data
          }
        ).catch(err=>console.log(err))
  }
};
</script>