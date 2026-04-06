<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import DialogueBox from '../../components/DialogueBox.vue';
import RescheduleModal from '../../components/RescheduleModal.vue';
import { cancelAppointment, myAppointments, rescheduleAppointment } from '../../services/patient';
import { useToast } from 'vue-toastification';

const toast = useToast();
const router = useRouter();

// State
const upcomingAppointments = ref([]);
const pastVisits = ref([]);
const currentPage = ref(1);
const totalRecords = ref(0);
const searchQuery = ref('');
const allVisites = ref(false);

// Dialog Controls
const cancelDialog = ref(null);
const isRescheduleOpen = ref(false);
const activeAppointment = ref(null);

// Static/Generated Data
const availableSlots = ['09:00 AM', '10:30 AM', '01:00 PM', '02:30 PM', '04:00 PM', '05:30 PM'];
const next15Days = ref([]);

const generateNext15Days = () => {
  const dates = [];
  for (let i = 0; i < 15; i++) {
    const d = new Date();
    d.setDate(d.getDate() + i);
    dates.push({
      fullDate: d.toISOString().split('T')[0], // Result: "2026-04-02"
      weekday: d.toLocaleDateString('en-US', { weekday: 'short' }),
      dayNum: d.getDate()
    });
  }
  next15Days.value = dates;
};

const getStatusClass = (status) => {
  const s = status?.toLowerCase();
  if (s === 'confirmed' || s === 'completed') return 'bg-green-100 text-green-600';
  if (s === 'pending') return 'bg-yellow-100 text-yellow-600';
  if (s === 'cancelled') return 'bg-red-100 text-red-600';
  return 'bg-slate-100 text-slate-600';
};

const getAppointmentsDetails = async () => {
  try {
    const params = { page: currentPage.value, search: searchQuery.value || undefined, all_past: allVisites.value };
    const data = await myAppointments(params);

    upcomingAppointments.value = (data.upcomingAppointments || []).map(apt => ({
      ...apt,
      date: apt.date,
      statusClass: getStatusClass(apt.status)
    }));

    const fullHistory = data.pastVisits || [];
    pastVisits.value = allVisites.value ? fullHistory : fullHistory.slice(0, 3);
    totalRecords.value = data.pagination?.total_items || 0;
  } catch (error) {
    toast.error("Failed to fetch appointments.");
  }
};

const openReschedule = (apt) => {
  activeAppointment.value = apt;
  isRescheduleOpen.value = true;
};

const processReschedule = async (newData) => {
  try {
    const res = await rescheduleAppointment(activeAppointment.value.id, newData);
    toast.success("Appointment rescheduled successfully!");
    isRescheduleOpen.value = false;
    await getAppointmentsDetails();
  } catch (error) {
    toast.error("Could not reschedule. Please try again.");
  }
};

const cancelAppointmentDialog = async (id) => {
  const confirmed = await cancelDialog.value.open(
    'Cancel Appointment',
    'Are you sure you want to cancel this appointment?'
  );
  if (confirmed) {
    await cancelAppointment(id);
    await getAppointmentsDetails();
  }
};

// Watchers & Lifecycle
let searchTimeout = null;
watch(searchQuery, () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => { getAppointmentsDetails(); }, 500);
});

onMounted(() => {
  getAppointmentsDetails();
  generateNext15Days();
});
</script>

