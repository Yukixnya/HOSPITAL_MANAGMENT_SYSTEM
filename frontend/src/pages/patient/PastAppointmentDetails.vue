<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getAppointmentDetails } from '../../services/patient';
import { useToast } from 'vue-toastification';

const toast = useToast();
const router = useRouter();
const id = router.currentRoute.value.params.id;

const details = ref({});
const prescriptions = ref([]);
const notes = ref([]);
const visitVitals = ref([]);
const isLoading = ref(true);

const getVisitDetails = async () => {
    try {
        isLoading.value = true;
        const res = await getAppointmentDetails(id);
        
        details.value = res.details || {};
        prescriptions.value = res.prescriptions || [];
        notes.value = res.notes || [];
        visitVitals.value = res.visitVitals || [];
        
    } catch (error) {
        toast.error("Failed to fetch appointment details.");
    } finally {
        isLoading.value = false;
    }
}

onMounted(() => {
    getVisitDetails();
});
</script>

<template>
  <div v-if="isLoading" style="display: flex; align-items: center; justify-content: center; min-height: 100vh;">
    <div style="width: 48px; height: 48px; border: 4px solid #f1f5f9; border-top-color: #2563eb; border-radius: 50%;" class="animate-spin"></div>
  </div>

  <div v-else class="summary-page">
    <div class="max-w-7xl space-y-8">
      
      <header>
        <h1 class="text-3xl">Visit Summary & Results</h1>
        <p style="color: #64748b; font-weight: 700; margin-top: 4px;">Appointment on {{ details.dateFormatted }}</p>
      </header>

      <section>
        <h2 style="font-size: 18px; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
          <span style="color: #ef4444;">❤️</span> Visit Vitals
        </h2>
        <div class="vitals-grid">
          <div v-for="v in visitVitals" :key="v.label" class="vital-stat-card">
            <p class="label-caps" style="margin-bottom: 8px;">{{ v.label }}</p>
            <p style="font-size: 24px; font-weight: 900; margin: 0;">
              {{ v.value }} <span style="font-size: 12px; font-weight: 700; color: #94a3b8;">{{ v.unit }}</span>
            </p>
          </div>
        </div>
      </section>

      <div class="grid-cols-12">
        
        <div class="col-span-12 lg:col-span-8" style="display: flex; flex-direction: column; gap: 32px;">
          
          <section class="card-4xl">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
              <div class="icon-box bg-blue-soft">🏥</div>
              <h2 style="font-size: 20px; font-weight: 700; margin: 0;">Primary Diagnosis</h2>
            </div>
            <div style="background: rgba(248, 250, 252, 0.5); border: 1px solid #f1f5f9; padding: 24px; border-radius: 24px;">
              <h3 style="font-size: 20px; font-weight: 900; color: #2563eb; margin: 0 0 4px 0;">{{ details.diagnosisTitle }}</h3>
              <p class="label-caps" style="margin-bottom: 16px;">
                ICD-10: {{ details.diagnosisCode }} • Status: {{ details.diagnosisStatus }}
              </p>
              <p style="color: #475569; line-height: 1.6; font-size: 14px; font-weight: 500;">
                {{ details.diagnosisDesc }}
              </p>
            </div>
          </section>

          <section class="card-4xl">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
              <div style="display: flex; align-items: center; gap: 12px;">
                <div class="icon-box bg-green-soft">💊</div>
                <h2 style="font-size: 20px; font-weight: 700; margin: 0;">Prescriptions</h2>
              </div>
              <span style="background: #dcfce7; color: #16a34a; font-size: 10px; font-weight: 900; padding: 4px 12px; border-radius: 99px;">
                {{ prescriptions.length }} ACTIVE
              </span>
            </div>
            <div style="display: flex; flex-direction: column; gap: 16px;">
              <div v-for="med in prescriptions" :key="med.name" class="medication-row">
                <div style="width: 48px; height: 48px; background: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px;">💊</div>
                <div>
                  <h4 style="font-weight: 700; color: #1e293b; margin: 0;">{{ med.name }}</h4>
                  <p class="label-caps" style="color: #94a3b8; font-size: 9px;">{{ med.dosage }} • {{ med.duration }}</p>
                  <p style="margin-top: 4px; color: #2563eb; font-size: 10px; font-weight: 900;">FREQUENCY: {{ med.frequency }}</p>
                </div>
              </div>
            </div>
          </section>
        </div>

        <div class="col-span-12 lg:col-span-4" style="display: flex; flex-direction: column; gap: 24px;">
          
          <section class="card-4xl">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
              <div class="icon-box bg-purple-soft">📝</div>
              <h2 style="font-size: 20px; font-weight: 700; margin: 0;">Visit Notes</h2>
            </div>
            <div class="notes-timeline">
              <div v-for="(note, index) in notes" :key="index" style="position: relative;">
                <div class="note-dot"></div>
                <p style="font-size: 13px; color: #475569; font-style: italic; font-weight: 500; line-height: 1.5; margin: 0;">
                  "{{ note.text }}"
                </p>
              </div>
            </div>
          </section>

          <section class="provider-dark-card">
            <p class="label-caps" style="color: #64748b; margin-bottom: 24px;">Your Care Provider</p>
            <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 32px;">
              <img :src="details.doctorImage" style="width: 64px; height: 64px; border-radius: 16px; border: 2px solid #334155; object-fit: cover;" />
              <div>
                <p style="font-size: 18px; font-weight: 700; margin: 0;">{{ details.doctorName }}</p>
                <p style="color: #60a5fa; font-size: 10px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px;">{{ details.doctorDepartment }}</p>
              </div>
            </div>
            <button style="width: 100%; background: #2563eb; color: white; padding: 16px; border-radius: 16px; border: none; font-weight: 700; cursor: pointer; transition: 0.2s;">
              ✉️ Send Message
            </button>
          </section>

        </div>
      </div>
    </div>
  </div>
</template>

<style src="./styles/pastApp.css" scoped></style>