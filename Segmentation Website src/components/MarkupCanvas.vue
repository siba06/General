<template>
  <div class="edit-section">
    <!-- Tool panel -->
    <div id="tool-panel" style="padding-bottom: 10px;" class=".toolpanel">
      <div class="multi-button">
        <button @click="displayCropper" v-if="!showCropper" :disabled="unconfirmedChange" class="tooltip">
          <div class="tooltip"><i class="fa-solid fa-crop"></i></div><span class="tooltiptext"
            v-if="!approval">Crop</span>
        </button>
        <button @click="changeTool('point')" v-if="false && !showCropper && !approval"
          :class="{ 'selected-tool': (selectedTool === 'point') }" class="tooltip"><i class="fa-solid fa-plus"></i>
          <span class="tooltiptext">Point</span></button>

        <button @click="changeTool('pen')" v-if="!showCropper && !approval"
          :class="{ 'selected-tool': (selectedTool === 'pen') }" class="tooltip"><i class="fa-solid fa-pen"></i>
          <span class="tooltiptext">Pen</span></button>

        <button @click="changeTool('eraser')" v-if="!showCropper && !approval"
          :class="{ 'selected-tool': (selectedTool === 'eraser') }" class="tooltip"><i class="fa-solid fa-eraser"></i>
          <span class="tooltiptext">Eraser</span></button>

        <button @click="changeTool('undo')" v-if="(!showCropper) && (!approval)"
          :disabled="session_undo_markup.length === 0" class="tooltip"><i class="fa-solid fa-rotate-left"></i>
          <span class="tooltiptext">Undo</span></button>

        <button @click="showDeleteModal = true" v-if="!showCropper && !approval" :disabled="markupDeleted"
          class="tooltip"><i class="fa-solid fa-trash"></i>
          <span class="tooltiptext">Delete</span></button>


        <button @click="reloadCanvas()" v-if="!showCropper && !approval" title="Reload" class="tooltip"><i
            class="fa-solid fa-arrows-rotate"></i>
          <span class="tooltiptext">Reload</span></button>


        <button @click="showChangesModal = true" v-if="!showCropper && !approval" :disabled="!unconfirmedChange"
          title="Save Changes" class="tooltip"><i class="fa-solid fa-floppy-disk"></i>
          <span class="tooltiptext">Save</span></button>

        <button @click="showCancelModal = true" v-if="!showCropper && !approval" :disabled="!unconfirmedChange"
          title="Cancel Changes" class="tooltip"><i class="fa-solid fa-xmark"></i>
          <span class="tooltiptext">Cancel</span></button>



        <!-- Crop Buttons -->
        <button v-if="showCropper" @click="showCropModal = true"><i class="fa-solid fa-check"></i></button>
        <button v-if="showCropper" @click="cancelCrop"><i class="fa-solid fa-xmark"></i></button>

      </div>
    </div>


    <!-- Color and eraser size pickers -->

    <div class="color-panel" v-if="!showCropper && !approval">

      <ColourPicker @colorChange="(color) => currentColor = color" :currentChosenColour="currentColor"
        v-if="selectedTool" />

      <div class='eraserSlider' v-if="this.selectedTool === 'eraser'">
        <label for="eraserSizeSlider">
          <div class="eraserSizeContainer">
            <div class="eraserSliderIcon" :style="{ width: eraserSize + 'px', height: eraserSize + 'px' }">
              <i class="fa-solid fa-eraser" :style="{ fontSize: eraserSize * 0.8 + 'px' }"></i>
            </div>
          </div>
        </label>
        <input id="eraserSizeSlider" type="range" min="1" max="20" v-model="eraserSize" />
      </div>
    </div>
  </div>

  <!-- Confirmation Modals -->
  <div>
    <ConfirmModal v-if="showCropModal" @close="showCropModal = false" @confirm="cropImage" />
    <ConfirmModal v-if="showCancelModal" @close="showCancelModal = false" @confirm="plotPoints" />
    <ConfirmModal v-if="showChangesModal" @close="showChangesModal = false" @confirm="sendBack" />
    <ConfirmModal v-if="showDeleteModal" @close="showDeleteModal = false" @confirm="changeTool('delete')">
      <template v-slot:header>Delete All Markup</template>
      <template v-slot:body>Are you sure you want to delete current segmentations?
      </template>
    </ConfirmModal>
  </div>
  <div class="imagecanvas">
    <div class="canvas_container" id="canvasContainer" ref="canvasContainer">
      <div id="circle-cursor" class="circle-cursor"></div>

      <img :src="displayImage" alt="" ref="editImage" id="image2" />
      <canvas ref="mycanvas" @mousedown="startDrawing" @mousemove="draw" @mouseup="stopDrawing"
        @mouseleave="mouseOffCanvas" @mouseenter="mouseOnCanvas" class="canvas_class"
        :style="{ 'pointer-events': !this.showCropper ? 'auto' : 'none', left: leftOffset + 'px' }"></canvas>
      <div class="multi-button2">
        <button @click="visiblity_choice = 'none'" v-if="!showCropper"
          :class="{ 'selected-tool': (visiblity_choice === 'none') }">
          <i class="fa-regular fa-eye"></i>
        </button>

        <button @click="visiblity_choice = 'current'" v-if="!showCropper && !approval"
          :class="{ 'selected-tool': (visiblity_choice === 'current') }"><svg viewBox="0 0 20 20" width="20" height="20"
            fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect y="9" width="20" height="2" :fill="currentColor" />
          </svg>
        </button>

        <button @click="visiblity_choice = 'all'" v-if="!showCropper"
          :class="{ 'selected-tool': (visiblity_choice === 'all') }"><svg viewBox="0 0 20 20" width="20" height="20"
            fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect y="0" width="20" height="1" fill="#FF0000" />
            <rect y="4" width="20" height="2" fill="#00FF00" />
            <rect y="9" width="20" height="2" fill="#FF00FF" />
            <rect y="14" width="20" height="2" fill="#00FFFF" />
            <rect y="19" width="20" height="1" fill="#FFA500" />

          </svg></button>

      </div>
    </div>

  </div>



