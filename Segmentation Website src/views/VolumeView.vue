<template>
  <i class="fa-regular fa-circle-question questionicon" @click="helpModal = true"></i>
  <AboutInfo v-if="helpModal" @close="helpModal = false" />
  <div>
    <!-- Loading element for data upload to db -->
    <ConfirmModal v-if="!uploaded_data">
      <template v-slot:header>
        <div></div>
      </template>
      <template v-slot:body>
        <div><img src='@/assets/spinner.gif' style="width: 60px; height: 60px;"></div>
      </template>
      <template v-slot:footer>
        <div></div>
      </template>
    </ConfirmModal>
  </div>


  <div>
    <div v-if="!current_url && !loading_images" class="loading-spinner">
      <div class="spinner"></div>
      Loading...
    </div>
    <!-- IMAGE AND CANVAS COMPONENT -->
    <div>
      <MarkupCanvas ref="editor" :img_url="current_url"
        :approvalChoice="(volumeApproval[currentIndex] === 'Approved' || volumeApproval[currentIndex] === '')"
        :slice_markup="current_markup" v-if="current_url" @new-markup="updateMarkup"
        @unconfirmed-changes="(x) => locked_changes = x" @img-cropped="imageCropped" />
      <div class="progress-container">
        <div class="Loading" :style="{ '--percentage': ((volumeCompleted / dataLen) * 100) }"></div>
      </div>
    </div>

    <!-- Approve/reject switch -->


    <div class="choice-switch">
      <div
        v-if="(missedSlices != -1) && (missedSlices != currentIndex) && !(alteredSlices.includes(currentIndex) || locked_changes)">
        <button @click="goToMissedSlice">Go to missed slice</button>
      </div>
      <div>
        <!-- Confirm button to return outcome -->
        <button @click="calculateApproval" v-if="volumeCompleted === dataLen && (!locked_changes)"
          class="submit_button">Submit</button>
      </div>

      <div class="approval-buttons" ref="approval_toggle"
        :style="{ pointerEvents: (alteredSlices.includes(currentIndex)) ? 'none' : 'auto' }"
        v-if="!alteredSlices.includes(currentIndex)">

        <button @click="approvalToggle = true" :disabled="alteredSlices.includes(currentIndex) || locked_changes"
          :class="{ 'selected-button': approvalToggle, 'approved': true }" style="--color : #6daa5f;"
          ref="approve-button" title="Approve">
          <i class="fa-solid fa-check"></i></button>

        <button @click="approvalToggle = false" :disabled="alteredSlices.includes(currentIndex) || locked_changes"
          :class="{ 'selected-button': (approvalToggle === false), 'rejected': true }" style="--color:#ff7e5b;"
          title="Reject">
          <i class="fa-solid fa-times"></i></button>
      </div>

      <div v-if="alteredSlices.includes(currentIndex)" style="margin-inline: 30px ">
        <p>{{ volumeApproval[currentIndex] }}</p>
      </div>

      <div class="arrow-div">
        <div class="arrow left_arrow" @click="currentIndex -= 1"
          :class="(currentIndex === 0 || locked_changes) ? 'lock-arrow' : ''" :title="arrowLabel"></div>
        <div class="arrow right_arrow" @click="currentIndex += 1"
          :class="(currentIndex === dataLen - 1 || locked_changes) ? 'lock-arrow' : ''" :title="arrowLabel"></div>
      </div>
    </div>

  </div>

  <div>

    <SubmissionModal v-if="showFinishModal" @close="showFinishModal = false" @submit="submissionConfirmed"
      :approvedPercentage="approvedPercentage" :rejectedPercentage="rejectedPercentage"
      :editedPercentage="editedPercentage" :result=vol_approval_status />

  </div>
</template>

<script>
import MarkupCanvas from "@/components/MarkupCanvas.vue";
import { storage, db, auth } from '../firebase/init.js'
import { ref, listAll, getDownloadURL, uploadString, deleteObject } from "firebase/storage";
import { addDoc, collection, doc, updateDoc, getDoc, deleteDoc, query, where, getDocs } from "firebase/firestore"
import ConfirmModal from "@/components/ConfirmModal.vue";
import AboutInfo from "@/components/AboutInfo.vue";
import SubmissionModal from "@/components/SubmissionModal.vue";
// import { auth } from '../firebase/init.js';
// import { signOut } from "@firebase/auth";

