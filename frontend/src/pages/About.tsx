import { profile, education } from '@/data/profile'

export default function About() {
  return (
    <section className="grid gap-8 text-slate-900 dark:text-slate-100">
      <header className="max-w-3xl">
        <h2 className="section-title">About</h2>
        <p className="mt-3 text-slate-600 dark:text-slate-300">
          I build products that prioritize reliability, accessibility, and developer experience. My work spans
          React/TypeScript interfaces and C#/.NET services, with a background in environmental science that keeps me user‑ and impact‑oriented.
        </p>
      </header>

      <div className="grid sm:grid-cols-2 gap-6">
        <article className="card p-6">
          <h3 className="font-semibold">Quick facts</h3>
          <ul className="mt-3 space-y-2 text-sm">
            <li><b>Location:</b> {profile.location}</li>
            <li><b>Focus:</b> Frontend platforms, design systems, testing, reliability</li>
            <li><b>Interests:</b> Maps/GIS, healthcare, outdoor tech</li>
          </ul>
        </article>
        <article className="card p-6">
          <h3 className="font-semibold">Education</h3>
          <ul className="mt-3 space-y-3 text-sm">
            {education.map(e => (
              <li key={e.school}>
                <div className="font-medium">{e.school}</div>
                <div className="text-slate-600 dark:text-slate-300">{e.detail}</div>
                <div className="text-xs text-slate-500 dark:text-slate-400">{e.range}</div>
              </li>
            ))}
          </ul>
        </article>
      </div>
    </section>
  )
}
