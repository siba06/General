<template>
  <div>
    <div v-if="!loading">
      <div v-for="docId in Object.keys(docs)" :key="docId" class="document-container">
        <div @click="toggleVolumes(docId)" class="document-header">
          {{ this.docs[docId].patient_id }}
          <span class="arrow" :class="{ 'arrow-down': selectedDocId === docId }"></span>
        </div>
        <!-- Display volumes if the corresponding index is selected -->
        <div v-if="selectedDocId === docId" class="volume-list">
          <div v-for="(volumeId) in Object.keys(volumesOfSelectedDoc).sort()" :key="volumeId" class="volume-box"
            :style="getVolumeStyle(volumesOfSelectedDoc[volumeId])" @click="returnSelectedVolume(docId, volumeId)">
            {{ 'Volume ' + volumeId.slice(7) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { db } from "../firebase/init.js";
import { query, collection, getDocs } from "firebase/firestore"

export default {
  name: "UnapprovedList",
  data() {
    return {
      doc_data: null,
      doc_keys: [],
      selectedDocId: null, // Keeps track of the selected document index
      loading: false,

      docs: {},
    };
  },
  mounted() {
    this.getDocData();
  },
  methods: {
    returnSelectedVolume(doc_id, volumeId) {
      this.$emit('picked-volume', {
        id: doc_id,
        vol: volumeId.slice(7),
        patient: this.docs[doc_id].patient_id
      });
    },
    async getDocData() {
      //Set doc data and doc keys from firestore

      // query to get all docs in 'countries' collection
      this.loading = true;
      try {

        const docKeysFromFirestore = await getDocs(query(collection(db, 'Pending')));
        docKeysFromFirestore.forEach((doc) => {
          if (Object.values(doc.data()).includes('pending')) {
            this.docs[doc.id] = doc.data();
          }
        });
      } catch (e) {
        alert('Failed to get volumes');
        console.log('Failed to get volumes', e);
      }
      this.loading = false;
    },
    toggleVolumes(index) {
      // Toggle the selected document index
      this.selectedDocId = this.selectedDocId === index ? null : index;
    },
    getVolumeStyle(status) {
      // Return a style object based on the volume status
      let b_col = ''
      if (status === "pending") {
        return { background: "#dcdcdc" }; // Light grey for pending (default)
      } else if (status[0].toLowerCase() === "approved") {
        b_col = "#8effa4"
      } else if (status[0].toLowerCase() === "rejected") {
        b_col = "#ffb8b8"
      } else if (status[0].toLowerCase() === "approved with edits") {
        b_col = "#fffa8e"
      }
      const percentageCompleted = status[1]

      const color = `linear-gradient(90deg, ${b_col} ${percentageCompleted}%, transparent ${percentageCompleted}%)`;
      if (percentageCompleted === 100) {
        return { background: color, pointerEvents: 'none' };
      }
      return { background: color };

    },
  },
  computed: {
    volumesOfSelectedDoc() {
      if (this.selectedDocId !== null) {
        const doc = this.docs[this.selectedDocId];
        // const volumeIds = Object.keys(doc).filter((property) => property.startsWith('volume'));
        let volumes = Object.assign({}, doc)
        delete volumes['patient_id']
        return volumes;
      }

      return [];
    }
  }
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.document-container {
  margin-bottom: 10px;
}

.document-header {
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 5px;
  background-color: #f0f0f0;
  /* Background color for document header */
}

.arrow {
  width: 0;
  height: 0;
  border-style: solid;
  margin-right: 5px;
}

.arrow-down {
  border-width: 0 5px 5px 5px;
  border-color: transparent transparent #333 transparent;
  /* Color of the arrow */
}

.volume-list {
  padding: 5px;
}

.volume-box {
  cursor: pointer;
  padding: 5px;
  margin-bottom: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Add some styling for the clickable area */
</style>