export default {
  name: 'VolumeView',
  components: {
    MarkupCanvas,
    ConfirmModal,
    AboutInfo,
    SubmissionModal,
  },
  data() {
    return {
      options: ['Approved', 'Rejected', 'Approved with edits'], //possible outputs for approval status
      uploaded_data: true, //for tracking data being uploaded to db
      croppedList: [], //list of slices that have been cropped by index

      vol_approval_status: null, //approval status of volume
      additionalNotes: null, //additional notes for volume after submitting
      reviewOutcome: null, //outcome of volume review calculated from approval percentage
      showFinishModal: false,

      locked_changes: false, //for tracking if changes have been made to markup

      //volume parameters
      doc_id: this.$route.params.id,
      vol_id: this.$route.params.vol,
      patient_id: this.$route.params.patient,
      samplePercent: Number(this.$route.query.samplesize[0]),
      sampleMin: this.$route.query.samplesize[1],
      sampleMax: this.$route.query.samplesize[2],


      alteredSlices: [], //list of slices that have been altered by index
      vol_data: {}, //object containing all slice data (urls, segmentations, slice number)
      dataLen: null, //number of slices in volume
      currentIndex: 0, //current slice index

      volumeApproval: {}, //object containing approval status of each slice
      loading_images: true, //for tracking if images are still loading
      num_of_slices: null, //number of slices in volume
      approvalToggle: null, //for tracking if approval toggle is on or off

      approvedPercentage: null, //percentage of volume approved
      rejectedPercentage: null, //percentage of volume rejected
      editedPercentage: null, //percentage of volume edited



      alt_percentage: null, //percentage of volume altered

      helpModal: false, //for tracking if help modal is open

      vol_remainder: null, //number of slices left in volume 


    }
  },
  methods: {
    goToMissedSlice() {
      for (const slice in this.volumeApproval) {
        if (this.volumeApproval[slice] === '') {
          this.currentIndex = parseInt(slice);
          break;
        }
      }
    },
    submissionConfirmed(choice, data) {
      this.vol_approval_status = choice;
      this.additionalNotes = data;
      this.returnApprovals();
      this.showFinishModal = false;
    },

    async returnToDB(seg_data, new_images) {

      this.uploaded_data = false;
      //Reference to collection of volumes completed in firestore
      const colRef = collection(db, 'CompletedVolumes');

      // Check if patient id and vol id already exist
      const q_exist = query(colRef, where('patient_id', '==', this.patient_id), where('vol_id', '==', this.vol_id));
      await getDocs(q_exist).then((snapshot) => {
        if (snapshot.size > 0) {

          //Get current data and update sampled size
          const curr_data = snapshot.docs[0].data();
          const new_sample_size = (curr_data.sample_size + this.dataLen)

          const slice_proportion = this.dataLen / new_sample_size;

          this.approvedPercentage = Math.round((slice_proportion * this.approvedPercentage) + (curr_data.approved_percentage * (1 - slice_proportion)));
          this.rejectedPercentage = Math.round((slice_proportion * this.rejectedPercentage) + (curr_data.rejected_percentage * (1 - slice_proportion)));
          this.editedPercentage = Math.round((slice_proportion * this.editedPercentage) + (curr_data.edited_percentage * (1 - slice_proportion)));

          this.dataLen = new_sample_size;
          this.additionalNotes = this.additionalNotes + '####' + curr_data.date + curr_data.notes;
          this.num_of_slices = curr_data.num_slices;
          // Verify new approval status
          if (this.approvedPercentage >= 70) {
            this.vol_approval_status = 'Approved';
          }
          else if (this.approvedPercentage + this.editedPercentage >= 70) {
            this.vol_approval_status = 'Approved with edits';
          } else {
            this.vol_approval_status = 'Rejected';
          }

          //Update existing doc in Completed
          const docRef = doc(db, 'CompletedVolumes', snapshot.docs[0].id);
          updateDoc(docRef, {
            'approval': this.vol_approval_status,
            'notes': this.additionalNotes,
            'approved_percentage': this.approvedPercentage,
            'rejected_percentage': this.rejectedPercentage,
            'edited_percentage': this.editedPercentage,
            'sample_size': this.dataLen,
            'date': new Date().toLocaleDateString(),
          });
          const storageRef = ref(storage, 'Completed/' + auth.currentUser.uid + '/' + this.patient_id + '_' + this.vol_id + '_' + (this.dataLen) + '.json');
          uploadString(storageRef, seg_data);

        } else {
          const docData = {
            'patient_id': this.patient_id,
            'vol_id': this.vol_id,
            'approval': this.vol_approval_status,
            'notes': this.additionalNotes,
            'approved_percentage': this.approvedPercentage,
            'rejected_percentage': this.rejectedPercentage,
            'edited_percentage': this.editedPercentage,
            'user_id': auth.currentUser.displayName,
            'sample_size': this.dataLen,
            'num_slices': this.num_of_slices,
            'date': new Date().toLocaleDateString(),
          };
          const docRef = addDoc(colRef, docData);
          const newDocId = docRef.id;

          //Upload cropped images as data url
          for (const new_img in new_images) {
            const storageRef = ref(storage, 'Completed/' + newDocId + '/' + new_img);
            uploadString(storageRef, new_images[new_img], 'data_url');
          }
          //Upload results and new segmentations
          const storageRef = ref(storage, 'Completed/' + auth.currentUser.uid + '/' + this.patient_id + '_' + this.vol_id + '_' + (this.dataLen) + '.json');
          uploadString(storageRef, seg_data);
        }
      });



      //Delete volume data from pending cloud storage
      const pendingRef = ref(storage, 'PendingApproval/' + this.doc_id + '/' + this.vol_id);

      for (const slice in this.vol_data) {
        const slice_no = this.vol_data[slice]['slice_no'];
        const sliceRef = ref(pendingRef, 'Slice_' + slice_no + '.png');
        await deleteObject(sliceRef);
      }

      //Update volume from patient document in pending firestore collection
      const docFirestoreRef = doc(db, 'Pending', this.doc_id);
      const vol_field = 'volume_' + this.vol_id;
      await updateDoc(docFirestoreRef, {
        [vol_field]: [this.vol_approval_status, (this.dataLen / this.num_of_slices) * 100],
      });

      //Check if all volumes for patient have been completed
      //if so, move patient to completed collection
      await getDoc(docFirestoreRef).then((doc) => {
        if (!doc.exists()) {
          console.log('Does not exist');
        } else {
          const patient_data = doc.data();
          if (!(Object.values(patient_data).includes('pending'))) {
            addDoc(collection(db, 'CompletedPatients'), patient_data);
            deleteDoc(docFirestoreRef);
          }


        }
      });
      this.uploaded_data = true;
      this.$router.push('/pending');
    },
    imageCropped(newImage) {
      this.current_slice.url = newImage[0];
      this.current_slice.segmentation = newImage[1];
      if (!this.croppedList.includes(this.currentIndex)) {
        this.croppedList.push(this.currentIndex);
      }
    },
    changesMade(unconfirmed) {
      this.lockedChanges = unconfirmed;

    },
    async getSampleDocument() {
      const allDocNames = []

      const doc_ref = ref(storage, 'PendingApproval/' + this.doc_id + '/' + this.vol_id);
      listAll(doc_ref).then((res) => {
        res.items.forEach((itemRef) => {
          if (itemRef.name.endsWith('.png')) {
            allDocNames.push(parseInt(itemRef.name.split('_')[1].split('.')[0]));
          }
        });
        this.num_of_slices = (allDocNames.length);
        const step_size = this.calculateStepSize(this.num_of_slices);
        this.getListOfSampleBlobs(this.num_of_slices, step_size, allDocNames.sort());

      })


    },
    calculateStepSize(numOfSlices) {
      const sMin = this.sampleMin;
      const sMax = this.sampleMax;
      const percentSample = Math.floor(numOfSlices * (this.samplePercent / 100));


      let stepSize;

      if (sMin !== 'null' && percentSample < parseInt(sMin)) {
        stepSize = Math.floor(numOfSlices / parseInt(sMin));
      } else if (sMax !== 'null' && percentSample > parseInt(sMax)) {
        stepSize = Math.ceil(numOfSlices / parseInt(sMax));
      } else {
        stepSize = Math.round(numOfSlices / percentSample);
      }

      return stepSize;

    },
    async getListOfSampleBlobs(numOfSlices, stepSize, allDocNames) {
      const seg_ref = ref(storage, 'PendingApproval/' + this.doc_id + '/' + this.vol_id + '/segmentation.json');

      // Get list of slices and segmentations
      getDownloadURL(seg_ref).then((url) => {
        fetch(url).then((response) => response.json()).then((data) => {
          let counter = 0
          for (let i = 0; i < numOfSlices; i += stepSize) {
            const step_i = allDocNames[i];

            getDownloadURL(ref(storage, 'PendingApproval/' + this.doc_id + '/' + this.vol_id + '/' + `Slice_${step_i}.png`)).then((url) => {
              this.vol_data[counter] = { 'url': url, 'segmentation': data[step_i], 'slice_no': step_i };
              counter += 1;
              this.dataLen = counter;
            })
          }
        })
      })

    },
    updateMarkup(newData) {
      this.current_slice.segmentation = newData;
      if (!this.alteredSlices.includes(this.currentIndex)) {
        this.alteredSlices.push(this.currentIndex);
        this.volumeApproval[this.currentIndex] = 'Edited';
        this.approvalToggle = null;
      }
    },
    returnApprovals() {
      //Need seg as json
      //approval stored as approve or reject or new seg
      //Store segmentations that have been altered
      const updated_data = {};
      const new_images = {};
      for (const cur in this.vol_data) {

        const cur_slice = parseInt(cur);
        const current_slice_num = this.vol_data[cur_slice].slice_no;
        if (this.alteredSlices.includes(cur_slice) || this.croppedList.includes(cur_slice)) {

          updated_data[current_slice_num] = { 'result': this.volumeApproval[cur_slice], 'segmentation': JSON.parse(JSON.stringify(this.vol_data[cur_slice].segmentation)) };
          if (this.croppedList.includes(cur_slice)) {
            new_images[current_slice_num] = this.vol_data[cur_slice].url;
          }
        } else {
          updated_data[current_slice_num] = this.volumeApproval[cur_slice];
        }
      }
      this.returnToDB(JSON.stringify(updated_data), new_images);

      this.showFinishModal = false;


    },
    calculateApproval() {
      //Get number of rejected, edited and approved slices
      const totalApprovals = Object.values(this.volumeApproval).filter(approval => approval === 'Approved').length;
      const totalRejections = Object.values(this.volumeApproval).filter(approval => approval === 'Rejected').length;
      const totalEdits = Object.values(this.volumeApproval).filter(approval => approval === 'Edited').length;

      const percentage = ((totalApprovals + totalEdits) / this.dataLen) * 100;

      this.approvedPercentage = Math.round((totalApprovals / this.dataLen) * 100);
      this.rejectedPercentage = Math.round((totalRejections / this.dataLen) * 100);
      this.editedPercentage = Math.round((totalEdits / this.dataLen) * 100);

      if (this.approvedPercentage >= 70) {
        this.vol_approval_status = 'Approved';
      }
      else if (percentage >= 70) {
        this.vol_approval_status = 'Approved with edits';


      } else {
        this.vol_approval_status = 'Rejected';
      }
      this.showFinishModal = true;
    }

  },
  created() {
    document.title = "Volume Review";
  },
  mounted() {
    this.getSampleDocument();
    this.loading_images = false;
    this.volumeApproval[this.currentIndex] = '';
  },
  computed: {
    current_slice() {
      try {
        return this.vol_data[this.currentIndex];
      } catch {
        return '';
      }
    },
    current_url() {
      try {
        return this.current_slice['url'];
      } catch {
        return '';
      }
    },
    current_markup() {
      try {
        return this.current_slice['segmentation'];
      } catch (error) {
        return '';
      }
    },

    //Labels for disabled buttons

    arrowLabel() {
      if (this.locked_changes) {
        return 'Cancel or confirm changes before moving on'
      }
      else {
        return null
      }
    },

    volumeCompleted() {
      return Object.values(this.volumeApproval).filter(res => res != '').length;
    },

    missedSlices() {
      console.log(Object.values(this.volumeApproval).findIndex(res => res === ''));
      return Object.values(this.volumeApproval).findIndex(res => res === '');
    }

  },
  watch: {
    approvalToggle() {
      if (this.approvalToggle === true) {
        this.volumeApproval[this.currentIndex] = 'Approved';
      }
      else if (this.approvalToggle === false) {
        this.volumeApproval[this.currentIndex] = 'Rejected';
      }
    },
    currentIndex() {
      if (this.currentIndex in this.volumeApproval) {
        if (this.volumeApproval[this.currentIndex] === 'Approved') {
          this.approvalToggle = true;
        }
        else if (this.volumeApproval[this.currentIndex] === 'Rejected') {
          this.approvalToggle = false;
        }
        else {
          this.approvalToggle = null;
        }
      }
      else {
        this.approvalToggle = null;
        this.volumeApproval[this.currentIndex] = '';
      }
    },
  }
}
</script>