<template>
  <div class="appointments-page">
    <div class="max-container space-y-12">

      <section class="search-section">
        <div class="search-wrapper">
          <span style="position: absolute; left: 16px; top: 50%; transform: translateY(-50%); color: #94a3b8;">🔍</span>
          <input v-model="searchQuery" type="text" placeholder="Search by doctor or clinic..." class="search-input" />
        </div>
      </section>

      <section>
        <h2 class="section-title"><span>📅</span> Upcoming Appointments</h2>

        <div v-if="upcomingAppointments.length === 0"
          style="background: white; padding: 48px; border-radius: 40px; border: 2px dashed #e2e8f0; text-align: center; color: #94a3b8; font-weight: 700;">
          No upcoming appointments scheduled.
        </div>

        <div v-else style="display: flex; flex-direction: column; gap: 16px;">
          <div v-for="apt in upcomingAppointments" :key="apt.id" class="apt-card">

            <div class="date-badge">
              <span class="month">{{ apt.month }}</span>
              <span class="day">{{ apt.day }}</span>
            </div>

            <div style="flex: 1;">
              <h3 style="font-size: 18px; font-weight: 900; margin: 0;">{{ apt.doctor }}</h3>
              <p style="color: #64748b; font-size: 14px; font-weight: 700; margin: 4px 0 12px 0;">
                {{ apt.specialty }} • {{ apt.type }}
              </p>
              <div style="display: flex; gap: 16px; font-size: 11px; font-weight: 700; color: #94a3b8;">
                <span>🕒 {{ apt.time }}</span>
                <span>📍 {{ apt.location }}</span>
              </div>
            </div>

            <div style="display: flex; align-items: center; gap: 16px;">
              <span :class="['status-tag', apt.status === 'Confirmed' ? 'status-confirmed' : 'status-pending']">
                {{ apt.status }}
              </span>
              <div style="display: flex; gap: 8px;">
                <button @click="openReschedule(apt)" class="btn-secondary-sm">Reschedule</button>
                <button @click="cancelAppointmentDialog(apt.id)" class="btn-danger-sm">Cancel</button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section>
        <h2 class="section-title"><span>🕒</span> Past Visits</h2>
        <div class="history-table-wrapper">
          <div style="overflow-x: auto;">
            <table class="medical-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Doctor</th>
                  <th>Department</th>
                  <th>Type</th>
                  <th style="text-align: right;">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="visit in pastVisits" :key="visit.id" @click="router.push(`/past/${visit.id}`)"
                  style="cursor: pointer;">
                  <td style="font-weight: 700; color: #334155;">{{ visit.date }}</td>
                  <td>
                    <div style="display: flex; align-items: center; gap: 12px;">
                      <img :src="visit.img || `https://ui-avatars.com/api/?name=${visit.doctor}`"
                        style="width: 32px; height: 32px; border-radius: 50%; border: 1px solid #f1f5f9;" />
                      <span style="font-weight: 700; font-size: 14px;">{{ visit.doctor }}</span>
                    </div>
                  </td>
                  <td style="color: #64748b; font-size: 12px; font-weight: 700;">{{ visit.department }}</td>
                  <td style="color: #64748b; font-size: 12px; font-weight: 700;">{{ visit.type }}</td>
                  <td @click="router.push(`/patient/my-appointments/past/${visit.id}`)" style="text-align: right;">
                    <span style="color: #2563eb; font-weight: 700; font-size: 12px;">View Notes</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <button v-if="totalRecords > 3" class="view-all-btn"
            style="width: 100%; padding: 16px; background: none; border: none; border-top: 1px solid #f1f5f9; color: #94a3b8; font-size: 10px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.1em; cursor: pointer;">
            View All History ({{ totalRecords }})
          </button>
        </div>
      </section>

      <footer
        style="display: flex; justify-content: space-between; align-items: center; padding-top: 48px; border-top: 1px solid #f1f5f9; margin-top: 48px;">
        <div>
          <p style="font-weight: 900; font-size: 12px; color: #0f172a; margin-bottom: 4px;">Need help with your
            appointment?</p>
          <p style="color: #94a3b8; font-weight: 700; font-size: 12px; margin: 0;">Contact our 24/7 support line at
            1-800-HEALTH-01</p>
        </div>
        <div style="display: flex; gap: 12px;">
          <button
            style="width: 40px; height: 40px; background: white; border: 1px solid #f1f5f9; border-radius: 12px; cursor: pointer; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">❓</button>
          <button
            style="width: 40px; height: 40px; background: white; border: 1px solid #f1f5f9; border-radius: 12px; cursor: pointer; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">💬</button>
        </div>
      </footer>
    </div>
  </div>
  <DialogueBox ref="cancelDialog" />

  <RescheduleModal v-if="isRescheduleOpen && activeAppointment" :is-open="isRescheduleOpen"
    :doctor-name="activeAppointment.doctor" :current-date="activeAppointment.date"
    :current-time="activeAppointment.time" :slots="availableSlots" :next-15-days="next15Days"
    @close="isRescheduleOpen = false" @confirm="processReschedule" />
</template>

<style src="./styles/Apointments.css" scoped></style>
