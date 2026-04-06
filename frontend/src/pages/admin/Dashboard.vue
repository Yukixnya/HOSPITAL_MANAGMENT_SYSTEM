<script setup>
import { ref, onMounted, computed } from 'vue';
import { 
  Stethoscope, User, DollarSign, Calendar, 
  CheckCircle2, AlertTriangle, PlusCircle, 
} from 'lucide-vue-next';

import { adminDashboard } from '../../services/admin';
import StatCard from '../../components/StateCard.vue';
import AppointmentTrendsChart from '../../components/AppointmentTrendsChart.vue';
import { useToast } from 'vue-toastification';

const toast = useToast();

const dashboard = ref({ "patients": 0, "doctors": 0, "appointments": 0 });

const getAdminDashboard = async() => {
    try {
        const res = await adminDashboard();
        dashboard.value = {
            "patients": res.total_patients,
            "doctors": res.total_doctors,
            "appointments": res.total_appointments
        };
    } catch (error) {
        toast.error("Unable to fetch dashboard data.");
    }
}

onMounted(() => { getAdminDashboard(); });

const stats = computed(() => [
  { title: 'Total Doctors', value: dashboard.value.doctors, trend: '+2.4%', isUp: true, icon: Stethoscope, type: 'blue' },
  { title: 'Active Patients', value: dashboard.value.patients, trend: '+5.1%', isUp: true, icon: User, type: 'indigo' },
  { title: "Today's Appointments", value: dashboard.value.appointments, trend: '-3.2%', isUp: false, icon: Calendar, type: 'orange' }
]);

const activity = [
    { id: 1, title: 'New appointment', detail: 'scheduled for John Doe', time: '10 minutes ago', icon: PlusCircle, status: 'info' },
    { id: 2, title: 'Surgery completed', detail: 'by Dr. Michael Chen', time: '45 minutes ago', icon: CheckCircle2, status: 'success' },
    { id: 3, title: 'Critical alert', detail: 'Low stock for insulin', time: '2 hours ago', icon: AlertTriangle, status: 'warning' },
];
</script>

<template>
    <div class="dashboard-container">
        <div class="stats-row">
            <StatCard v-for="stat in stats" :key="stat.title" v-bind="stat" />
        </div>

        <div class="main-grid">
            
            <div class="content-left">
                <AppointmentTrendsChart />
            </div>
        </div>
    </div>
</template>

<style src="../../styles/adminDashboard.css" scoped></style>
