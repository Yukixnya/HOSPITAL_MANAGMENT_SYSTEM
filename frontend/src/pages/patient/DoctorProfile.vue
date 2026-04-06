<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from "vue-router";
import { getDocDetails, bookAppointment, addReview } from '../../services/patient';
import { Plus } from 'lucide-vue-next';
import  ReviewModal from '../../components/ReviewModal.vue';
import { useToast } from 'vue-toastification';

const toast = useToast();
const route = useRoute();

// --- State ---
const doctor = ref(null);
const reviews = ref([]);
const isBooking = ref(false);
const isLoadingPage = ref(true);

// --- Booking Selections ---
const today = new Date();
const selectedDate = ref(new Date().toISOString().split('T')[0]);
const selectedSlot = ref('10:30 AM');
const slots = ['09:00 AM', '10:30 AM', '01:00 PM', '02:30 PM', '04:00 PM', '05:30 PM'];

// --- Get ID from Route ---
const id = computed(() => route.params.id || route.path.split("/").pop());

// --- Fetch Doctor Data ---
const getDoc = async () => {
  try {
    isLoadingPage.value = true;
    const res = await getDocDetails(id.value);
    doctor.value = res.doctor;
    reviews.value = res.reviews || [];
  } catch (error) {
    toast.error('Failed to fetch doctor details.');
  } finally {
    isLoadingPage.value = false;
  }
};

onMounted(() => {
  getDoc();
});

// --- Helpers & Computed ---
const next15Days = computed(() => {
  const dates = [];
  for (let i = 1; i < 15; i++) {
    const d = new Date();
    d.setDate(today.getDate() + i);
    dates.push({
      fullDate: d.toISOString().split('T')[0],
      dayNum: d.getDate(),
      weekday: d.toLocaleDateString('en-US', { weekday: 'short' }).substring(0, 2),
    });
  }
  return dates;
});

const currentMonthDisplay = computed(() => {
  return today.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
});

// --- Booking Logic ---
const handleBooking = async () => {
  if (!doctor.value || isBooking.value) return;

  try {
    isBooking.value = true;

    const [time, modifier] = selectedSlot.value.split(' ');
    let [hours, minutes] = time.split(':');
    if (hours === '12') hours = '00';
    if (modifier === 'PM') hours = parseInt(hours, 10) + 12;
    const time24 = `${hours.toString().padStart(2, '0')}:${minutes}`;

    const appointmentDateTime = `${selectedDate.value}T${time24}`;

    const payload = {
      doctor_id: id.value,
      date: appointmentDateTime,
      type: doctor.value.title || "Consultation"
    };

    const res = await bookAppointment(payload);
    toast.success("Appointment booked successfully!");
  } catch (error) {
    toast.error("Booking failed. Please try again.");
  } finally {
    isBooking.value = false;
  }
};

const isReviewModalOpen = ref(false);
const submitting = ref(false);

const handleReviewSubmit = async (reviewData) => {
  try {
    submitting.value = true;
    
    await addReview(id.value, reviewData);
    toast.success("Review added successfully!");
    await getDoc();
    isReviewModalOpen.value = false;
  } catch (e) {
    toast.error("Error saving review");
  } finally {
    submitting.value = false;
  }
};

</script>

