import { skills, experience } from '@/data/profile'

function Pill({ children }: { children: React.ReactNode }) {
  return <span className="badge">{children}</span>
}

export default function SkillsExperience() {
  return (
    <section className="grid gap-8 text-slate-900 dark:text-slate-100">
      <header>
        <h2 className="section-title">Skills & Experience</h2>
        <p className="mt-2 text-slate-600 dark:text-slate-300 max-w-2xl">Full-stack engineer with a strong UI foundation — building accessible, tested, and maintainable applications through close collaboration across design and backend teams.</p>
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

      {experience.map((co) => (
        <article
          key={co.company}
          className="rounded-2xl border border-slate-900 dark:border-slate-800 p-6 bg-white/60 dark:bg-slate-900/60 shadow-sm"
        >
          {/* Company header */}
          <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
            <div>
              <div className="font-semibold text-base">{co.company}</div>
              <div className="text-xs text-slate-500 dark:text-slate-400">
                {co.location}
              </div>
            </div>
          </header>

          {/* Detailed roles (expand/collapse per role) */}
          <div className="mt-4 grid">
            {co.roles.map((r, idx) => (
              <details
                key={`${co.company}-${r.title}-details`}
                className="group border-t first:border-t-0 border-slate-200 dark:border-slate-800 py-4"
                open={idx === 0} // open the most recent by default
              >
                <summary className="cursor-pointer list-none flex items-start justify-between gap-3">
                  <div>
                    <div className="font-medium">
                      {r.title}{' '}
                      <span className="text-xs text-slate-500">
                        • {r.range}
                      </span>
                    </div>
                    {r.blurb && (
                      <p className="text-sm text-slate-600 dark:text-slate-300 mt-1">
                        {r.blurb}
                      </p>
                    )}
                  </div>
                  <span
                    aria-hidden
                    className="mt-1 text-slate-400 group-open:rotate-180 transition-transform"
                  >
                    ▾
                  </span>
                </summary>

                {r.bullets && r.bullets.length > 0 && (
                  <ul className="mt-3 grid gap-2 text-sm list-disc pl-5">
                    {r.bullets.map((b, i) => (
                      <li key={`${co.company}-${r.title}-b-${i}`}>{b}</li>
                    ))}
                  </ul>
                )}
              </details>
            ))}
          </div>
        </article>
      ))}
    </section>
    </section>
  )
}