<style scoped lang="scss">
.bar-container {
  margin: auto;
  width: 600px;
  text-align: center;
}



.progress-container {
  position: relative;
  width: 100%;
  margin: 0px auto;
  border-radius: 4px;
  box-sizing: border-box;
}

.Loading {
  position: relative;
  display: inline-block;
  width: 100%;
  height: 10px;
  background: #f1f1f1;
  box-shadow: inset 0 0 5px rgba(0, 0, 0, .2);
  border-radius: 4px;
  overflow: hidden;
}



.Loading:after {
  content: '';
  position: absolute;
  left: 0;
  width: calc(var(--percentage) * 1%);
  background: #b6c98a;
  height: 100%;
  border-radius: 4px;
  box-shadow: 0 0 5px rgba(0, 0, 0, .2);
  transition: width 0.5s ease;
  //animation: load 5s;
}



.tooltip .tooltiptext {
  font-size: 10px;
  visibility: hidden;
  width: auto;
  max-width: 100%;
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

.questionicon {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1;
  color: #000000;
  cursor: pointer;
  font-size: 1.5em;
}

.capitalize::first-letter {
  text-transform: uppercase;
}

.approval-buttons {
  position: relative;
  width: 20%;

  button {
    background-color: #ff7a7a;
    border: none;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 8px;
    opacity: 0.6;
  }

  button:hover {
    opacity: 0.8;
  }

  .selected-button {
    opacity: 1;
    border: 5px solid var(--color);
    padding: 5px 15px;
  }

  .approved {
    background-color: #008000;

  }

  .rejected {
    background-color: #ff0000;
  }
}

.bordered {
  border: 1px solid black;
  padding: 5px;
}

.slice_img {
  width: 100%;
  /* Set a maximum width for the images */
  height: auto;
  /* Set a maximum height for the images */

}


.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  /* Adjust as needed */
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left: 4px solid #3498db;
  /* Change to your preferred color */
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.choice-switch {
  display: flex;
  justify-content: flex-end;
  /* Align items in reverse order */

  align-items: center;
  position: relative;
  z-index: 1;
  width: 90%;
}

.arrow-div {
  width: 50px;
  position: relative;
  display: flex;
  justify-content: center;
  top: 0px;
  height: 45px;
}

div.arrow {
  width: 6vmin;
  height: 6vmin;
  box-sizing: border-box;
  position: absolute;
  top: 0px;

  &::before {
    content: '';
    width: 100%;
    height: 100%;
    border-width: .8vmin .8vmin 0 0;
    border-style: solid;
    border-color: #000000;
    transition: .2s ease;
    display: block;
    transform-origin: 100% 0;
  }


  &:after {
    content: '';
    float: left;
    position: relative;
    top: -100%;
    width: 100%;
    height: 100%;
    border-width: 0 .8vmin 0 0;
    border-style: solid;
    border-color: #000000;
    transform-origin: 100% 0;
    transition: .2s ease;
  }

  &:hover::after {
    transform: rotate(45deg);
    border-color: orange;
    height: 120%;
  }

  &:hover::before {
    border-color: orange;
    transform: scale(.8);

  }

}

div.lock-arrow {
  pointer-events: none;
  opacity: 0.5;

}

div.left_arrow {
  transform: rotate(135deg) scale(0.5, -0.5);
  right: 20px;
}

div.right_arrow {
  transform: rotate(45deg) scale(0.5);
  right: 0px;
}

.submit_button {
  //position: relative;
  outline: none;
  border: none;

  width: 60px;
  height: 30px;

  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  //margin: 0 auto;

  &:hover {
    opacity: 0.5;
  }

}



//=== Button styling, semi-ignore
.btn {
  position: relative;
  top: 5px;
  right: 5px;
  background: none;
  border: none;
  cursor: pointer;
  line-height: 1.5;
  font: 700 1.2rem 'Roboto Slab', sans-serif;
  padding: 1em 2em;
  letter-spacing: 0.05rem;
  transform-origin: top right;
  transform: scale(0.5);

  &:focus {
    outline: 2px dotted #55d7dc;
  }
}
</style>