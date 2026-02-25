import './App.css'
import { useState, useEffect } from 'react'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

const TABS = [
  { tab: 'dashboard',   label: 'Home' },
  { tab: 'students',    label: 'Students' },
  { tab: 'staff',       label: 'Staff' },
  { tab: 'classrooms',  label: 'Classrooms' },
  { tab: 'exams',       label: 'Exams' },
  { tab: 'allocations', label: 'Allocations' },
]

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="app-root">
      <header className="navbar">
        <div className="navbar-inner">
          <div className="navbar-brand">
            <div className="brand-logo">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <rect x="3" y="3" width="8" height="8" rx="1.5" fill="currentColor"/>
                <rect x="13" y="3" width="8" height="8" rx="1.5" fill="currentColor" opacity="0.55"/>
                <rect x="3" y="13" width="8" height="8" rx="1.5" fill="currentColor" opacity="0.55"/>
                <rect x="13" y="13" width="8" height="8" rx="1.5" fill="currentColor" opacity="0.25"/>
              </svg>
            </div>
            <span className="brand-name">CIA Allocator</span>
          </div>
          <nav className="navbar-nav">
            {TABS.map(({ tab, label }) => (
              <button
                key={tab}
                className={`nav-btn ${activeTab === tab ? 'active' : ''}`}
                onClick={() => setActiveTab(tab)}
              >
                {label}
              </button>
            ))}
          </nav>
        </div>
      </header>

      <main className="page-root">
        {activeTab === 'dashboard'   && <Dashboard setActiveTab={setActiveTab} />}
        {activeTab === 'students'    && <StudentsPage />}
        {activeTab === 'staff'       && <StaffPage />}
        {activeTab === 'classrooms'  && <ClassroomsPage />}
        {activeTab === 'exams'       && <ExamsPage />}
        {activeTab === 'allocations' && <AllocationsPage />}
      </main>
    </div>
  )
}

// ─── Hook ─────────────────────────────────────────────────────────────────────
function useApiList(url) {
  const [items, setItems]     = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)

  const fetchItems = async () => {
    setLoading(true); setError(null)
    try {
      const res  = await fetch(url)
      if (!res.ok) throw new Error(`Request failed with status ${res.status}`)
      const data = await res.json()
      setItems(Array.isArray(data) ? data : Array.isArray(data?.data) ? data.data : [])
    } catch (err) {
      setError(err.message === 'Failed to fetch'
        ? `Cannot reach backend at ${API_BASE_URL}. Make sure the FastAPI server is running.`
        : err.message || 'Failed to fetch data')
    } finally { setLoading(false) }
  }

  useEffect(() => { fetchItems() }, [url])
  return { items, setItems, loading, error, refresh: fetchItems }
}

