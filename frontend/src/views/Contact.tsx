import { useState } from 'react'
import { profile } from '@/data/profile'

export default function Contact() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [msg, setMsg] = useState('')
  const valid = name.trim().length > 1 && /.+@.+\..+/.test(email) && msg.trim().length > 4

  return (
    <section className="grid gap-8 max-w-xl">
      <header>
        <h2 className="section-title">Contact</h2>
        <p className="mt-2 text-slate-600 dark:text-slate-300">Want to collaborate or chat? Email is best.</p>
      </header>

      <form
        onSubmit={(e) => { e.preventDefault(); window.location.href = `mailto:${profile.email}?subject=Portfolio%20Inquiry%20from%20${encodeURIComponent(name)}&body=${encodeURIComponent(msg + '\n\nFrom: ' + email)}` }}
        className="card p-6 grid gap-4"
      >
        <label className="grid gap-1 text-sm">
          <span>Name</span>
          <input className="border rounded-xl px-3 py-2 bg-white/80 dark:bg-slate-950/60" value={name} onChange={e=>setName(e.target.value)} required />
        </label>
        <label className="grid gap-1 text-sm">
          <span>Email</span>
          <input type="email" className="border rounded-xl px-3 py-2 bg-white/80 dark:bg-slate-950/60" value={email} onChange={e=>setEmail(e.target.value)} required />
        </label>
        <label className="grid gap-1 text-sm">
          <span>Message</span>
          <textarea className="border rounded-xl px-3 py-2 min-h-[140px] bg-white/80 dark:bg-slate-950/60" value={msg} onChange={e=>setMsg(e.target.value)} required />
        </label>
        <button className="btn-primary disabled:opacity-50" disabled={!valid}>Send Email</button>
      </form>

      <div className="text-sm text-slate-600 dark:text-slate-300">
        Or reach out directly: <a className="navlink" href={`mailto:${profile.email}`}>{profile.email}</a> • <a className="navlink" href={profile.linkedin} target="_blank" rel="noreferrer">LinkedIn</a>
      </div>
    </section>
  )
}
