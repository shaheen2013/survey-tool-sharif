<template>
  <div class="container">
    <div class="row">
      <div v-if="this.error_msg['title']" class="alert alert-danger text-center text-white" role="alert"> <h6>Survey title must be required</h6></div>
      <div v-if="this.is_save" class="alert alert-success text-center text-white" role="alert"> <h6>{{this.error_msg.message}}</h6></div>
      <div v-if="this.is_error" class="alert alert-danger text-center text-white" role="alert"> <h6>At list one question required</h6></div>
    <div class="col-4">
      <h3>Available list</h3>
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
                <input v-model="element.title" class="form-control" type="text">
<!--                <div v-if="index in error_list" class="alert alert-danger text-center text-white" role="alert">-->
<!--                  This field is required-->
<!--                </div>-->
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
import draggable from "vuedraggable"
import axios from 'axios'
let idGlobal = 1;
export default {
  name: "SurveyFormBuilder",
  display: "Custom Clone",
  order: 3,
  props:['edit','surveyid'],
  components: {
    draggable
  },
  data() {
    return {
      list1: [],
      list2: [],
      survey_title:"",
      is_error: false,
      error_msg:{},
      is_save: false,
      error_list:[],
      survey_item:{}
    };
  },
  methods: {
    submit_btn(){
      let url = '/survey-save/'
      this.list2.push({"survey_title":this.survey_title})
      if(this.edit === 0){
        axios.post(url,this.list2).then(
          res=>{
            this.error_msg=""
            this.error_list = []
            if(res.data['info']==='save'){
              this.survey_title = ""
              this.list2 = []
              this.is_error = false
              this.is_save = true
              this.error_msg = res.data
            }
            else{
                this.is_save = false
                this.error_msg = res.data
                if(this.error_msg['questions'][0]==='This list may not be empty.')
                  this.is_error = true
                else{
                  this.is_error = false
                  console.log(this.error_msg['questions'][0]['title'])
                }
            }
            this.list2.pop()
          }
      ).catch(error=>{
            console.log(error)
      })
      }else{
        this.list2.push({"survey_id":this.surveyid})
        axios.put(url,this.list2).then(
            res=>{
              this.list2.pop()
              this.error_msg=""
              this.error_list = []
              if(res.data['info']==='update'){
                this.survey_title = ""
                this.list2 = []
                this.is_error = false
                this.is_save = true
                this.error_msg = res.data
              }
              else{
                  this.is_save = false
                  this.error_msg = res.data
                  if(this.error_msg['questions'][0]==='This list may not be empty.')
                    this.is_error = true
                  else{
                    this.is_error = false
                    console.log(this.error_msg['questions'][0]['title'])
                  }
              }
              this.list2.pop()
            }
        ).catch(
            err=>console.log(err)
        )
      }
    },
    log: function(evt) {
      if(evt.added)
        ++idGlobal
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
    if(this.edit===0)
    {
      let url = '/question-type'
      axios.get(url)
          .then(res=>{
              this.list1 = res.data
            }
          ).catch(err=>console.log(err))
    }else{
      let url = '/question-type'
      axios.get(url)
          .then(res=>{
              this.list1 = res.data
            }
          ).catch(err=>console.log(err))
      url = '/update-survey/'+this.surveyid
      axios.get(url)
      .then(
          res=>{
            this.list2 = res.data
            this.survey_item = this.list2.pop()
            this.survey_title = this.survey_item['title']
          }
      )
      .catch(
          err=>console.log("error",err)
      )
    }
  }
};
</script>