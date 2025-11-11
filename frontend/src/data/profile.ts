export const profile = {
  name: 'Ryley Hynes',
  title: 'Full‑Stack Application Engineer',
  location: 'Nashville, TN',
  email: 'RyleyHynes@gmail.com',
  phone: '(518) 813‑2692',
  github: 'https://github.com/RyleyHynes',
  linkedin: 'https://www.linkedin.com/in/ryleyhynes',
  summary:
    'Full-stack engineer crafting reliable, human-centered web applications.I build modern React + TypeScript frontends and resilient backend APIs with Django and .NET — focused on clean architecture, accessible design, and code that teams love to maintain.',
}

export const skills = {
  frontend: ['TypeScript','React','Redux','RTK Query','HTML5','CSS3','SCSS','Bootstrap','Figma','Neutron DS'],
  backend: ['C#','.NET','Python','Django','SQL','CosmosDB','REST','Swagger/OpenAPI'],
  qa: ['Vitest','Jest','React Testing Library','Postman'],
  devops: ['Azure DevOps','Git','GitHub'],
  gis: ['ArcGIS','Survey123'],
}

export type ExperienceRole = {
  title: string;
  range: string;
  blurb?: string;
  bullets?: string[];
};

export type ExperienceCompany = {
  company: string;
  location: string;
  roles: ExperienceRole[];
};

export const experience: ExperienceCompany[] = [
  {
    company: 'HCA Healthcare',
    location: 'Nashville, TN',
    roles: [
      {
        title: 'Application Engineer II',
        range: 'Nov 2024 – Present',
        blurb:
          'Full-stack delivery across React/TypeScript and Django REST, from data models to accessible, responsive UI.',
        bullets: [
          'Designed authenticated CRUD features and integrated REST endpoints.',
          'Raised test coverage with Jest/RTL; mentored juniors via reviews/pairing.',
          'Partnered with product/QA to ship reliable, patient-facing workflows.',
        ],
      },
      {
        title: 'Application Engineer I',
        range: 'Sep 2023 – Nov 2024',
        blurb:
          'Shipped cross-stack features, expanding from front-end into backend APIs and service logic.',
        bullets: [
          'Built React features with RTK Query; validated APIs with Swagger/Postman.',
          'Assisted C#/.NET and Django endpoints; supported incident response.',
          'Contributed to planning/reviews to reduce regressions and improve flow.',
        ],
      },
      {
        title: 'Technical Resident Application Engineer',
        range: 'Jan 2023 – Sep 2023',
        blurb:
          'Enterprise UI foundations using React + TypeScript and the Neutron design system.',
        bullets: [
          'Implemented accessible components and responsive layouts.',
          'Translated Figma into production UI; supported CI/CD in Azure DevOps.',
          'Collaborated with QA through manual testing and bug triage.',
        ],
      },
    ],
  },
];

export const education = [
  { school: 'Nashville Software School', detail: 'Full‑Stack Web Development Certificate', range: 'Apr 2022 – Sep 2022' },
  { school: 'University of Tennessee, Knoxville', detail: 'B.S. Environmental & Soil Science, Minor in Watershed', range: 'Aug 2017 – Aug 2019' },
]


// Reuse the same stack for all apps
export const STACK = ['TypeScript', 'React', 'SCSS', 'Python/Django', 'SQLite'] as const;

export const projects = [
  {
    name: 'Peak Planner',
    blurb:
      'Plan alpine trips with routes, gear, partners, and weather windows. Full CRUD with auth and a clean, fast UI.',
    features: [
      'Trips, routes, waypoints, partners (CRUD)',
      'Gear lists + packing presets',
      'Search, filters, pagination'
    ],
    links: [
      { label: 'Launch App', href: '/apps/peak-planner' },
      { label: 'API Docs', href: '/api/peak-planner/schema/swagger-ui/' },
      { label: 'Repository', href: 'https://github.com/RyleyHynes/hynes-fullstack-portfolio' }
    ],
    stack: STACK
  },
  {
    name: 'Route Log',
    blurb:
      'Personal climbing logbook with grades, styles, notes, and media. Analyze progress over time.',
    features: [
      'Areas, routes, ascents, partners (CRUD)',
      'Filters, sorting, and route tagging',
      'CSV import (bulk adds)'
    ],
    links: [
      { label: 'Launch App', href: '/apps/route-log' },
      { label: 'API Docs', href: '/api/route-log/schema/swagger-ui/' },
      { label: 'Repository', href: 'https://github.com/RyleyHynes/hynes-fullstack-portfolio' }
    ],
    stack: STACK
  },
  {
    name: 'Trail Supply',
    blurb:
      'Inventory + orders for outdoor gear. Track products, suppliers, purchase orders, and fulfillment.',
    features: [
      'Products, SKUs, suppliers, orders (CRUD)',
      'Stock levels + low-inventory view',
      'CSV export for admin ops'
    ],
    links: [
      { label: 'Launch App', href: '/apps/trail-supply' },
      { label: 'API Docs', href: '/api/trail-supply/schema/swagger-ui/' },
      { label: 'Repository', href: 'https://github.com/RyleyHynes/hynes-fullstack-portfolio' }
    ],
    stack: STACK
  }
] as const;
