<script setup>
import { ref, reactive } from 'vue';
import DialogueBox from '../../components/DialogueBox.vue';

const deactiveAccountModal = ref(null);

const deactiveAcc = async(id) => {
    const ok = await deactiveAccountModal.value.open('Are you sure you want to deactivate your account? You can\'t reactivate it without contacting support.');
    if(ok) {
        alert('Account deactivated. Please contact support to reactivate.');
    }else {
        alert('Deactivation cancelled. Your account is safe.');
    }
}

const profile = reactive({
  fullName: 'Dr. Sarah Smith',
  email: 'sarah.smith@example.com',
  phone: '+1 (555) 000-0000',
  dob: '1988-10-12',
  address: '123 Healthcare Ave, Suite 400, Medical Center, NY 10001'
});

const formFields = [
  { id: 'name', label: 'Full Name', key: 'fullName', type: 'text' },
  { id: 'email', label: 'Email Address', key: 'email', type: 'email' },
  { id: 'phone', label: 'Phone Number', key: 'phone', type: 'tel' },
  { id: 'dob', label: 'Date of Birth', key: 'dob', type: 'date' },
];

const preferences = reactive([
  { label: 'Appointment Reminders', desc: 'Receive SMS and email reminders 24 hours before your visit.', enabled: true },
  { label: 'Lab Results Notifications', desc: 'Get notified immediately when your test results are ready.', enabled: true },
  { label: 'Health Tips & Newsletter', desc: 'Monthly curated health advice from our specialists.', enabled: false },
]);

const saveChanges = () => {
  alert('Settings saved successfully!');
};
</script>

<template>
  <div class="max-w-7xl mx-auto p-4 md:p-8 font-sans text-slate-900 bg-[#F8FAFC] min-h-screen">
    <header class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
      <div>
        <h1 class="text-3xl font-black text-slate-900">Patient Profile Settings</h1>
        <p class="text-slate-500 mt-1 text-sm">Manage your account information, security settings, and notifications.</p>
      </div>
      <button @click="saveChanges" class="bg-[#2563eb] text-white px-8 py-3 rounded-xl font-bold text-sm shadow-lg shadow-blue-500/20 hover:bg-blue-700 transition active:scale-95">
        Save Changes
      </button>
    </header>

    <div class="space-y-6">
      <section class="bg-white p-8 rounded-4xl border border-slate-100 shadow-sm">
        <h2 class="text-lg font-bold mb-1">Personal Information</h2>
        <p class="text-xs text-slate-400 mb-8 font-medium">Update your basic profile details and contact information.</p>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div v-for="field in formFields" :key="field.id" class="space-y-2">
            <label :for="field.id" class="text-xs font-black text-slate-400 uppercase tracking-tighter">{{ field.label }}</label>
            <input 
              v-model="profile[field.key]"
              :type="field.type" 
              :id="field.id" 
              class="w-full px-4 py-3 bg-slate-50 border border-slate-100 rounded-xl text-sm focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500 outline-none transition-all"
            />
          </div>
          <div class="md:col-span-2 space-y-2">
            <label class="text-xs font-black text-slate-400 uppercase tracking-tighter">Residential Address</label>
            <textarea 
              v-model="profile.address"
              rows="3" 
              class="w-full px-4 py-3 bg-slate-50 border border-slate-100 rounded-xl text-sm focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500 outline-none transition-all resize-none"
            ></textarea>
          </div>
        </div>
      </section>

      <section class="bg-white p-8 rounded-4xl border border-slate-100 shadow-sm">
        <h2 class="text-lg font-bold mb-1">Preferences</h2>
        <p class="text-xs text-slate-400 mb-8 font-medium">Customize how you receive updates and communications.</p>
        
        <div class="space-y-6">
          <div v-for="pref in preferences" :key="pref.label" class="flex items-center justify-between py-2">
            <div>
              <p class="text-sm font-bold">{{ pref.label }}</p>
              <p class="text-xs text-slate-400">{{ pref.desc }}</p>
            </div>
            <button @click="pref.enabled = !pref.enabled" 
                    :class="pref.enabled ? 'bg-blue-600' : 'bg-slate-200'"
                    class="w-12 h-6 rounded-full relative transition-colors duration-300">
              <div :class="pref.enabled ? 'translate-x-6' : 'translate-x-1'" 
                   class="absolute top-1 w-4 h-4 bg-white rounded-full transition-transform duration-300 shadow-sm"></div>
            </button>
          </div>
        </div>
      </section>

      <section class="bg-red-50/50 p-8 rounded-4xl border border-red-100 flex items-center justify-between">
        <div>
          <h2 class="text-sm font-bold text-red-600">Deactivate Account</h2>
          <p class="text-[10px] text-red-400 font-medium">This will temporarily disable your portal access. You can reactivate it later.</p>
        </div>
        <button @click="deactiveAcc(789)" class="bg-white border cursor-pointer border-red-100 text-red-600 px-6 py-2.5 rounded-xl font-bold text-xs hover:bg-red-50 transition">
          Deactivate
        </button>
      </section>
    </div>
  </div>

  <DialogueBox ref="deactiveAccountModal"></DialogueBox>

</template>