<template>
  <div v-if="isLoadingPage" class="loading-state">
    <div class="spinner"></div>
    <p>Loading Doctor Profile...</p>
  </div>

  <div v-else-if="doctor" class="profile-page">
    <div class="layout-grid">

      <div class="col-span-8 space-y-6">

        <section class="card-4xl">
          <div style="display: flex; gap: 32px; align-items: flex-start; flex-wrap: wrap;">
            <div style="position: relative; flex-shrink: 0;">
              <img :src="doctor.image" class="doc-header-img" />
              <div class="online-indicator"></div>
            </div>

            <div style="flex: 1;">
              <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <h1 style="font-size: 30px; font-weight: 900; margin: 0;">{{ doctor.name }}</h1>
                <span class="expert-badge">Verified Expert</span>
              </div>
              <p style="color: #64748b; font-weight: 700; margin-bottom: 24px;">{{ doctor.title }}</p>

              <div class="tag-list" style="display: flex; gap: 10px; flex-wrap: wrap;">
                <span>🎓 {{ doctor.education }}</span>
                <span>💼 {{ doctor.experience }}</span>
                <span>🌐 {{ doctor.languages.join(', ') }}</span>
              </div>

              <div class="stats-grid">
                <div class="stat-item">
                  <p class="stat-value">{{ doctor.rating }}</p>
                  <p class="stat-label">Rating</p>
                </div>
                <div class="stat-item">
                  <p class="stat-value" style="color: #2563eb;">✓</p>
                  <p class="stat-label">Status</p>
                </div>
                <div class="stat-item">
                  <p class="stat-value">{{ doctor.reviews }}</p>
                  <p class="stat-label">Reviews</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section class="card-4xl">
          <h2
            style="font-size: 20px; font-weight: 700; margin-bottom: 24px; display: flex; align-items: center; gap: 8px;">
            <span style="color: #2563eb;">👤</span> Professional Bio
          </h2>
          <div style="color: #475569; line-height: 1.7; font-size: 14px;">
            <p>{{ doctor.bio_p1 }}</p>
            <p v-if="doctor.bio_p2" style="margin-top: 16px;">{{ doctor.bio_p2 }}</p>
          </div>
        </section>

        <section class="card-4xl">
          <div class="review-header">
            <h2 class="review-title">
              <span class="star-icon">⭐</span>
              Patient Reviews
            </h2>

            <button @click="isReviewModalOpen = true" class="btn-review">
              <Plus class="icon-sm" />
              <span>Add Review</span>
            </button>
          </div>
          <div v-if="reviews.length > 0"
            style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 24px;">
            <div v-for="review in reviews" :key="review.id" class="review-card">
              <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <div
                  style="width: 32px; height: 32px; border-radius: 50%; background: #dbeafe; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; color: #2563eb;">
                  {{ review.author.charAt(0) }}
                </div>
                <div>
                  <h4 style="font-size: 12px; font-weight: 700; margin: 0;">{{ review.author }}</h4>
                  <div style="color: #facc15; font-size: 10px;">★★★★★</div>
                </div>
              </div>
              <p style="font-size: 11px; color: #64748b; font-style: italic; margin: 0;">"{{ review.comment }}"</p>
            </div>
          </div>
        </section>
      </div>

      <div class="col-span-4">
        <div class="sticky-sidebar">

          <div class="booking-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px;">
              <h3 style="font-size: 18px; font-weight: 700; margin: 0;">Book Session</h3>
              <p style="color: #2563eb; font-weight: 900; margin: 0;">${{ doctor.fee }}<span
                  style="font-size: 10px; color: #94a3b8;"> / hr</span></p>
            </div>

            <div style="margin-bottom: 32px;">
              <p class="stat-label" style="margin-bottom: 16px;">{{ currentMonthDisplay }}</p>
              <div class="no-scrollbar" style="display: flex; gap: 12px; overflow-x: auto; padding-bottom: 8px;">
                <button v-for="date in next15Days" :key="date.fullDate" @click="selectedDate = date.fullDate"
                  :class="['date-btn', selectedDate === date.fullDate ? 'active-date' : '']"
                  style="background: #f8fafc; color: #64748b;">
                  <span style="font-size: 9px; text-transform: uppercase; font-weight: 700;">{{ date.weekday }}</span>
                  <span style="font-size: 14px; font-weight: 900;">{{ date.dayNum }}</span>
                </button>
              </div>
            </div>

            <div style="margin-bottom: 32px;">
              <p class="stat-label" style="margin-bottom: 16px;">Available Slots</p>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                <button v-for="time in slots" :key="time" @click="selectedSlot = time"
                  :class="['slot-btn', selectedSlot === time ? 'active-slot' : '']">
                  {{ time }}
                </button>
              </div>
            </div>

            <button @click="handleBooking" :disabled="isBooking || !selectedSlot" class="btn-confirm">
              {{ isBooking ? 'Processing...' : 'Confirm Appointment' }}
            </button>
          </div>

          <div style="background: #0f172a; color: white; padding: 32px; border-radius: 24px; margin-top: 24px;">
            <p class="stat-label" style="color: #60a5fa; margin-bottom: 16px;">Clinic Location</p>
            <div style="display: flex; gap: 12px;">
              <span>📍</span>
              <p style="font-size: 14px; color: #cbd5e1; margin: 0; line-height: 1.6;">
                Main Medical Plaza, Suite 402, Downtown District, New York
              </p>
            </div>
          </div>

        </div>
      </div>

    </div>
  </div>

  //Modal for adding reviews
  <ReviewModal :isOpen="isReviewModalOpen" :isSubmitting="submitting" @close="isReviewModalOpen = false"
    @submit="handleReviewSubmit" />
</template>

<style src="./styles/docDetails.css" scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}

.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>