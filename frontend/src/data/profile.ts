export const profile = {
  name: 'Ryley Hynes',
  title: 'Full‑Stack Application Engineer',
  location: 'Nashville, TN',
  email: 'RyleyHynes@gmail.com',
  phone: '(518) 813‑2692',
  github: 'https://github.com/RyleyHynes',
  linkedin: 'https://www.linkedin.com/in/ryleyhynes',
  summary:
    'Engineer focused on reliable, accessible healthcare software. React + TypeScript on the frontend, C#/.NET on the backend, with an eye for DX, testing, and resilient systems.',
}

export const skills = {
  frontend: ['TypeScript','React','Redux','RTK Query','HTML5','CSS3','SCSS','Bootstrap','Figma','Neutron DS'],
  backend: ['C#','.NET','Python','Django','SQL','CosmosDB','REST','Swagger/OpenAPI'],
  qa: ['Vitest','Jest','React Testing Library','Postman'],
  devops: ['Azure DevOps','Git','GitHub'],
  gis: ['ArcGIS','Survey123'],
}

export const experience = [
  {
    company: 'HCA Healthcare',
    location: 'Nashville, TN',
    roles: [
      { title: 'Application Engineer 2', range: 'Nov 2024 – Present' },
      { title: 'Application Engineer 1', range: 'Sep 2023 – Nov 2024' },
      { title: 'Technical Resident Application Engineer', range: 'Jan 2023 – Sep 2023' }
    ],
    highlights: [
      'Owned delivery of frontend features across multiple healthcare apps using Redux, RTK Query, and REST APIs.',
      'Expanded into backend development with C#/.NET implementing internal APIs and service logic.',
      'Validated APIs with Postman and supported cross‑stack debugging to improve release stability.',
      'Participated in on‑call rotations for incident triage, reducing downtime and improving reliability.',
      'Contributed to backlog grooming and sprint reviews to align engineering, QA, and product.',
      'Built accessible, responsive interfaces; enhanced shared components using Neutron DS.',
      'Paired with designers in Figma to deliver production‑ready UI; supported CI/CD in Azure DevOps.',
      'Added unit/integration coverage (Vitest/Jest/RTL); mentored juniors via reviews and pairing.'
    ],
  },
]

export const education = [
  { school: 'Nashville Software School', detail: 'Full‑Stack Web Development Certificate', range: 'Apr 2022 – Sep 2022' },
  { school: 'University of Tennessee, Knoxville', detail: 'B.S. Environmental & Soil Science, Minor in Watershed', range: 'Aug 2017 – Aug 2019' },
]

export const projects = [
  {
    name: 'Surgical Symphony — Frontend Rebuild',
    blurb: 'Refactored complex surgical workflow UI into modular React + TS with RTK Query, improving load time and reliability.',
    metrics: ['‑38% bundle size','+27% faster median render','A11y score 100'],
    links: [
      { label: 'Case Study', href: '#projects' },
    ],
    stack: ['React','TypeScript','RTK Query','C#/.NET (APIs)','Jest','RTL']
  },
  {
    name: 'Neutron Component Library Enhancements',
    blurb: 'Extended HCA design system components and tokens, accelerating feature delivery across teams.',
    metrics: ['15+ shared components','Design tokens v2','Docs site PRs'],
    links: [ { label: 'Notes', href: '#projects' }],
    stack: ['Design Tokens','Storybook','Figma','SCSS']
  },
  {
    name: 'Incident Triage Dashboard',
    blurb: 'Built on‑call dashboard for incident triage with filtering, timelines, and Postman‑validated API surfaces.',
    metrics: ['‑20% MTTR (in pilot)','On‑call QoL ↑'],
    links: [ { label: 'Overview', href: '#projects' }],
    stack: ['React','TypeScript','REST','Azure DevOps']
  }
]
