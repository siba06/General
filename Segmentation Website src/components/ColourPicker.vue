<template>
  <div style="margin: 0 auto;">
    <nav class="slidemenu">
      <input v-for="(color, layer, index) in colorLayerMap" :key="index" type="radio" :name="index + '_item'"
        :id="'slide-item-' + index" class="slide-toggle" :value="color" v-model="chosenColor"
        :ref="color + '-slide-item'" />

      <label v-for="(color, layer, index) in colorLayerMap" :key="index" :for="'slide-item-' + index"
        :id="color + '-label'" :ref="color + '-label-ref'" :style="{ opacity: (color == chosenColor) ? '1' : '0.2' }">
        <p class="icon" :style="{ 'background-color': color }"></p>
        <span :style="{ 'max-height': layersOn ? '10px' : '0px', 'opacity': layersOn ? '1' : '0' }">{{ layer }}</span>
      </label>
      <div class="tooltip" @click="layersOn = !layersOn" style="cursor: pointer;">
        <p :style="{ 'opacity': layersOn ? '1' : '0.4' }">&#x1F6C8;</p>
      </div>
      <div class="clear"></div>

      <!-- Bar -->
      <div class="slider">
        <div class="bar">
        </div>
      </div>
    </nav>
  </div>
</template>
<script>

export default {
  name: 'ColourPicker',
  props: ['currentChosenColour'],
  data() {
    return {
      chosenColor: '',
      layersOn: false,
      colorLayerMap: { // Map of colours for each layer
        'Inner Limiting Membrane': '#FF0000',
        'RNFL - GCL interface': '#00FF00',
        'IPL - INL interface': '#FFFF00',
        'INL - OPL interface': '#FF00FF',
        'OPL - ONL interface': '#00FFFF',
        'External Limiting Membrane': '#FFA500',
        'Inner boundary of EZ': '#A52A2A',
        'Inner boundary of RPE/IZ complex': '#008000',
        "Bruch's Membrane": '#800080',
      },
    }
  },
  created() {

  },
  mounted() {
    this.chosenColor = this.currentChosenColour.slice();
  },
  watch: {
    chosenColor() {
      this.$emit('colorChange', this.chosenColor);
    }
  },

}
</script>
<style scoped>
* {
  margin: 0;
  padding: 0;
}

.clear {
  clear: both;
}


.slide-toggle {
  display: none;
}

.slidemenu {
  position: relative;
  font-family: arial, sans-serif;
  width: 88%;
  margin: 0px auto;
  overflow: hidden;
}

.slidemenu label {
  width: 11.1%;
  text-align: center;
  display: block;
  float: left;
  color: #333;
  opacity: 0.2;

}

.slidemenu label:hover {
  cursor: pointer;
  color: #666;
}

.slidemenu label span {
  display: block;
  padding: 10px;
  font-size: 8px;
  overflow: hidden;
}

.slidemenu label .icon {
  font-size: 20px;
  border: solid 2px #333;
  text-align: center;
  height: 30px;
  width: 30px;
  display: block;
  margin: 0 auto;
  line-height: 50px;
  border-radius: 50%;
}

/*Bar Style*/

.slider {
  width: 100%;
  height: 5px;
  display: block;
  background: #ccc;
  margin-top: 0px;
  border-radius: 5px;
}

.slider .bar {
  width: 11.1%;
  height: 5px;
  background: #333;
  border-radius: 5px;
}

/*Animations*/
.slidemenu label,
.slider .bar {
  transition: all 500ms ease-in-out;
  -webkit-transition: all 500ms ease-in-out;
  -moz-transition: all 500ms ease-in-out;
}

/*Toggle*/


.slidemenu #slide-item-0:checked~.slider .bar {
  margin-left: 0;
}

.slidemenu #slide-item-1:checked~.slider .bar {
  margin-left: 11.1%;
}

.slidemenu #slide-item-2:checked~.slider .bar {
  margin-left: 22.2%;
}

.slidemenu #slide-item-3:checked~.slider .bar {
  margin-left: 33.3%;
}

.slidemenu #slide-item-4:checked~.slider .bar {
  margin-left: 44.4%;
}

.slidemenu #slide-item-5:checked~.slider .bar {
  margin-left: 55.5%;
}

.slidemenu #slide-item-6:checked~.slider .bar {
  margin-left: 66.6%;
}

.slidemenu #slide-item-7:checked~.slider .bar {
  margin-left: 77.7%;
}

.slidemenu #slide-item-8:checked~.slider .bar {
  margin-left: 88.8%;
}






.tooltip {
  position: absolute;
  top: 0px;
  right: 0px;
}
</style>