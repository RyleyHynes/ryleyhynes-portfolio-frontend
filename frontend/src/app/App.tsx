import { useEffect, useMemo, useState } from 'react'
import { Routes, Route, NavLink, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Moon, Sun, Github, Linkedin, Mail, MapPin } from 'lucide-react'
import { profile } from '@/data/profile'
import Home from '@/pages/Home'
import Projects from '@/pages/Projects'
import About from '@/pages/About'
import SkillsExperience from '@/pages/SkillsExperience'
import Contact from '@/pages/Contact'

function useDarkMode() {
  const [enabled, setEnabled] = useState(() => window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)
  useEffect(() => {
    const root = document.documentElement
    if (enabled) root.classList.add('dark')
    else root.classList.remove('dark')
  }, [enabled])
  return { enabled, setEnabled }
}

const Page = ({ children }: { children: React.ReactNode }) => (
  <motion.main
    initial={{ opacity: 0, y: 8 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -8 }}
    transition={{ type: 'spring', stiffness: 90, damping: 16, mass: .6 }}
    className="container-padded py-10 sm:py-14"
  >
    {children}
  </motion.main>
)

export default function App() {
  const { enabled, setEnabled } = useDarkMode()
  const location = useLocation()

  const nav = useMemo(() => ([
    { to: '/', label: 'Home' },
    { to: '/projects', label: 'Projects' },
    { to: '/about', label: 'About' },
    { to: '/skills-experience', label: 'Skills & Experience' },
    { to: '/contact', label: 'Contact' },
  ]), [])

  return (
    <div>
      <a href="#content" className="a11y-skiplink">Skip to content</a>
      <header className="sticky top-0 z-40 backdrop-blur border-b border-slate-200/60 dark:border-slate-800 bg-white/70 dark:bg-slate-950/40">
        <div className="container-padded flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-xl bg-brand-600 text-white grid place-items-center font-bold">RH</div>
            <div className="leading-tight">
              <div className="font-bold">{profile.name}</div>
              <div className="text-xs text-slate-500 dark:text-slate-400">{profile.title}</div>
            </div>
          </div>
          <nav className="hidden md:flex items-center gap-6">
            {nav.map(item => (
              <NavLink key={item.to} to={item.to} className={({isActive}) => `navlink ${isActive ? 'text-brand-600 dark:text-brand-400' : ''}`}>{item.label}</NavLink>
            ))}
          </nav>
          <div className="flex items-center gap-2">
            <a className="btn-ghost" href={profile.github} target="_blank" rel="noreferrer" aria-label="GitHub"><Github size={18} /></a>
            <a className="btn-ghost" href={profile.linkedin} target="_blank" rel="noreferrer" aria-label="LinkedIn"><Linkedin size={18} /></a>
            <button className="btn-ghost" onClick={() => setEnabled(!enabled)} aria-label="Toggle dark mode">
              {enabled ? <Sun size={18} /> : <Moon size={18} />}
            </button>
          </div>
        </div>
      </header>

      <AnimatePresence mode="wait">
        <Page key={location.pathname}>
          <div id="content" />
          <Routes location={location}>
            <Route path="/" element={<Home />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/about" element={<About />} />
            <Route path="/skills-experience" element={<SkillsExperience />} />
            <Route path="/contact" element={<Contact />} />
          </Routes>
        </Page>
      </AnimatePresence>

      <footer className="border-t border-slate-200/60 dark:border-slate-800 py-8">
        <div className="container-padded text-sm text-slate-500 dark:text-slate-400 flex flex-col sm:flex-row gap-3 sm:items-center justify-between">
          <div className="flex items-center gap-2"><MapPin size={16}/>{profile.location}</div>
          <div className="flex items-center gap-4">
            <a className="navlink" href={`mailto:${profile.email}`}><Mail className="inline-block mr-1" size={16}/> {profile.email}</a>
            <a className="navlink" href={profile.github} target="_blank" rel="noreferrer">GitHub</a>
            <a className="navlink" href={profile.linkedin} target="_blank" rel="noreferrer">LinkedIn</a>
          </div>
        </div>
      </footer>
    </div>
  )
}