</template>


<script>
import ColourPicker from './ColourPicker.vue';
import ConfirmModal from './ConfirmModal.vue';
import Cropper from 'cropperjs';
export default {
  name: 'MarkupCanvas',
  props: ['img_url', 'slice_markup', 'approvalChoice'],
  components: {
    ConfirmModal,
    ColourPicker
  },
  emits: ['new-markup', 'unconfirmed-changes', 'img-cropped'], // declare the custom events
  data() {
    return {
      unconfirmedChange: false, // Is there an unconfirmed change?
      showCropModal: false, // Show the crop modal
      showChangesModal: false, // Show the changes modal
      showCancelModal: false,  // Show the cancel modal
      showDeleteModal: false, // Show the delete modal
      Cropper: null, // Cropper object
      showCropper: false, // Show the cropper
      drawing: false, // Is the user drawing?
      context: null, // Canvas context
      markupData: {}, // Markup data for each layer in pair format
      iScale: 1, // Image scale
      xScale: 1,
      yScale: 1,
      cScale: 1, // Cropped image width scale
      hScale: 1, // Cropped image Height scale
      session_markup: [], // Markup data for the current mouse drag
      pointMarkup: [], // Markup data for the current points drawn
      selectedTool: null, // Selected tool
      eraserSize: 5, // Eraser size
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
      currentColor: '#FF0000', // Current color
      leftOffset: 0, // Left offset for the canvas
      session_undo_markup: [], // Markup data for the current session
      session_undo: null, // Undo data for the current session
      visiblity_choice: 'all',
      circleCursor: null,
      canvasContainer: null,
    };
  },
  created() {
    this.displayImage = this.img_url.slice();

  },
  mounted() {
    this.context = this.$refs.mycanvas.getContext('2d', { willReadFrequently: true });
    this.circleCursor = document.getElementById('circle-cursor');
    this.canvasContainer = document.getElementById('canvasContainer');

    this.loadImage();

    // const resizeObserver = new ResizeObserver(() => {
    //   if (!this.showCropper) {


    //   }
    // });
    // // Get the image element using ref and observe it
    // const canvasElement = this.canvasContainer;
    // resizeObserver.observe(canvasElement);

  },
  methods: {
    fillStorePointsMarkup(currentColor = this.currentColor) {

      const currentLayer = Object.keys(this.colorLayerMap).find(key => this.colorLayerMap[key] === currentColor);

      const point_pairs = this.pointMarkup.slice().sort((a, b) => a.X - b.X);
      const interpolated_points = this.interpolateLine(point_pairs);


      const data_pairs = this.markupData[currentLayer].slice();

      const filteredPairs = data_pairs.filter(dataPair => !interpolated_points.some(sessionPair => sessionPair.X === dataPair.X));

      // Replace with new points
      const firstXIndex = filteredPairs.findIndex(dataPair => dataPair.X > point_pairs[0].X);
      filteredPairs.splice(firstXIndex, 0, ...interpolated_points);

      this.markupData[currentLayer] = filteredPairs;
      this.pointMarkup = [];
      this.redrawPlot();
    },
    testFun() {
      //this.loadImage();
    },
    handleImageResize() {
      this.cScale = 1;
      this.hScale = 1;

      //If cropper is on, cancel it
      if (this.Cropper) {
        this.cancelCrop();
      }
      const img = new Image();
      img.src = this.img_url;
      //New url needs to be updated
      this.displayImage = this.img_url.slice();


      img.onload = () => {
        //Calculate if the markup needs to be scaled
        this.xScale = img.width / this.getDimensions()[0]
        this.yScale = img.height / this.getDimensions()[1]
        img.height = this.getDimensions()[1];
        img.width = this.getDimensions()[0];
        this.$refs.mycanvas.width = img.width;
        this.$refs.mycanvas.height = img.height;

        this.leftOffset = this.$refs.editImage.offsetLeft;

        this.plotPoints();
        this.session_undo = this.context.getImageData(0, 0, this.$refs.mycanvas.width, this.$refs.mycanvas.height);
      };
    },
    mouseOffCanvas() {
      this.circleCursor.style.display = 'none';
      this.canvasContainer.style.cursor = 'auto';
      this.circleCursor.style.border = 'none';
    },
    mouseOnCanvas() {
      if (this.selectedTool) {
        this.canvasContainer.style.cursor = 'pointer';
        if (this.selectedTool === 'eraser') {
          this.circleCursor.style.display = 'block';
          this.circleCursor.style.border = '1px solid white';
          this.circleCursor.style.backgroundColor = 'transparent';

          this.circleCursor.style.width = this.context.lineWidth + 'px';
          this.circleCursor.style.height = this.context.lineWidth + 'px';
        } else if (this.selectedTool === 'point') {
          this.canvasContainer.style.cursor = 'crosshair';

        } else {
          this.circleCursor.style.display = 'block';
          this.circleCursor.style.backgroundColor = this.currentColor;
          this.circleCursor.style.opacity = 0.5;
          this.circleCursor.style.width = '5px';
          this.circleCursor.style.height = '5px';
        }
      }




    },
    changeTool(tool) {
      if (tool === 'delete') {
        this.$emit("unconfirmed-changes", true);
        this.unconfirmedChange = true;

        this.session_undo_markup = JSON.parse(JSON.stringify(this.markupData));
        this.session_undo = this.context.getImageData(0, 0, this.$refs.mycanvas.width, this.$refs.mycanvas.height);
        for (const layer in this.markupData) {
          this.markupData[layer] = [];
        }
        this.redrawPlot();
        this.showDeleteModal = false;
      } else if (tool === 'undo') {
        //Revert canvas to previous state
        this.context.putImageData(this.session_undo, 0, 0);

        //Revert markup data to previous state
        this.markupData = JSON.parse(JSON.stringify(this.session_undo_markup));

        //Clear undo data
        this.session_undo_markup = [];
        this.updateTool();
      }

      else if (this.selectedTool === tool) {
        this.selectedTool = null;
      } else {
        this.selectedTool = tool;
      }
    },
    async displayCropper() {
      this.unconfirmedChange = true;
      this.$emit("unconfirmed-changes", true);

      const imgRef = document.getElementById('image2');
      //Indicate cropper is on
      this.showCropper = true;

      //Create new cropper for the image
      this.Cropper = new Cropper(imgRef, {
        viewMode: 1,
        background: false,
        movable: false,
        scalable: false,
        rotatable: false,
        zoomable: false,
        autoCropArea: 1,
        minCropBoxHeight: this.$refs.editImage.height,
        ready() {
          this.leftOffset = this.cropper.getCropBoxData().left;
        },
      });



      // Now that the Cropper is ready, you can access its properties
    },

    cropImage() {
      this.showCropModal = false;

      //Get the left crop and width. Gives range of points to keep or remove
      const cropBoxData = this.Cropper.getCropBoxData();
      const cropperCanvas = this.Cropper.getCroppedCanvas();
      this.displayImage = cropperCanvas.toDataURL();
      //Get the left and right crop values
      let cropLeft = Math.round(cropBoxData.left);
      let cropRight = cropLeft + Math.round(cropBoxData.width);

      //Does it after everything renders
      setTimeout(() => {
        this.cScale = this.$refs.editImage.width / cropBoxData.width;
        this.hScale = this.$refs.editImage.height / cropBoxData.height;
        //Calculate image shift to align canvas and image
        for (const layer in this.markupData) {

          //Sort data pairs by X value
          const sorted_pairs = this.markupData[layer].slice().sort((a, b) => a.X - b.X);
          //Shift the X values to align with the cropped image
          const data_pairs = sorted_pairs.map(pair => ({ X: pair.X + this.leftOffset, Y: pair.Y }));

          // Find the largest point that is less than cropLeft
          const largestPointBeforeCropLeft = data_pairs.reduce((largest, dataPair) => {
            if (dataPair.X <= cropLeft && dataPair.X >= largest.X) {
              return dataPair;
            }
            return largest;
          }, data_pairs[0]);

          // Find the smallest point greater than cropRight
          const smallestPointAfterCropRight = data_pairs.reduce((smallest, dataPair) => {
            if (dataPair.X >= cropRight && dataPair.X <= smallest.X) {
              return dataPair;
            }
            return smallest;
          }, data_pairs[data_pairs.length - 1]);
          // Filter out all points that are outside the crop box
          const filteredDataPairs = data_pairs.filter(dataPair =>
            dataPair.X > cropLeft &&
            dataPair.X < cropRight);
          // Add the largest point before cropLeft and smallest point after cropRight if needed
          if (data_pairs.length > filteredDataPairs.length) {
            filteredDataPairs.unshift({
              X: (largestPointBeforeCropLeft.X > cropLeft) ? largestPointBeforeCropLeft.X : cropLeft,
              Y: largestPointBeforeCropLeft.Y
            });
            filteredDataPairs.push({
              X: (cropRight < smallestPointAfterCropRight.X) ? cropRight : smallestPointAfterCropRight.X,
              Y: smallestPointAfterCropRight.Y
            });
          }

          //Shift markup data back to 0
          this.markupData[layer] = filteredDataPairs.map(dataPair => ({
            X: ((dataPair.X - cropLeft) * this.cScale),
            Y: dataPair.Y * this.hScale
          }));

        }

        this.selectedTool = null;
        this.redrawPlot();

        this.$emit("img-cropped", [this.displayImage, this.convertMarkupForm()]);

        this.cancelCrop();

      }, 0);

    },
    redrawPlot(currentMarkup = this.markupData) {
      //Reset canvas
      this.context.lineWidth = 1;
      this.context.globalCompositeOperation = "source-over";
      this.context.clearRect(0, 0, this.$refs.mycanvas.width, this.$refs.mycanvas.height);
      //Redraw the plot
      for (const layer in currentMarkup) {

        //If the layer is not in visible list, skip it
        if (!this.visibleLayers.includes(this.colorLayerMap[layer])) {
          continue;
        }
        const data_pairs = currentMarkup[layer].slice()//.sort((a, b) => a.X - b.X);
        const drawColor = this.colorLayerMap[layer];
        const numPoints = data_pairs.length;
        this.context.beginPath();

        // Move to the starting point (first point in the array)
        if (numPoints > 0) {
          this.context.moveTo(data_pairs[0].X, data_pairs[0].Y);
        }

        // Loop through the points and draw lines between them
        for (let i = 0; i < numPoints - 1; i++) {
          const dist_X = Math.abs(data_pairs[i].X - data_pairs[i + 1].X);
          const dist_Y = Math.abs(data_pairs[i].Y - data_pairs[i + 1].Y);
          if (dist_X > 1 || dist_Y > 1) {
            this.context.moveTo(data_pairs[i + 1].X, data_pairs[i + 1].Y);
            continue;
          }
          this.context.lineTo(data_pairs[i + 1].X, data_pairs[i + 1].Y);
        }
        // Set the fill color and draw the lines
        this.context.fillStyle = drawColor;
        this.context.strokeStyle = drawColor;
        this.context.stroke();
      }
      this.updateTool();

    },
    cancelCrop() {
      //Indicate cropper is off
      this.showCropper = false;
      //Destroy the cropper
      this.Cropper.destroy();

      this.unconfirmedChange = false;
      this.$emit("unconfirmed-changes", false);


    },
    reloadCanvas(currentMarkup = this.markupData) {

      for (const layer in currentMarkup) {
        currentMarkup[layer] = this.interpolateLine(currentMarkup[layer].slice());

      }



      this.updateTool();

      const img = new Image();
      img.src = this.img_url;
      //New url needs to be updated
      this.displayImage = this.img_url.slice();


      img.onload = () => {
        //Calculate if the markup needs to be scaled
        this.xScale = img.width / this.getDimensions()[0]
        this.yScale = img.height / this.getDimensions()[1]
        img.height = this.getDimensions()[1];
        img.width = this.getDimensions()[0];
        this.$refs.mycanvas.width = img.width;
        this.$refs.mycanvas.height = img.height;

        this.leftOffset = this.$refs.editImage.offsetLeft;

        this.redrawPlot(currentMarkup);


        this.session_undo = this.context.getImageData(0, 0, this.$refs.mycanvas.width, this.$refs.mycanvas.height);
      };

    },


    interpolateLine(currentLine) {

      //Sort and round pairs
      const rounded_pairs = currentLine.map(pair => ({ X: Math.round(pair.X), Y: Math.round(pair.Y) }));

      const data_pairs = [... new Set(rounded_pairs.map(JSON.stringify))].map(JSON.parse);

      const numPoints = data_pairs.length;

      const filledData = [];
      if (numPoints > 0) {
        filledData.push({ 'X': data_pairs[0].X, 'Y': data_pairs[0].Y });
      }


      for (let i = 0; i < numPoints - 1; i++) {

        const interpolatedPoints = this.interpolatePoints(data_pairs[i], data_pairs[i + 1]);

        filledData.push(...interpolatedPoints);
        filledData.push(data_pairs[i + 1]);
      }

      return filledData;
    },
    interpolatePoints(pointA, pointB) {
      const dist_X = Math.abs(pointA.X - pointB.X);
      const dist_Y = Math.abs(pointA.Y - pointB.Y);
      const interpolatedPoints = [];
      if (dist_X > 1 || dist_Y > 1) {
        const dist = Math.max(dist_X, dist_Y);
        if (dist_X === dist) {

          const slope = (pointB.Y - pointA.Y) / (pointB.X - pointA.X);
          let step = 1;
          if (pointA.X > pointB.X) {
            step = -1;
          }


          for (let x = (pointA.X) + step; x != pointB.X; x += step) {

            // y = m(x - x1) + y1

            const interpolatedY = pointA.Y + slope * (x - pointA.X);
            interpolatedPoints.push({ 'X': x, 'Y': Math.round(interpolatedY) });
          }
        }
        else if (dist_Y === dist) {

          const slope = (pointB.X - pointA.X) / (pointB.Y - pointA.Y);
          let step = 1;
          if (pointA.Y > pointB.Y) {
            step = -1;
          }
          for (let y = (pointA.Y) + step; y != pointB.Y; y += step) {

            const interpolatedX = pointA.X + slope * (y - pointA.Y);
            interpolatedPoints.push({ 'X': Math.round(interpolatedX), 'Y': y });
          }
        }
      }


      return interpolatedPoints;
    },
    plotPoints() {
      this.session_undo_markup = []
      //Gets rid of cancel modal if on
      this.showCancelModal = false;
      //Indicate no unsaved changes
      this.$emit("unconfirmed-changes", false);
      this.unconfirmedChange = false;
      //Reset tool selection         
      this.selectedTool = null;

      //Reset canvas
      this.context.lineWidth = 1;
      this.context.globalCompositeOperation = "source-over";
      this.context.clearRect(0, 0, this.$refs.mycanvas.width, this.$refs.mycanvas.height);

      //Reset markup data
      const sliceMarkup = JSON.parse(JSON.stringify(this.slice_markup))

      for (const layer in this.colorLayerMap) {

        const currentLayer = sliceMarkup[layer];

        const x_vals = currentLayer['X'];
        const y_vals = currentLayer['Y'];

        const scaledX = x_vals.map(x => (x / this.xScale));
        const scaledY = y_vals.map(y => (y / this.yScale));

        this.markupData[layer] = scaledX.map((x, i) => ({ X: x, Y: scaledY[i] }));
        this.markupData[layer] = this.interpolateLine(this.markupData[layer].slice());

      }
      this.redrawPlot();

    },
    loadImage() {
      this.cScale = 1;
      this.hScale = 1;

      //If cropper is on, cancel it
      if (this.Cropper) {
        this.cancelCrop();
      }
      const img = new Image();
      img.src = this.img_url;
      //New url needs to be updated
      this.displayImage = this.img_url.slice();


      img.onload = () => {
        //Calculate if the markup needs to be scaled
        this.xScale = img.width / this.getDimensions()[0]
        this.yScale = img.height / this.getDimensions()[1]
        img.height = this.getDimensions()[1];
        img.width = this.getDimensions()[0];
        this.$refs.mycanvas.width = img.width;
        this.$refs.mycanvas.height = img.height;

        this.leftOffset = this.$refs.editImage.offsetLeft;

        this.plotPoints();
        this.session_undo = this.context.getImageData(0, 0, this.$refs.mycanvas.width, this.$refs.mycanvas.height);
      };
    },
    getDimensions() {
      return [this.$refs.editImage.width, this.$refs.editImage.height];
    },

    startDrawing(event) {
      if (this.selectedTool) {

        this.$emit("unconfirmed-changes", true);
        this.unconfirmedChange = true;

        this.session_undo = this.context.getImageData(0, 0, this.$refs.mycanvas.width, this.$refs.mycanvas.height);
        this.session_undo_markup = JSON.parse(JSON.stringify(this.markupData));

        const { offsetX, offsetY } = event;
        this.context.beginPath();
        this.context.moveTo(offsetX, offsetY);
        if (this.selectedTool === 'point') {
          this.context.fillStyle = this.currentColor;
          this.context.arc(offsetX, offsetY, 2, 0, 2 * Math.PI);
          this.context.fill();
          this.pointMarkup.push({ 'X': offsetX, 'Y': offsetY });
        } else {
          this.drawing = true;
          this.session_markup = [{ 'X': offsetX, 'Y': offsetY }];
        }
      }
    },
    draw(event) {
      if (this.selectedTool) {

        const mouseX = event.clientX - this.canvasContainer.getBoundingClientRect().left - (this.currentLineWidth);
        const mouseY = event.clientY - this.canvasContainer.getBoundingClientRect().top - (this.currentLineWidth);

        this.circleCursor.style.left = `${mouseX}px`;
        this.circleCursor.style.top = `${mouseY}px`;

      }


      if ((this.selectedTool) && this.drawing) {
        const { offsetX, offsetY } = event;
        this.context.strokeStyle = this.currentColor;
        this.context.lineTo(offsetX, offsetY);
        this.context.stroke();
        const newPoint = { 'X': offsetX, 'Y': offsetY };

        //Interpolate points to make sure they are not too far apart to detect gaps
        if (this.session_markup.length > 0) {
          const lastPoint = this.session_markup[this.session_markup.length - 1];
          const interpolatedPoints = this.interpolatePoints(lastPoint, newPoint);
          this.session_markup.push(...interpolatedPoints);
        }
        this.session_markup.push(newPoint);


      }
    },
    stopDrawing() {
      if (this.selectedTool) {
        this.drawing = false;
        const currentLayer = Object.keys(this.colorLayerMap).find(key => this.colorLayerMap[key] === this.currentColor);

        if (this.selectedTool === 'pen') {

          //Get rid of existing line at overlapping X
          this.session_markup = this.session_markup.sort((a, b) => a.X - b.X);
          const data_pairs = this.markupData[currentLayer].slice();

          const filteredPairs = data_pairs.filter(dataPair => !this.session_markup.some(sessionPair => sessionPair.X === dataPair.X));

          const firstXIndex = filteredPairs.findIndex(dataPair => dataPair.X > this.session_markup[0].X);

          // Insert the new points into the data pairs at the correct index
          filteredPairs.splice(firstXIndex, 0, ...this.session_markup);

          this.markupData[currentLayer] = filteredPairs;

        } else if (this.selectedTool === 'eraser') {
          const new_markup = this.session_markup.slice();
          setTimeout(() => {

            for (const current_layer in this.markupData) {

              if (!this.visibleLayers.includes(this.colorLayerMap[current_layer])) {
                continue;
              }
              const data_pairs = this.markupData[current_layer].slice();
              //const eraserWidth = this.eraserSize;
              const eraserWidth = this.eraserSize / 2;

              this.markupData[current_layer] = data_pairs.filter(dataPair => !new_markup.some(erased => (Math.abs(dataPair.X - erased.X) < eraserWidth) && (Math.abs(dataPair.Y - erased.Y) < eraserWidth)));


            }

          }, 0);
          //Logging eraser changes

        }

        this.session_markup = [];
      }
    },
    updateTool() {
      if (this.selectedTool === 'pen') {
        this.context.lineWidth = 1;
        this.context.globalCompositeOperation = "source-over";
        this.context.strokeStyle = this.currentColor;

      } else if (this.selectedTool === 'eraser') {
        this.context.globalCompositeOperation = "destination-out";
        this.context.strokeStyle = "rgba(255,255,255,1)";
        this.context.lineWidth = this.eraserSize; // Set eraser size

      } else if (this.selectedTool === 'point') {
        this.context.globalCompositeOperation = "source-over";
      }

      setTimeout(() => {
        this.leftOffset = this.$refs.editImage.offsetLeft;
      }, 0);
    },
    updateEraserSize() {
      this.context.lineWidth = this.eraserSize; // Set eraser size
    },
    sendBack() {
      this.showChangesModal = false;
      this.$emit("new-markup", this.convertMarkupForm());
      this.loadImage();

    },

    convertMarkupForm() {
      const editedMarkup = {};
      for (const layer in this.markupData) {
        const currentLayer = this.markupData[layer].slice()

        let filteredDataPairs = [...new Set(currentLayer.map(JSON.stringify))].map(JSON.parse).sort((a, b) => a.X - b.X);

        // If more than 1 point has the same X value, use rounded mean of Y values
        const endX = filteredDataPairs[filteredDataPairs.length - 1].X + 1;
        const startX = filteredDataPairs[0].X;

        for (let i = startX; i < endX; i++) {
          const currentPairs = filteredDataPairs.filter(pair => pair.X === i);
          if (currentPairs.length > 1) {
            const meanY = Math.round(currentPairs.reduce((acc, pair) => acc + pair.Y, 0) / currentPairs.length);
            filteredDataPairs = filteredDataPairs.filter(pair => pair.X !== i);
            filteredDataPairs.push({ X: i, Y: meanY });
          }
        }

        const uniquePairs = filteredDataPairs.sort((a, b) => a.X - b.X);
        const rescaledPairs = uniquePairs.map(pair => ({ X: Math.round((pair.X * this.xScale) / this.cScale), Y: Math.round((pair.Y * this.yScale) / this.hScale) }));


        const x_vals = rescaledPairs.map(item => item.X);
        const y_vals = rescaledPairs.map(item => item.Y);
        editedMarkup[layer] = { 'X': x_vals, 'Y': y_vals };
      }
      return editedMarkup;
    },
  },
  computed: {

    currentLineWidth() {
      if (this.selectedTool === 'eraser') {
        return this.eraserSize / 2;
      } else {
        return 2.5;
      }
    },
    approval() {
      if (this.approvalChoice === false) {
        return false;
      } else {
        return true;
      }

    },
    cropButtonLabel() {
      if (this.unconfirmedChange) {
        return 'Please confirm/cancel changes before cropping';
      } else {
        return null;
      }
    },
    markupDeleted() {
      for (const layer in this.markupData) {
        if (this.markupData[layer].length === 0) {
          continue;
        }
        return false;
      }
      return true;
    },
    visibleLayers() {
      if (this.visiblity_choice === 'none') {
        return [];
      } else if (this.visiblity_choice === 'current') {
        return [this.currentColor];

      } else {
        return ['#FF0000', '#00FF00', '#FFFF00', '#FF00FF', '#00FFFF', '#FFA500', '#A52A2A', '#008000', '#800080'];
      }
    },
  },
  watch: {
    img_url: 'loadImage',
    eraserSize: 'updateEraserSize',
    selectedTool: 'updateTool',
    visibleLayers() {
      this.redrawPlot();
    },
    currentColor(newCol, oldCol) {
      if (this.selectedTool === 'point') {
        if (this.pointMarkup.length > 0) {
          this.fillStorePointsMarkup(oldCol);
        }
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.edit-section {
  height: 100%;
}

.circle-cursor {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: rgb(191, 41, 41);
  position: absolute;
  pointer-events: none;
  display: none;

}

.eraserSlider {
  display: flex;
  margin: auto;
  height: 50px;
  gap: 20px;
  align-items: center;

  .eraserSizeContainer {
    width: 30px;
    height: 30px;
    justify-content: center;
    align-items: center;
    display: flex;
    position: relative;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    border-radius: 10px;

  }

  .eraserSliderIcon {
    position: relative;
    border-radius: 50%;
    border: 1px solid #9ecfe7;
    color: #9ecfe7;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #9ecfe7;


  }

  .size-slider-icon {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 1px solid #9ecfe7;
  }

  input[type="range"] {
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    width: 550px;
    background-color: transparent;

    &:focus {
      outline-color: #95caf8;
    }
  }

  input[type="range"]::-webkit-slider-runnable-track {
    -webkit-appearance: none;
    appearance: none;
    height: 3px;
    background: rgb(114, 246, 246);
    background: -webkit-linear-gradient(left,
        #a3b7ca 0%,
        #7593af 50%,
        #476f95 100%);
    background: linear-gradient(to right,
        #a3b7ca 0%,
        #7593af 50%,
        #476f95 100%);
    filter: progid:DXImageTransform.Microsoft.gradient(startColorstr="#f67280",
        endColorstr="#355c7d",
        GradientType=1);
  }

  input[type="range"]::-moz-range-track {
    -moz-appearance: none;
    appearance: none;
    height: 3px;
    background: rgb(246, 114, 128);
    background: -moz-linear-gradient(left,
        #a3b7ca 0%,
        #7593af 50%,
        #476f95 100%);
    background: linear-gradient(to right,
        #a3b7ca 0%,
        #7593af 50%,
        #476f95 100%);
    filter: progid:DXImageTransform.Microsoft.gradient(startColorstr="#f67280",
        endColorstr="#355c7d",
        GradientType=1);
  }

  input[type="range"]::-ms-track {
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    height: 3px;
    background: rgb(246, 114, 128);
    background: -moz-linear-gradient(left,
        #a3b7ca 0%,
        #7593af 50%,
        #476f95 100%);
    background: -webkit-linear-gradient(left,
        #a3b7ca 0%,
        #7593af 50%,
        #476f95 100%);
    background: linear-gradient(to right,
        #a3b7ca 0%,
        #7593af 50%,
        #476f95 100%);
    filter: progid:DXImageTransform.Microsoft.gradient(startColorstr="#f67280",
        endColorstr="#355c7d",
        GradientType=1);
  }

  input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    border: 2px solid rgba(209, 219, 228, 0.353);
    border-radius: 50%;
    height: 20px;
    width: 20px;
    position: relative;
    bottom: 8px;
    background: #406c99;
    background-size: 50%;
    box-shadow: 0px 3px 5px 0px rgba(0, 0, 0, 0.4);
    cursor: grab;

    &:active {
      cursor: grabbing;
    }
  }


  input[type="range"]::-moz-range-thumb {
    -moz-appearance: none;
    appearance: none;
    border: 2px solid #f8b195;
    border-radius: 50%;
    height: 20px;
    width: 20px;
    position: relative;
    bottom: 8px;
    background: #222 url("http://codemenatalie.com/wp-content/uploads/2019/09/slider-thumb.png") center no-repeat;
    background-size: 50%;
    box-shadow: 0px 3px 5px 0px rgba(0, 0, 0, 0.4);
    cursor: grab;

    &:active {
      cursor: grabbing;
    }
  }

  input[type="range"]::-ms-thumb {
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    border: 2px solid #f8b195;
    border-radius: 50%;
    height: 20px;
    width: 20px;
    position: relative;
    bottom: 8px;
    background: #222 url("http://codemenatalie.com/wp-content/uploads/2019/09/slider-thumb.png") center no-repeat;
    background-size: 50%;
    box-shadow: 0px 3px 5px 0px rgba(0, 0, 0, 0.4);
    cursor: grab;

    &:active {
      cursor: grabbing;
    }
  }


}


.toolpanel {
  display: flex;
  justify-content: space-between;
  padding: 10px;
}

.layer-view-toggle {
  display: flex;
  align-items: center;
  column-gap: 5px;
}

div.multi-button {
  background: #fafafa;
  border: 1px solid #eaeaea;
  padding: 5px;
  border-radius: 10%;
  width: fit-content;
  justify-content: space-between;
  column-gap: 8px;
  display: flex;
  margin-left: auto;
  margin-right: auto;
  scale: 1.2;
}

div.multi-button button {
  background: #fafafa;
  border: none;
  padding: 5px;
  cursor: pointer;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  width: 30px;
  height: 30px;
}

div.multi-button button:hover {
  background: #f0f0f0;
}

div.multi-button2 {
  position: absolute;
  background: #fafafa;
  border: 1px solid #eaeaea;
  padding: 2px;
  border-radius: 10%;
  width: fit-content;
  justify-content: space-between;
  column-gap: 3px;
  display: flex;
  z-index: 100;
  left: 0;
  top: 0;
  opacity: 0.5;
}

div.multi-button2 button {
  background: #fafafa;
  border: none;
  padding: 2px;
  cursor: pointer;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  width: 25px;
  height: 25px;
  display: flex;
  justify-content: center;
  align-items: center;

}

div.multi-button2 button:hover {
  background: #f0f0f0;
  opacity: 1;
}

.color-panel {
  position: relative;
  display: flex;
  justify-content: space-between;
  padding: 10px;
}

.color-button {
  border: none;
  padding: 10px;
  cursor: pointer;
}

.color-button:hover::before {
  content: attr(title);
  position: absolute;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border-radius: 5px;
  padding: 5px;
  top: -30px;
  /* Adjust the position as needed */
  left: 50%;
  transform: translateX(-50%);
  white-space: nowrap;
  display: none;
}

.color-button:hover::before {
  display: block;
}



.canvas_class {
  position: absolute;
  top: 0;
  z-index: 10;
}

.imgcanvas {

  display: flex;
  justify-content: center;
  align-items: center;

}

.canvas_container {
  position: relative;
  width: 90%;
  margin: auto;


}

img {
  max-width: 100%;
}

.selected-tool {
  opacity: 0.2;
}

.tooltip .tooltiptext {
  font-size: 10px;
  visibility: hidden;
  width: 100%;
  color: #5f5f5f;

  /* Position the tooltip */
  position: absolute;
  z-index: 1;
  top: 100%;
  left: 0;
  border-color: #5f5f5f;
  border-style: solid;
  border-width: 1px;

}

.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>
