<script setup>
import { onMounted, ref, computed } from 'vue';
import {
    Trash2,
    History,
    Stethoscope,
    Search,
    Plus,
    Save,
    Phone
} from 'lucide-vue-next';
import AddmedicationModal from '../../components/AddmedicationModal.vue';
import { addMedicalRecord, addNotes, addVitals, addPrescription, getAppointmentReport } from '../../services/doctor';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';

const toast = useToast();
const route = useRoute();
const router = useRouter();
const id = computed(() => route.params.id || route.path.split("/").pop());

// --- State Management ---
const patient = ref(null);
const loading = ref(true);
const isSaving = ref(false);
const isOpen = ref(false);

const diagnosis = ref({
    title: '',
    description: '',
    note_id: null,
    prescription_id: null,
    vitals_id: null,
});

const vitals = ref([
    { label: 'Blood Pressure', value: '', unit: 'mmHg' },
    { label: 'Heart Rate', value: '', unit: 'bpm' }
]);

const prescriptions = ref([]);

// --- Methods ---
const fetchReport = async () => {
    try {
        loading.value = true;
        const report = await getAppointmentReport(id.value);
        console.log("Fetched Report:", report);
        patient.value = {
            report_id: report?.id || id.value,
            patient_id: report.patient?.id || 'N/A',
            medical_id: report.patient?.medical_id || 'N/A',
            name: report.patient?.name || 'Unknown Patient',
            age: report.patient?.age || '--',
            gender: report.patient?.gender || '--',
            time: report.date ? formattedTime(report.date) : "10:30 AM"
        };
    } catch (error) {
        toast.error('Failed to fetch appointment report. Please try again later.');
    } finally {
        loading.value = false;
    }
};

const addMedication = (med) => {
    prescriptions.value.push({
        id: Date.now(),
        name: med.name,
        dosage: med.dosage,
        frequency: med.frequency
    });
    isOpen.value = false;
};

const removeMedication = (medId) => {
    prescriptions.value = prescriptions.value.filter(m => m.id !== medId);
};

const handleSave = async () => {
    if (!diagnosis.value.primary || !diagnosis.value.symptoms) {
        alert("Please fill in the primary diagnosis and symptoms.");
        return;
    }

    if (!diagnosis.value.notes?.trim()) {
        alert("Please add clinical notes.");
        return;
    }

    const hasIncompleteVitals = vitals.value.some(v => !v.value);
    if (hasIncompleteVitals) {
        alert("Please fill in all vitals.");
        return;
    }

    try {
        isSaving.value = true;

        // --- Prepare Data ---
        const vitalsData = vitals.value.map(v => ({
            
            label: v.label,
            value: v.value,
            unit: v.unit
        }));

        const prescriptionsData = prescriptions.value.map(m => ({
            name: m.name,
            dosage: m.dosage,
            frequency: m.frequency,
            duration: m.duration || "N/A"
        }));

        // --- 1. Create vitals ---
        const vitalsRes = await addVitals(id.value, vitalsData);
        const vitalIds = vitalsRes.ids;

        // --- 2. Create prescriptions ---
        const presRes = await addPrescription(id.value, prescriptionsData);
        const prescriptionIds = presRes.ids;

        // --- 3. Create note ---
        const noteRes = await addNotes(id.value, {
            text: diagnosis.value.notes
        });
        const noteId = noteRes.id;

        // --- 4. Create medical record ---
        await addMedicalRecord(id.value, {
            title: diagnosis.value.primary,
            description: diagnosis.value.symptoms,
            vital_ids: vitalIds,
            prescription_ids: prescriptionIds,
            note_ids: [noteId],
        });

        toast.success("Consultation saved successfully!");
        router.push("/doctor/appointments");

    } catch (error) {
        toast.error("Failed to save consultation.");
    } finally {
        isSaving.value = false;
    }
};

const formattedTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString("en-IN", {
        hour: "2-digit",
        minute: "2-digit",
        hour12: true
    });
};

