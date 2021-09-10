<template>
  <div class="container mt-5">
    <div class="col-10 bg-light">
      <h6>Survey name: {{ survey_title }}</h6>
      <h3>Questions</h3>
      <div>
        <form @submit.prevent="submit_btn" method="POST">
          <div class="list-group-item border-2" v-for="(element,index) in questions" :key="index">
            <label>{{ element.title }}</label>
            <div v-if="element.type === 'checkbox' ">
              <div v-for="choice in element.choices">
                <input type="checkbox" value=choice> <label> {{ choice }} </label><br>
              </div>
            </div>
            <div v-if="element.type === 'radio' ">
              <div v-for="choice in element.choices">
                <input type="radio" value=choice> <label> {{ choice }} </label><br>

              </div>
            </div>
            <div v-if="element.type === 'select' ">
              <select>
                  <option v-for="choice in element.choices">{{choice}}</option>
              </select>
            </div>
            <div v-else-if="element.type === 'file' ">
              <input type='file'>
            </div>
            <div v-else-if="element.type==='date'">
              <input type="date">
            </div>
            <div v-else-if="element.type==='textarea'">
              <textarea class="form-control"></textarea>
            </div>
            <div v-else-if="element.type==='text'">
              <input type="text"s>
            </div>
          </div>


          <div class="mt-3">
            <button class="btn btn-primary" type="submit"> Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import ApiService from "../services/api.service";

export default {
  props: ['surveyid', 'survey_title'],
  name : "SurveyPreview",
  data() {
    return {
      questions: [],
      
    }
  },
  mounted() {
    let url = '/preview-questions/' + this.surveyid
    ApiService.get(url)
        .then(
            res => {
              console.log(res.data)
              this.questions = res.data
            }
        )
  },
  methods: {
    submit_btn() {
      console.log("Printed")
    }
  }
}
</script>
