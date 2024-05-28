<template>
  <Transition name="modal">
    <div v-if="show" class="modal-mask">
      <div class="modal-container">
        <div class="modal-header">
          <slot name="header">Select Sample Size</slot>
        </div>

        <div class="modal-body">
          <slot name="body">
            <div class="input-border">
              <div class="tooltip">&#x1F6C8;
                <span class="tooltiptext">Choose percentage of volume to sample. Complete volumes contain approximately
                  100-200 slices. Ideally 20-40%</span>
              </div>
              <label for="percentageSlider">Sample Proportion</label>
              <div><input type="range" id="percentageSlider" v-model="selectedPercentage" min="10" :max="userMax" />
                <input type="number" ref="percentageInput" v-model="selectedPercentage" @input="handleInputChange"
                  min='10' :max='userMax' :style="{ width: '40px' }" />%
              </div>

            </div>
            <div class="input-border">
              <div class="tooltip">&#x1F6C8;
                <span class="tooltiptext">Optional. Applied if sample percentage too small or too large. Full volume
                  will be displayed if minimum greater than volume size.</span>
              </div>
              <div><label for="minimumSlices">Minimum number of slices</label>

                <input type="number" ref="minimumSlices" v-model="minSlices" min="2" placeholder="No minimum">
              </div>
              <div><label for="maximumSlices">Maximum number of slices</label>

                <input type="number" ref="maximumSlices" v-model="maxSlices" :min="maxSlicesMinimum"
                  placeholder="No maximum">
              </div>
            </div>
          </slot>
        </div>

        <div class="modal-footer">
          <slot name="footer">
            <button class="modal-default-button" @click="confirmClicked">Confirm</button>
            <button class="modal-default-button" @click="$emit('close')">Cancel</button>
          </slot>
        </div>
      </div>
    </div>
  </Transition>
</template>


<script>
import { auth } from '@/firebase/init';

export default {
  props: {
    show: Boolean
  },
  data() {
    return {
      selectedPercentage: 30,
      minSlices: null,
      maxSlices: null,
    }
  },
  methods: {
    confirmClicked() {
      const validPercent = this.$refs.percentageInput.checkValidity();
      const validMin = this.$refs.minimumSlices.checkValidity();
      const validMax = this.$refs.maximumSlices.checkValidity();

      if (validPercent && validMin && validMax) {
        this.$emit('size-selection', { 'percent': this.selectedPercentage, 'min': this.minSlices, 'max': this.maxSlices })
      } else {
        const invalidParams = [];
        if (!validPercent) {
          invalidParams.push('percentageInput');
        }
        if (!validMin) {
          invalidParams.push('minimumSlices');
        }
        if (!validMax) {
          invalidParams.push('maximumSlices');
        }
        this.shakeInputs(invalidParams)
      }
    },
    shakeInputs(invalidInputs) {
      // Add a shake class to trigger the animation
      invalidInputs.forEach((refName) => {
        const inputRef = this.$refs[refName];
        if (inputRef) {
          inputRef.classList.add('shake');
          // Remove the shake class after the animation duration (1s)
          setTimeout(() => {
            inputRef.classList.remove('shake');
          }, 1000);
        }
      });
    },
  },
  computed: {
    maxSlicesMinimum() {
      if (this.minSlices) {
        return this.minSlices;
      } else {
        return 1;
      }
    },
    userMax() {
      if (auth.currentUser.displayName === 'admin') {
        return 100;
      } else {
        return 50;
      }
    }
  }
}
</script>



<style scoped>
.input-border {
  padding: 5px;
  margin-bottom: 5px;
  border: 1px solid #000000;
  border-radius: 5px;
  position: relative;
}

.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  transition: opacity 0.3s ease;
}

.modal-container {
  width: 300px;
  margin: auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
}

.modal-header h3 {
  margin-top: 0;
  color: #42b983;
}

.modal-body {
  margin: 20px 0;
}

.modal-default-button {
  float: right;
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter-from {
  opacity: 0;
}

.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}

input:invalid {
  background-color: #ffdddd;

}

.shake {
  animation: shake 0.5s;
}

@keyframes shake {
  0% {
    transform: translateX(0);
  }

  25% {
    transform: translateX(-2px);
  }

  50% {
    transform: translateX(2px);
  }

  75% {
    transform: translateX(-2px);
  }

  100% {
    transform: translateX(0);
  }
}


.tooltip {
  position: absolute;
  display: inline-block;
  top: 0px;
  right: 0px;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 200px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 0;

  /* Position the tooltip */
  position: absolute;
  z-index: 1;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>