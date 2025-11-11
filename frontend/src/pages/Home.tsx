import { motion } from 'framer-motion'
import { profile, projects } from '@/data/profile'
import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <section className="grid gap-8">
      <div className="card gradient-border p-8 text-slate-900 dark:text-slate-100">
        <h1 className="section-title">Building reliable software for healthcare & beyond</h1>
        <p className="mt-3 max-w-2xl text-slate-600 dark:text-slate-300">
          {profile.summary}
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link to="/projects" className="btn-primary">Explore Projects</Link>
          <Link to="/contact" className="btn-ghost">Contact</Link>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {projects.slice(0, 3).map((p, i) => {
          const disabled = p.comingSoon
          const launchLink = p.links.find(l => l.internal)
          const cardClasses = [
            'card',
            'p-6',
            'text-slate-900',
            'dark:text-slate-100',
            disabled ? 'card-coming-soon' : '',
          ]

          return (
            <motion.article
              key={p.name}
              className={cardClasses.filter(Boolean).join(' ')}
              aria-disabled={disabled || undefined}
              title={disabled ? 'Live demo coming soon' : undefined}
              initial={{ opacity: 0, y: 8 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: .2 }}
              transition={{ delay: i * .05 }}
            >
              <h3 className="font-semibold text-lg">{p.name}</h3>
              <p className="mt-2 text-sm text-slate-600 dark:text-slate-200">{p.blurb}</p>
              <div className="mt-3 flex flex-wrap gap-2">
                {p.stack.map(s => <span key={s} className="badge">{s}</span>)}
              </div>

              {!disabled && launchLink && (
                <div className="mt-4">
                  <Link
                    to={launchLink.href}
                    className="navlink font-semibold inline-flex items-center gap-1"
                  >
                    Launch App <span aria-hidden>↗</span>
                  </Link>
                </div>
              )}
            </motion.article>
          )
        })}
      </div>
    </section>
  )
}
