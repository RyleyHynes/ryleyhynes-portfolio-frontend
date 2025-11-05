import { projects } from '@/data/profile'

export default function Projects() {
  return (
    <section className="grid gap-6">
      <header>
        <h2 className="section-title">Selected Projects</h2>
        <p className="text-slate-600 dark:text-slate-300 mt-2 max-w-2xl">Impact‑focused work spanning UI engineering, design systems, and reliability tooling.</p>
      </header>

      <div className="grid md:grid-cols-2 gap-6">
        {projects.map(p => (
          <article key={p.name} className="card p-6">
            <div className="flex items-start justify-between gap-4">
              <h3 className="text-xl font-semibold">{p.name}</h3>
              <div className="flex gap-2">
                {p.links.map(l => <a key={l.label} className="navlink" href={l.href}>{l.label}</a>)}
              </div>
            </div>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">{p.blurb}</p>
            <ul className="mt-3 flex flex-wrap gap-2">
              {p.stack.map(s => <li key={s} className="badge">{s}</li>)}
            </ul>
            {p.metrics?.length ? (
              <ul className="mt-4 grid grid-cols-3 gap-2 text-center">
                {p.metrics.map(m => (
                  <li key={m} className="rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-200/60 dark:border-slate-800 p-3 text-xs font-medium">{m}</li>
                ))}
              </ul>
            ) : null}
          </article>
        ))}
      </div>
    </section>
  )
}
