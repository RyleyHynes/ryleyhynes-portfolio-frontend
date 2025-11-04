import { skills, experience } from '@/data/profile'

function Pill({ children }: { children: React.ReactNode }) {
  return <span className="badge">{children}</span>
}

export default function SkillsExperience() {
  return (
    <section className="grid gap-8">
      <header>
        <h2 className="section-title">Skills & Experience</h2>
        <p className="mt-2 text-slate-600 dark:text-slate-300 max-w-2xl">Breadth across the stack with a strong UI foundation.
        I value a11y, testing, and cross‑team collaboration.</p>
      </header>

      <div className="grid lg:grid-cols-3 gap-6">
        <article className="card p-6">
          <h3 className="font-semibold">Frontend</h3>
          <div className="mt-3 flex flex-wrap gap-2">{skills.frontend.map(s => <Pill key={s}>{s}</Pill>)}</div>
        </article>
        <article className="card p-6">
          <h3 className="font-semibold">Backend</h3>
          <div className="mt-3 flex flex-wrap gap-2">{skills.backend.map(s => <Pill key={s}>{s}</Pill>)}</div>
        </article>
        <article className="card p-6">
          <h3 className="font-semibold">QA & DevOps</h3>
          <div className="mt-3 flex flex-wrap gap-2">
            {[...skills.qa, ...skills.devops].map(s => <Pill key={s}>{s}</Pill>)}
          </div>
        </article>
      </div>

      <section className="grid gap-4">
        <h3 className="font-semibold text-lg">Experience</h3>
        <article className="card p-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
            <div>
              <div className="font-semibold">{experience[0].company}</div>
              <div className="text-xs text-slate-500 dark:text-slate-400">{experience[0].location}</div>
            </div>
            <ul className="text-sm text-slate-600 dark:text-slate-300">
              {experience[0].roles.map(r => (
                <li key={r.title}><b>{r.title}</b> — {r.range}</li>
              ))}
            </ul>
          </div>
          <ul className="mt-4 grid gap-2 text-sm list-disc pl-5">
            {experience[0].highlights.map(h => <li key={h}>{h}</li>)}
          </ul>
        </article>
      </section>
    </section>
  )
}
