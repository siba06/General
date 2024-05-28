<template>
  <div>
    <ConfirmModal v-if="first_use">
      <template v-slot:header>
        <div>Welcome</div>
      </template>
      <template v-slot:body>
        <div>
          <p>To get started, we recommend exploring our menu options:</p>
          <p>1. Click on the menu button located in the top-left corner of the screen.</p>
          <p>2. Navigate to the "About" tab: Here, you'll find valuable information on how to use our website
            effectively.
          </p>
          <p>Once you've familiarized yourself with the platform through the About tab, feel free to begin using the
            platform to view, edit, and approve pending samples.</p>
          <p>If you have any questions or need assistance, don't hesitate to reach out to us.</p>
          <p>For any technical issues, please contact siba.al-dalaty@durham.ac.uk </p>
        </div>
      </template>
      <template v-slot:footer>
        <div @click="first_use = false"><i class="fa-solid fa-xmark closemark"></i></div>
      </template>
    </ConfirmModal>
  </div>
  <div class="listHalf">
    <h3>Patients Pending Approval</h3>
    <UnapprovedList @picked-volume="openVolumeSampler" />
    <modal :show="showModal" @close="this.showModal = false" @size-selection="goToVolume" />
  </div>
</template>

<script>
import UnapprovedList from '@/components/UnapprovedList.vue';
import SamplePicker from '@/components/SamplePicker.vue';
import ConfirmModal from '@/components/ConfirmModal.vue';
import { auth, db } from '../firebase/init.js';
import { where, query, getDocs, updateDoc, doc, collection } from 'firebase/firestore';



export default {
  name: 'PendingApprovalView',
  components: {
    UnapprovedList,
    ConfirmModal,
    'Modal': SamplePicker,
  },
  data() {
    return {
      volParams: null,
      showModal: false,
      user_status: null,
      first_use: false,
    }
  },
  methods: {
    openVolumeSampler(newData) {
      this.volParams = newData;
      this.showModal = true;

    },
    goToVolume(newData) {
      this.showModal = false;
      this.$router.push({ name: 'volume', query: { samplesize: [newData['percent'], newData['min'], newData['max']] }, params: this.volParams })
    },
    async fetchStatus(email) {
      const q = query(collection(db, "Users"), where("email", "==", email));
      const querySnapshot = await getDocs(q);

      let status = "";
      querySnapshot.forEach(async (userdoc) => {
        if (userdoc.data().status === "registered") {
          status = "registered";
          const docRef = doc(db, "Users", userdoc.id);
          await updateDoc(docRef, {
            ['status']: "verified"
          });
        } else {
          status = userdoc.data().status;
        }
      });

      return status;
    },
  },
  async mounted() {
    this.user_status = await this.fetchStatus(auth.currentUser.email);
  },
  created() {
    document.title = "Pending";

  },
  watch: {
    user_status() {
      if (this.user_status === "registered") {
        this.first_use = true;
      }
    }
  }
}
</script>

<style scoped>
.listHalf {
  width: 60%;
  padding: 20px;
  margin: 0 auto;
  text-align: center;
}

.closemark {
  cursor: pointer;
}

.closemark:hover {
  opacity: 0.2;
}
</style>