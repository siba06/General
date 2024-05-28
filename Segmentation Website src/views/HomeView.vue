<template>
  <div><router-link to="/pending">pending</router-link></div>
  <div><router-link to="/completed">completed</router-link></div>
<div><router-view/></div>
</template>


<script>


export default {
    name: "HomeView",
    components:{
    },
    data(){
        return{
        }
      },
    }
</script>

