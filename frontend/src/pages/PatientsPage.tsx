import { Eye, PencilLine, Plus, Search, Trash2, UsersRound } from 'lucide-react'
import StatusBadge from '../components/StatusBadge'

const patients = [
  {
    id: 'pat-001',
    name: 'Hannah Lee',
    lastVisit: 'Jan 28, 2026',
    nextStep: 'Annual physical follow-up',
    status: 'Active care plan',
  },
  {
    id: 'pat-002',
    name: 'Jordan Patel',
    lastVisit: 'Jan 30, 2026',
    nextStep: 'Lab results review',
    status: 'Awaiting confirmation',
  },
  {
    id: 'pat-003',
    name: 'Maya Rivera',
    lastVisit: 'Feb 2, 2026',
    nextStep: 'Telehealth check-in',
    status: 'Confirmed visit',
  },
  {
    id: 'pat-004',
    name: 'Carlos Diaz',
    lastVisit: 'Feb 4, 2026',
    nextStep: 'Reschedule requested',
    status: 'Needs follow-up',
  },
]

const PatientsPage = () => {
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">My patients</h1>
        <p className="mt-1 text-sm text-slate-600">
          Manage patient records tied to appointments and call activity.
        </p>
        </div>
        <button className="inline-flex items-center gap-2 rounded-full bg-primary px-4 py-2 text-sm font-semibold text-white transition hover:bg-blue-700">
          <Plus className="h-4 w-4" />
          Add patient
        </button>
      </div>

      <div className="flex flex-wrap items-center gap-3 rounded-2xl border border-slate-200 bg-white px-4 py-3 shadow-soft">
        <Search className="h-4 w-4 text-slate-400" />
        <input
          type="search"
          placeholder="Search patients by name or last visit"
          className="flex-1 text-sm text-slate-700 outline-none"
        />
        <div className="flex items-center gap-2 text-xs text-slate-500">
          <UsersRound className="h-4 w-4" />
          128 active patients
        </div>
      </div>

      <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-soft">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-6 py-4">Patient</th>
              <th className="px-6 py-4">Last visit</th>
              <th className="px-6 py-4">Next step</th>
              <th className="px-6 py-4">Status</th>
              <th className="px-6 py-4">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {patients.map((patient) => {
              const variant =
                patient.status === 'Needs follow-up' || patient.status === 'Awaiting confirmation'
                  ? 'warning'
                  : 'success'

              return (
                <tr key={patient.id} className="hover:bg-slate-50">
                  <td className="px-6 py-4 font-semibold text-slate-900">{patient.name}</td>
                  <td className="px-6 py-4 text-slate-600">{patient.lastVisit}</td>
                  <td className="px-6 py-4 text-slate-600">{patient.nextStep}</td>
                  <td className="px-6 py-4">
                    <StatusBadge label={patient.status} variant={variant} />
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3 text-xs font-semibold text-slate-600">
                      <button className="inline-flex items-center gap-1 text-primary">
                        <Eye className="h-3.5 w-3.5" />
                        View
                      </button>
                      <button className="inline-flex items-center gap-1 text-slate-500">
                        <PencilLine className="h-3.5 w-3.5" />
                        Edit
                      </button>
                      <button className="inline-flex items-center gap-1 text-rose-500">
                        <Trash2 className="h-3.5 w-3.5" />
                        Remove
                      </button>
                    </div>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default PatientsPage
