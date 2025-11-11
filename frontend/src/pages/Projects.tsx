import { Link } from 'react-router-dom'
import { projects } from '@/data/profile'

export default function Projects() {
  return (
    <section className="grid gap-6">
      <header>
        <h2 className="section-title">Selected Projects</h2>
        <p className="text-slate-600 dark:text-slate-300 mt-2 max-w-2xl">End-to-end CRUD applications demonstrating full-stack proficiency across React, TypeScript, Django REST Framework, and relational data modeling.</p>
      </header>

      <div className="grid md:grid-cols-2 gap-6">
        {projects.map(p => {
          const disabled = p.comingSoon
          const cardClasses = [
            'card',
            'p-6',
            'text-slate-900',
            'dark:text-slate-100',
            disabled ? 'card-coming-soon' : '',
          ]

          return (
            <article
              key={p.name}
              className={cardClasses.filter(Boolean).join(' ')}
              aria-disabled={disabled || undefined}
              title={disabled ? 'Live demo coming soon' : undefined}
            >
            <div className="flex items-start justify-between gap-4">
              <h3 className="text-xl font-semibold">{p.name}</h3>
              <div className="flex gap-2">
                {p.links.map(l => {
                  if (disabled) {
                    return (
                      <span
                        key={l.label}
                        className="navlink opacity-60 pointer-events-none select-none"
                        aria-disabled="true"
                      >
                        {l.label}
                      </span>
                    )
                  }

                  if (l.internal) {
                    return (
                      <Link key={l.label} className="navlink font-semibold" to={l.href}>
                        {l.label}
                      </Link>
                    )
                  }

                  return (
                    <a
                      key={l.label}
                      className="navlink"
                      href={l.href}
                      target="_blank"
                      rel="noreferrer"
                    >
                      {l.label}
                    </a>
                  )
                })}
              </div>
            </div>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-200">{p.blurb}</p>
            <ul className="mt-3 flex flex-wrap gap-2">
              {p.stack.map(s => <li key={s} className="badge">{s}</li>)}
            </ul>
          </article>
          )
        })}
      </div>
    </section>
  )
}