// ─── Dashboard ────────────────────────────────────────────────────────────────
function Dashboard({ setActiveTab }) {
  const [status, setStatus] = useState('checking')

  useEffect(() => {
    fetch(`${API_BASE_URL}/`)
      .then(r => { if (!r.ok) throw new Error(); setStatus('online') })
      .catch(() => setStatus('offline'))
  }, [])

  return (
    <div className="landing">
      {/* Hero */}
      <div className="hero">
        <div className="hero-content">
          <div className="hero-badge">
            <span className={`pulse-dot ${status}`} />
            {status === 'online' ? 'System Online' : status === 'offline' ? 'Backend Offline' : 'Connecting…'}
          </div>
          <h1 className="hero-title">
            Automate CIA Exam<br />Seating &amp; Duty Allocation
          </h1>
          <p className="hero-desc">
            Stop juggling spreadsheets. Manage students, staff, and classrooms in one place —
            then generate department-mixed seating and invigilator assignments instantly.
          </p>
          <div className="hero-actions">
            <button className="cta-btn" onClick={() => setActiveTab('exams')}>Schedule an Exam</button>
            <button className="cta-btn-outline" onClick={() => setActiveTab('allocations')}>View Allocations</button>
          </div>
        </div>
        <div className="hero-visual">
          <div className="visual-card vc-1">
            <div className="vc-icon">◈</div>
            <div className="vc-label">Smart Seating</div>
            <div className="vc-desc">Departments mixed automatically across rooms</div>
          </div>
          <div className="visual-card vc-2">
            <div className="vc-icon">⊙</div>
            <div className="vc-label">Auto Duty</div>
            <div className="vc-desc">Invigilators assigned by room capacity</div>
          </div>
          <div className="visual-card vc-3">
            <div className="vc-icon">◻</div>
            <div className="vc-label">One Record</div>
            <div className="vc-desc">All exam data in a single system</div>
          </div>
        </div>
      </div>

      {/* How it works */}
      <div className="section-block">
        <p className="section-eyebrow">How it works</p>
        <div className="steps-grid">
          {[
            { n: '01', title: 'Register your data', desc: 'Add students with USN, department, and semester. Register staff members and mark their invigilation availability. Add every classroom with its block and capacity.' },
            { n: '02', title: 'Schedule the exam', desc: 'Create a CIA exam entry with the subject name, scheduled date and time, and target semester. Students from that semester are automatically included.' },
            { n: '03', title: 'Generate & review', desc: 'Click Generate Allocation. The engine mixes departments across rooms, respects seating capacity, and assigns the correct number of invigilators per room.' },
          ].map(s => (
            <div className="step" key={s.n}>
              <div className="step-n">{s.n}</div>
              <h3 className="step-title">{s.title}</h3>
              <p className="step-desc">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Features */}
      <div className="section-block">
        <p className="section-eyebrow">Why use CIA Allocator</p>
        <div className="features-grid">
          {[
            { icon: '⊞', title: 'Department-mixed seating', desc: 'Students from the same department are spread across rooms, significantly reducing malpractice risk during exams.' },
            { icon: '◑', title: 'Capacity-aware rooms', desc: 'The allocation engine always respects your classroom capacity limits. No room is ever over-allocated.' },
            { icon: '⊙', title: 'Smart invigilator duty', desc: 'Invigilators are auto-assigned based on room size. Larger rooms automatically get more staff on duty.' },
            { icon: '◻', title: 'Centralised records', desc: 'All students, staff, classrooms, and exam records live in one place — no more cross-referencing multiple sheets.' },
          ].map(f => (
            <div className="feature-card" key={f.title}>
              <span className="feature-icon">{f.icon}</span>
              <h4 className="feature-title">{f.title}</h4>
              <p className="feature-desc">{f.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Quick nav */}
      <div className="section-block">
        <p className="section-eyebrow">Get started</p>
        <div className="quicknav-grid">
          {[
            { tab: 'students',    label: 'Manage Students',   desc: 'Add, view or remove student records.' },
            { tab: 'staff',       label: 'Manage Staff',      desc: 'Register invigilators and availability.' },
            { tab: 'classrooms',  label: 'Manage Classrooms', desc: 'Set up rooms with block and capacity.' },
            { tab: 'exams',       label: 'Schedule Exams',    desc: 'Create CIA exams by semester and date.' },
            { tab: 'allocations', label: 'Allocations',       desc: 'Generate and review seating plans.' },
          ].map(n => (
            <button className="quicknav-card" key={n.tab} onClick={() => setActiveTab(n.tab)}>
              <span className="qn-label">{n.label}</span>
              <span className="qn-desc">{n.desc}</span>
              <span className="qn-arrow">→</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

// ─── Page shell ───────────────────────────────────────────────────────────────
function PageWrap({ title, subtitle, loading, error, onRefresh, children }) {
  return (
    <div className="page-wrap">
      <div className="page-head">
        <div>
          <h2 className="page-title">{title}</h2>
          {subtitle && <p className="page-sub">{subtitle}</p>}
        </div>
        <button className="refresh-btn" onClick={onRefresh} disabled={loading}>
          <svg width="13" height="13" fill="none" stroke="currentColor" strokeWidth="2.2" viewBox="0 0 24 24">
            <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>
          </svg>
          Refresh
        </button>
      </div>
      {loading && <div className="loader-bar"><div className="loader-fill" /></div>}
      {error && <div className="err-box">{error}</div>}
      {children}
    </div>
  )
}

function Field({ label, children }) {
  return (
    <div className="field-wrap">
      <label className="field-label">{label}</label>
      {children}
    </div>
  )
}

function EmptyRow({ msg }) {
  return <tr><td colSpan="99" className="empty-td">{msg}</td></tr>
}

// ─── Students ─────────────────────────────────────────────────────────────────
function StudentsPage() {
  const { items, setItems, loading, error, refresh } = useApiList(`${API_BASE_URL}/api/students/`)
  const [form, setForm]     = useState({ usn: '', name: '', semester: '', department: '' })
  const [saving, setSaving] = useState(false)

  const handleChange = e => setForm(p => ({ ...p, [e.target.name]: e.target.value }))

  const handleSubmit = async e => {
    e.preventDefault(); setSaving(true)
    try {
      const res = await fetch(`${API_BASE_URL}/api/students/`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ usn: form.usn.trim(), name: form.name.trim(), semester: Number(form.semester), department: form.department.trim() }),
      })
      if (!res.ok) throw new Error(`Failed with status ${res.status}`)
      const json = await res.json()
      setItems(p => [...p, json?.data || json])
      setForm({ usn: '', name: '', semester: '', department: '' })
    } catch (err) { alert(err.message || 'Failed to create student') }
    finally { setSaving(false) }
  }

  const handleDelete = async id => {
    if (!confirm('Delete this student?')) return
    try {
      const res = await fetch(`${API_BASE_URL}/api/students/${id}`, { method: 'DELETE' })
      if (!res.ok) throw new Error(`Failed with status ${res.status}`)
      setItems(p => p.filter(s => s.id !== id && s._id !== id))
    } catch (err) { alert(err.message || 'Failed to delete') }
  }

  return (
    <PageWrap title="Students" subtitle="Manage student records for CIA exam allocation." loading={loading} error={error} onRefresh={refresh}>
      <div className="form-card">
        <h3 className="form-card-title">Add New Student</h3>
        <form className="inline-form" onSubmit={handleSubmit}>
          <Field label="USN"><input name="usn" value={form.usn} onChange={handleChange} required maxLength={10} placeholder="e.g. 1MS22CS001" /></Field>
          <Field label="Full Name"><input name="name" value={form.name} onChange={handleChange} required placeholder="Student name" /></Field>
          <Field label="Semester"><input name="semester" type="number" min="1" max="8" value={form.semester} onChange={handleChange} required placeholder="1–8" /></Field>
          <Field label="Department"><input name="department" value={form.department} onChange={handleChange} required placeholder="e.g. CSE" /></Field>
          <button type="submit" className="submit-btn" disabled={saving}>{saving ? 'Adding…' : '+ Add Student'}</button>
        </form>
      </div>
      <div className="list-section">
        <div className="list-head">
          <h3 className="list-title">All Students</h3>
          <span className="count-chip">{items.length} records</span>
        </div>
        <table className="data-table">
          <thead><tr><th>USN</th><th>Name</th><th>Semester</th><th>Department</th><th /></tr></thead>
          <tbody>
            {items.length === 0
              ? <EmptyRow msg="No students added yet. Use the form above to add one." />
              : items.map(s => (
                <tr key={s.id || s._id}>
                  <td className="mono">{s.usn}</td>
                  <td>{s.name}</td>
                  <td><span className="chip">Sem {s.semester}</span></td>
                  <td>{s.department}</td>
                  <td><button className="del-btn" onClick={() => handleDelete(s.id || s._id)}>Delete</button></td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </PageWrap>
  )
}

// ─── Staff ────────────────────────────────────────────────────────────────────
function StaffPage() {
  const { items, setItems, loading, error, refresh } = useApiList(`${API_BASE_URL}/api/staff/`)
  const [form, setForm]     = useState({ name: '', department: '', designation: '', isAvailable: true })
  const [saving, setSaving] = useState(false)

  const handleChange = e => {
    const { name, value, type, checked } = e.target
    setForm(p => ({ ...p, [name]: type === 'checkbox' ? checked : value }))
  }

  const handleSubmit = async e => {
    e.preventDefault(); setSaving(true)
    try {
      const res = await fetch(`${API_BASE_URL}/api/staff/`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: form.name.trim(), department: form.department.trim(), designation: form.designation.trim(), isAvailable: Boolean(form.isAvailable) }),
      })
      if (!res.ok) throw new Error(`Failed with status ${res.status}`)
      const json = await res.json()
      setItems(p => [...p, json?.data || json])
      setForm({ name: '', department: '', designation: '', isAvailable: true })
    } catch (err) { alert(err.message || 'Failed to create staff') }
    finally { setSaving(false) }
  }

  const handleDelete = async id => {
    if (!confirm('Delete this staff member?')) return
    try {
      const res = await fetch(`${API_BASE_URL}/api/staff/${id}`, { method: 'DELETE' })
      if (!res.ok) throw new Error(`Failed with status ${res.status}`)
      setItems(p => p.filter(s => s.id !== id && s._id !== id))
    } catch (err) { alert(err.message || 'Failed to delete') }
  }

  return (
    <PageWrap title="Staff" subtitle="Register invigilators and manage their availability." loading={loading} error={error} onRefresh={refresh}>
      <div className="form-card">
        <h3 className="form-card-title">Add New Staff Member</h3>
        <form className="inline-form" onSubmit={handleSubmit}>
          <Field label="Full Name"><input name="name" value={form.name} onChange={handleChange} required placeholder="Staff name" /></Field>
          <Field label="Department"><input name="department" value={form.department} onChange={handleChange} required placeholder="e.g. CSE" /></Field>
          <Field label="Designation"><input name="designation" value={form.designation} onChange={handleChange} required placeholder="e.g. Professor" /></Field>
          <Field label="Availability">
            <label className="toggle">
              <input type="checkbox" name="isAvailable" checked={form.isAvailable} onChange={handleChange} />
              <span className="toggle-track" />
              <span className="toggle-txt">{form.isAvailable ? 'Available for invigilation' : 'Not available'}</span>
            </label>
          </Field>
          <button type="submit" className="submit-btn" disabled={saving}>{saving ? 'Adding…' : '+ Add Staff'}</button>
        </form>
      </div>
      <div className="list-section">
        <div className="list-head">
          <h3 className="list-title">All Staff</h3>
          <span className="count-chip">{items.length} records</span>
        </div>
        <table className="data-table">
          <thead><tr><th>Name</th><th>Department</th><th>Designation</th><th>Availability</th><th /></tr></thead>
          <tbody>
            {items.length === 0
              ? <EmptyRow msg="No staff added yet. Use the form above." />
              : items.map(s => (
                <tr key={s.id || s._id}>
                  <td>{s.name}</td>
                  <td>{s.department}</td>
                  <td>{s.designation}</td>
                  <td><span className={`avail-chip ${s.isAvailable ? 'yes' : 'no'}`}>{s.isAvailable ? 'Available' : 'Unavailable'}</span></td>
                  <td><button className="del-btn" onClick={() => handleDelete(s.id || s._id)}>Delete</button></td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </PageWrap>
  )
}

// ─── Classrooms ───────────────────────────────────────────────────────────────
function ClassroomsPage() {
  const { items, setItems, loading, error, refresh } = useApiList(`${API_BASE_URL}/api/classrooms/`)
  const [form, setForm]     = useState({ roomNumber: '', block: '', capacity: '' })
  const [saving, setSaving] = useState(false)

  const handleChange = e => setForm(p => ({ ...p, [e.target.name]: e.target.value }))

  const handleSubmit = async e => {
    e.preventDefault(); setSaving(true)
    try {
      const res = await fetch(`${API_BASE_URL}/api/classrooms/`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ roomNumber: form.roomNumber.trim(), block: form.block.trim(), capacity: Number(form.capacity) }),
      })
      if (!res.ok) throw new Error(`Failed with status ${res.status}`)
      const json = await res.json()
      setItems(p => [...p, json?.data || json])
      setForm({ roomNumber: '', block: '', capacity: '' })
    } catch (err) { alert(err.message || 'Failed to create classroom') }
    finally { setSaving(false) }
  }

  const handleDelete = async id => {
    if (!confirm('Delete this classroom?')) return
    try {
      const res = await fetch(`${API_BASE_URL}/api/classrooms/${id}`, { method: 'DELETE' })
      if (!res.ok) throw new Error(`Failed with status ${res.status}`)
      setItems(p => p.filter(c => c.id !== id && c._id !== id))
    } catch (err) { alert(err.message || 'Failed to delete') }
  }

  return (
    <PageWrap title="Classrooms" subtitle="Add exam venues with their block and seating capacity." loading={loading} error={error} onRefresh={refresh}>
      <div className="form-card">
        <h3 className="form-card-title">Add New Classroom</h3>
        <form className="inline-form" onSubmit={handleSubmit}>
          <Field label="Room Number"><input name="roomNumber" value={form.roomNumber} onChange={handleChange} required placeholder="e.g. 101" /></Field>
          <Field label="Block"><input name="block" value={form.block} onChange={handleChange} required placeholder="e.g. A" /></Field>
          <Field label="Capacity"><input name="capacity" type="number" min="1" value={form.capacity} onChange={handleChange} required placeholder="e.g. 60" /></Field>
          <button type="submit" className="submit-btn" disabled={saving}>{saving ? 'Adding…' : '+ Add Classroom'}</button>
        </form>
      </div>
      <div className="list-section">
        <div className="list-head">
          <h3 className="list-title">All Classrooms</h3>
          <span className="count-chip">{items.length} records</span>
        </div>
        <table className="data-table">
          <thead><tr><th>Room</th><th>Block</th><th>Capacity</th><th /></tr></thead>
          <tbody>
            {items.length === 0
              ? <EmptyRow msg="No classrooms added yet. Use the form above." />
              : items.map(c => (
                <tr key={c.id || c._id}>
                  <td className="mono">{c.roomNumber}</td>
                  <td>{c.block}</td>
                  <td>{c.capacity} seats</td>
                  <td><button className="del-btn" onClick={() => handleDelete(c.id || c._id)}>Delete</button></td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </PageWrap>
  )
}

// ─── Exams ────────────────────────────────────────────────────────────────────
function ExamsPage() {
  const { items, setItems, loading, error, refresh } = useApiList(`${API_BASE_URL}/api/exams/`)
  const [form, setForm]     = useState({ examName: '', date: '', semester: '' })
  const [saving, setSaving] = useState(false)

  const handleChange = e => setForm(p => ({ ...p, [e.target.name]: e.target.value }))

  const handleSubmit = async e => {
    e.preventDefault(); setSaving(true)
    try {
      const res = await fetch(`${API_BASE_URL}/api/exams/`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ examName: form.examName.trim(), date: form.date, semester: Number(form.semester) }),
      })
      if (!res.ok) throw new Error(`Failed with status ${res.status}`)
      const json = await res.json()
      setItems(p => [...p, json?.data || json])
      setForm({ examName: '', date: '', semester: '' })
    } catch (err) { alert(err.message || 'Failed to create exam') }
    finally { setSaving(false) }
  }

  const handleDelete = async id => {
    if (!confirm('Delete this exam?')) return
    try {
      const res = await fetch(`${API_BASE_URL}/api/exams/${id}`, { method: 'DELETE' })
      if (!res.ok) throw new Error(`Failed with status ${res.status}`)
      setItems(p => p.filter(e => e.id !== id && e._id !== id))
    } catch (err) { alert(err.message || 'Failed to delete') }
  }

  return (
    <PageWrap title="Exams" subtitle="Schedule CIA exam sessions by semester and date." loading={loading} error={error} onRefresh={refresh}>
      <div className="form-card">
        <h3 className="form-card-title">Schedule New Exam</h3>
        <form className="inline-form" onSubmit={handleSubmit}>
          <Field label="Exam Name"><input name="examName" value={form.examName} onChange={handleChange} required placeholder="e.g. CIA 1 – Data Structures" /></Field>
          <Field label="Date &amp; Time"><input type="datetime-local" name="date" value={form.date} onChange={handleChange} required /></Field>
          <Field label="Semester"><input name="semester" type="number" min="1" max="8" value={form.semester} onChange={handleChange} required placeholder="1–8" /></Field>
          <button type="submit" className="submit-btn" disabled={saving}>{saving ? 'Saving…' : '+ Schedule Exam'}</button>
        </form>
      </div>
      <div className="list-section">
        <div className="list-head">
          <h3 className="list-title">All Exams</h3>
          <span className="count-chip">{items.length} records</span>
        </div>
        <table className="data-table">
          <thead><tr><th>Exam Name</th><th>Date &amp; Time</th><th>Semester</th><th /></tr></thead>
          <tbody>
            {items.length === 0
              ? <EmptyRow msg="No exams scheduled yet. Use the form above." />
              : items.map(e => (
                <tr key={e.id || e._id}>
                  <td>{e.examName}</td>
                  <td className="date-td">{new Date(e.date).toLocaleString()}</td>
                  <td><span className="chip">Sem {e.semester}</span></td>
                  <td><button className="del-btn" onClick={() => handleDelete(e.id || e._id)}>Delete</button></td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </PageWrap>
  )
}

// ─── Allocations ──────────────────────────────────────────────────────────────
function AllocationsPage() {
  const { items, setItems, loading, error, refresh } = useApiList(`${API_BASE_URL}/api/allocations/`)
  const [exams, setExams]               = useState([])
  const [selectedExam, setSelectedExam] = useState('')
  const [generating, setGenerating]     = useState(false)
  const [viewExamId, setViewExamId]     = useState(null)
  const [viewData, setViewData]         = useState(null)
  const [viewLoading, setViewLoading]   = useState(false)

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/exams/`)
      .then(r => r.json())
      .then(data => setExams(Array.isArray(data) ? data : Array.isArray(data?.data) ? data.data : []))
      .catch(() => {})
  }, [])

  const handleGenerate = async () => {
    if (!selectedExam) { alert('Please select an exam first.'); return }
    setGenerating(true)
    try {
      const res = await fetch(`${API_BASE_URL}/api/allocations/generate/${selectedExam}`, { method: 'POST' })
      if (!res.ok) { const txt = await res.text(); throw new Error(`Failed with status ${res.status}: ${txt}`) }
      const json = await res.json()
      setItems(p => [...p, json?.data || json])
      await refresh()
      alert('Allocation generated successfully.')
    } catch (err) { alert(err.message || 'Failed to generate allocation') }
    finally { setGenerating(false) }
  }

  const handleDelete = async id => {
    if (!confirm('Delete this allocation?')) return
    try {
      const res = await fetch(`${API_BASE_URL}/api/allocations/${id}`, { method: 'DELETE' })
      if (!res.ok) throw new Error(`Failed with status ${res.status}`)
      setItems(p => p.filter(a => a.id !== id && a._id !== id))
    } catch (err) { alert(err.message || 'Failed to delete') }
  }

  const openView = async examId => {
    setViewExamId(examId); setViewData(null); setViewLoading(true)
    try {
      const res  = await fetch(`${API_BASE_URL}/api/allocations/exam/${examId}`)
      if (!res.ok) throw new Error(`Failed with status ${res.status}`)
      const data = await res.json()
      setViewData(data?.data || data)
    } catch (err) { alert(err.message || 'Failed to fetch allocation details') }
    finally { setViewLoading(false) }
  }

  return (
    <PageWrap title="Allocations" subtitle="Generate seating plans and invigilator assignments for CIA exams." loading={loading} error={error} onRefresh={refresh}>
      <div className="form-card">
        <h3 className="form-card-title">Generate Allocation</h3>
        <p className="form-card-desc">Select a scheduled exam to auto-generate department-mixed seating and assign invigilators to each room.</p>
        <form className="inline-form" onSubmit={e => { e.preventDefault(); handleGenerate() }}>
          <Field label="Select Exam">
            <select value={selectedExam} onChange={e => setSelectedExam(e.target.value)}>
              <option value="">Choose an exam…</option>
              {exams.map(e => (
                <option key={e.id || e._id} value={e.id || e._id}>
                  {e.examName} — Sem {e.semester} · {new Date(e.date).toLocaleDateString()}
                </option>
              ))}
            </select>
          </Field>
          <button type="submit" className="submit-btn generate-btn" disabled={generating || !selectedExam}>
            {generating ? 'Generating…' : '⚡ Generate Allocation'}
          </button>
        </form>
      </div>

      <div className="list-section">
        <div className="list-head">
          <h3 className="list-title">All Allocations</h3>
          <span className="count-chip">{items.length} records</span>
        </div>
        <table className="data-table">
          <thead><tr><th>Exam</th><th>Semester</th><th>Created At</th><th /></tr></thead>
          <tbody>
            {items.length === 0
              ? <EmptyRow msg="No allocations yet. Generate one using the form above." />
              : items.map(a => (
                <tr key={a.id || a._id}>
                  <td>{a.examId?.examName || '—'}</td>
                  <td>{a.examId?.semester != null ? <span className="chip">Sem {a.examId.semester}</span> : '—'}</td>
                  <td className="date-td">{a.createdAt ? new Date(a.createdAt).toLocaleString() : '—'}</td>
                  <td>
                    <div className="row-actions">
                      <button className="view-btn" onClick={() => openView(a.examId?._id || a.examId || a.exam_id)}>View</button>
                      <button className="del-btn"  onClick={() => handleDelete(a.id || a._id)}>Delete</button>
                    </div>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      {viewExamId && (
        <div className="drawer-overlay" onClick={e => { if (e.target === e.currentTarget) { setViewExamId(null); setViewData(null) } }}>
          <div className="drawer-panel">
            <div className="drawer-top">
              <h3 className="drawer-heading">Allocation Details</h3>
              <button className="drawer-close" onClick={() => { setViewExamId(null); setViewData(null) }}>✕</button>
            </div>
            <div className="drawer-scroll">
              {viewLoading && <div className="loader-bar"><div className="loader-fill" /></div>}
              {!viewLoading && viewData && (
                <>
                  <div className="drawer-exam-info">
                    <p className="dei-name">{viewData.examId?.examName || 'Unnamed exam'}</p>
                    {viewData.examId?.semester != null && <span className="chip">Semester {viewData.examId.semester}</span>}
                    {viewData.examId?.date && <p className="dei-date">{new Date(viewData.examId.date).toLocaleString()}</p>}
                  </div>

                  {Array.isArray(viewData.roomAllocations) && viewData.roomAllocations.length > 0 ? (
                    <>
                      <div className="drawer-summary">
                        <div className="ds-stat">
                          <span className="ds-num">{viewData.roomAllocations.length}</span>
                          <span className="ds-lbl">Rooms used</span>
                        </div>
                        <div className="ds-stat">
                          <span className="ds-num">{viewData.roomAllocations.reduce((s, ra) => s + (ra.studentsAssigned?.length || 0), 0)}</span>
                          <span className="ds-lbl">Students assigned</span>
                        </div>
                      </div>
                      {viewData.roomAllocations.map((ra, idx) => (
                        <div className="room-block" key={ra._id || idx}>
                          <div className="rb-head">
                            <span className="rb-room">Room {ra.room?.roomNumber || '—'}{ra.room?.block && ` · Block ${ra.room.block}`}</span>
                            <span className="rb-count">{ra.studentsAssigned?.length || 0} students</span>
                          </div>
                          {ra.staffAssigned?.length > 0 && (
                            <p className="rb-staff">Invigilators: {ra.staffAssigned.map(st => st.name).join(', ')}</p>
                          )}
                          {ra.studentsAssigned?.length > 0
                            ? (
                              <table className="data-table drawer-table">
                                <thead><tr><th>USN</th><th>Name</th><th>Dept</th><th>Sem</th></tr></thead>
                                <tbody>
                                  {ra.studentsAssigned.map(s => (
                                    <tr key={s._id || s.usn}>
                                      <td className="mono">{s.usn}</td>
                                      <td>{s.name}</td>
                                      <td>{s.department}</td>
                                      <td>{s.semester}</td>
                                    </tr>
                                  ))}
                                </tbody>
                              </table>
                            )
                            : <p className="muted-sm">No students in this room.</p>
                          }
                        </div>
                      ))}
                    </>
                  ) : <p className="muted-sm">No room allocations found for this exam.</p>}
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </PageWrap>
  )
}

export default App