onMounted(fetchReport);
</script>

<template>
    <div class="p-6 lg:p-10 bg-[#f8fafc] min-h-screen font-sans text-slate-600">
        <div v-if="loading" class="flex items-center justify-center h-64">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>

        <div v-else class="max-w-7xl mx-auto">
            <div class="bg-white rounded-3xl p-6 shadow-sm border border-slate-200/60 mb-8 flex flex-col md:flex-row justify-between items-center gap-6">
                <div class="flex items-center gap-6 w-full">
                    <div class="relative">
                        <img :src="`https://i.pravatar.cc/150?u=${patient?.id}`"
                            class="w-20 h-20 rounded-2xl object-cover ring-4 ring-slate-50 shadow-sm" />
                        <div class="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 border-4 border-white rounded-full"></div>
                    </div>
                    <div>
                        <div class="flex items-center gap-3">
                            <h1 class="text-2xl font-bold text-slate-800">{{ patient?.name }}</h1>
                            <span class="bg-slate-100 text-slate-500 text-[10px] font-black px-2 py-1 rounded-md tracking-wider">
                                ID: #{{ patient?.medical_id }}
                            </span>
                        </div>
                        <p class="text-slate-500 font-medium mt-1 flex items-center gap-2">
                            {{ patient?.age }} Years • {{ patient?.gender }} • <span class="text-blue-600">{{ patient?.time }}</span>
                        </p>
                    </div>
                </div>
                <div class="flex gap-3 w-full md:w-auto">
                    <button @click="router.push(`/doctor/patients/${patient.patient_id}`)" class="flex-1 md:flex-none px-5 py-2.5 bg-white border border-slate-200 text-slate-700 font-bold text-sm hover:bg-slate-50 rounded-xl transition-all flex items-center justify-center gap-2">
                        <History class="w-4 h-4" /> History
                    </button>
                    <button class="flex-1 md:flex-none px-6 py-2.5 bg-blue-600 text-white font-bold text-sm rounded-xl shadow-lg shadow-blue-200 hover:bg-blue-700 transition-all flex items-center justify-center gap-2">
                        <Phone class="w-4 h-4" /> Contact
                    </button>
                </div>
            </div>

            <div class="grid grid-cols-12 gap-8">
                <div class="col-span-12 lg:col-span-8 space-y-8">
                    <div class="bg-white rounded-3xl p-8 border border-slate-200/60 shadow-sm">
                        <div class="flex items-center gap-3 mb-8">
                            <div class="p-2 bg-blue-50 rounded-lg">
                                <Stethoscope class="w-5 h-5 text-blue-600" />
                            </div>
                            <h2 class="text-sm font-black text-slate-400 uppercase tracking-widest">Diagnosis & Symptoms</h2>
                        </div>

                        <div class="space-y-6">
                            <div>
                                <label class="text-[11px] font-bold text-slate-400 uppercase mb-2 block ml-1">Primary Diagnosis</label>
                                <div class="relative group">
                                    <Search class="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 group-focus-within:text-blue-500 transition-colors" />
                                    <input v-model="diagnosis.primary" type="text" placeholder="e.g. Hypertension..."
                                        class="w-full pl-11 pr-4 py-3.5 bg-slate-50/50 rounded-2xl border border-slate-100 focus:bg-white focus:ring-4 focus:ring-blue-50 focus:border-blue-200 transition-all outline-none" />
                                </div>
                            </div>
                            <div>
                                <label class="text-[11px] font-bold text-slate-400 uppercase mb-2 block ml-1">Observations & Symptoms</label>
                                <textarea v-model="diagnosis.symptoms" placeholder="Note down symptoms..."
                                    class="w-full p-4 bg-slate-50/50 rounded-2xl border border-slate-100 h-32 focus:bg-white focus:ring-4 focus:ring-blue-50 focus:border-blue-200 transition-all outline-none resize-none"></textarea>
                            </div>
                        </div>
                    </div>

                    <div class="bg-white rounded-3xl p-8 border border-slate-200/60 shadow-sm">
                        <div class="flex justify-between items-center mb-8">
                            <h2 class="text-sm font-black text-slate-400 uppercase tracking-widest">Prescription</h2>
                            <button @click="isOpen = true" class="flex items-center gap-1.5 px-4 py-2 bg-blue-50 text-blue-600 rounded-xl text-xs font-bold hover:bg-blue-100 transition-colors">
                                <Plus class="w-4 h-4" /> Add Medication
                            </button>
                        </div>

                        <div class="overflow-hidden">
                            <table class="w-full text-left">
                                <thead>
                                    <tr class="text-[10px] font-black uppercase text-slate-400 border-b border-slate-100">
                                        <th class="pb-4">Medication</th>
                                        <th class="pb-4">Instructions</th>
                                        <th class="pb-4 text-right">Action</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-50">
                                    <tr v-for="med in prescriptions" :key="med.id" class="group hover:bg-slate-50/50">
                                        <td class="py-5">
                                            <p class="text-sm font-bold text-slate-700">{{ med.name }}</p>
                                            <p class="text-xs text-slate-400">{{ med.dosage }}</p>
                                        </td>
                                        <td class="py-5 text-sm font-medium text-slate-500">{{ med.frequency }}</td>
                                        <td class="py-5 text-right">
                                            <button @click="removeMedication(med.id)" class="p-2.5 text-slate-300 hover:text-red-500 hover:bg-red-50 rounded-lg transition-all">
                                                <Trash2 class="w-4 h-4" />
                                            </button>
                                        </td>
                                    </tr>
                                    <tr v-if="prescriptions.length === 0">
                                        <td colspan="3" class="py-10 text-center text-slate-400 italic text-sm">No medications added yet.</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <div class="col-span-12 lg:col-span-4 space-y-8">
                    <div class="bg-white rounded-3xl p-8 border border-slate-200/60 shadow-sm">
                        <h2 class="text-sm font-black text-slate-400 uppercase tracking-widest mb-6">Patient Vitals</h2>
                        <div class="grid grid-cols-2 gap-4">
                            <div v-for="v in vitals" :key="v.label" class="p-4 bg-slate-50/50 rounded-2xl border border-slate-100">
                                <p class="text-[9px] font-black text-slate-400 uppercase mb-2 tracking-tight">{{ v.label }}</p>
                                <div class="flex items-end gap-1">
                                    <input v-model="v.value" placeholder="0" class="bg-transparent font-bold text-slate-800 w-full outline-none focus:text-blue-600" />
                                    <span class="text-[10px] font-bold text-slate-400 mb-0.5">{{ v.unit }}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="bg-white rounded-3xl p-8 border border-slate-200/60 shadow-sm">
                        <h2 class="text-sm font-black text-slate-400 uppercase tracking-widest mb-6">Clinical Notes</h2>
                        <div class="bg-slate-50/50 rounded-2xl p-4 border border-slate-100 focus-within:ring-2 focus-within:ring-blue-50 transition-all">
                            <textarea v-model="diagnosis.notes"
                                class="w-full bg-transparent border-none focus:ring-0 text-slate-700 placeholder:text-slate-400 leading-relaxed resize-none min-h-50 outline-none text-sm"
                                placeholder="Start typing internal notes..."></textarea>
                        </div>
                    </div>

                    <button @click="handleSave" :disabled="isSaving"
                        class="w-full group px-4 py-4 bg-slate-900 text-white font-bold text-sm rounded-2xl shadow-xl hover:bg-blue-600 transition-all flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed">
                        <Save v-if="!isSaving" class="w-4 h-4 group-hover:scale-110 transition-transform" />
                        <span v-if="isSaving" class="flex items-center gap-2">
                            <div class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                            Saving...
                        </span>
                        <span v-else>Complete Consultation</span>
                    </button>
                </div>
            </div>
        </div>

        <AddmedicationModal :isOpen="isOpen" @close="isOpen = false" @add="addMedication" />
    </div>
</template>