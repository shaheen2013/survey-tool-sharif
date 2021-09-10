<template>
  <div class="container">
    <div class="row">
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
            <div class="list-group-item border-2" v-for="(element,index) in list2" :key="index">
              <div class="d-flex justify-content-between mb-2">
                Add question No {{ index + 1 }}
                <span @click="removeQue(index)" class="btn btn-danger">X</span>
              </div>
              <input v-model="element.title" class="form-control" type="text">
              <div v-if="element.type === 'radio' || element.type === 'select' || element.type === 'checkbox'">
                Options
                <textarea v-model="element.options" class="form-control"></textarea>
              </div>
            </div>
          </draggable>
          <div class="mt-3">
            <button class="btn btn-primary" type="submit"> Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import draggable from "vuedraggable"
import ApiService from "../services/api.service"
import NotificationService from "../services/notification.service";

let idGlobal = 1;
export default {
  name      : "SurveyFormBuilder",
  display   : "Custom Clone",
  props     : ['edit', 'surveyid'],
  components: {
    draggable
  },
  data() {
    return {
      list1       : [],
      list2       : [],
      survey_title: "",
      survey_item : {}
    };
  },
  methods: {
    submit_btn() {
      let url = '/survey/'
      if (this.edit === 0) {
        let info = {"title": this.survey_title, "questions": this.list2}
        ApiService.post(url, info).then(res => {
              this.survey_title = ""
              this.list2 = []
              NotificationService.success("Survey saved successfully")
            }
        ).catch(error => {
          let errors
          let error_message = []
          if (error.response.data.title) {
            error_message.push(`<p>Survey title can not be empty</p>`)
          }
          if (error.response.data['questions'][0] === 'This list may not be empty.') {
            error_message.push(`<p> Survey list should need minimum one question </p>`)
          } else {
            errors = error.response.data.questions
          }
          if (errors) {
            for (let i of Object.keys(errors)) {
              error_message.push(`<p>Question ${parseInt(i) + 1} is required</p>`)
            }
          }
          NotificationService.error(error_message)
        })
      } else {
        let info = {"title": this.survey_title, "questions": this.list2, "survey_id": this.surveyid}
        ApiService.update(url, info).then(
            res => {
              this.survey_title = ""
              this.list2 = []
              NotificationService.success("Updated!!!")
            }
        ).catch(
            err => {
              NotificationService.error("Errors")
            }
        )
      }
    },
    log: function (evt) {
      if (evt.added)
        ++idGlobal
    },
    cloneDog({id}) {
      return {
        type   : `${this.list1[id - 1].type}`,
        title  : "",
        options: ""
      };
    },
    removeQue(index) {
      this.list2.splice(index, 1)
    }
  },
  mounted() {
    let url = '/question-type'
    ApiService.get(url)
        .then(res => {
              this.list1 = res.data
            }
        ).catch(err => console.log(err))
    if (this.edit === 1) {
      let url = '/survey/' + this.surveyid
      ApiService.get(url)
          .then(
              res => {
                console.log(res.data)
                this.list2 = res.data
                this.survey_item = this.list2.pop()
                this.survey_title = this.survey_item['title']
              }
          )
          .catch(
              err => console.log("error", err)
          )
    }
  }
};
</script>