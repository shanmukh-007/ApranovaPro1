"use client"

import { useEffect, useState } from "react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { 
  ArrowRight, 
  CheckCircle2, 
  ExternalLink,
  Clock,
  Target,
  BookOpen
} from "lucide-react"
import Link from "next/link"
import apiClient from "@/lib/apiClient"

export default function ProjectGuideStaticPage() {
  const [userTrack, setUserTrack] = useState<'DP' | 'FSD' | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchUserData() {
      try {
        const response = await apiClient.get("/users/profile")
        setUserTrack(response.data.track)
      } catch (error) {
        console.error("Failed to fetch user data:", error)
      } finally {
        setLoading(false)
      }
    }
    fetchUserData()
  }, [])

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto space-y-6 animate-pulse">
        <div className="h-32 bg-slate-200 dark:bg-slate-800 rounded-lg"></div>
        <div className="h-96 bg-slate-200 dark:bg-slate-800 rounded-lg"></div>
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto space-y-12 pb-20">
      {/* Header */}
      <div className="space-y-4">
        <h1 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-slate-100">
          Project Guide
        </h1>
        <p className="text-xl text-slate-600 dark:text-slate-400">
          {userTrack === 'DP' ? 'Data Professional Track' : 'Full-Stack Developer Track'}
        </p>
        <p className="text-slate-600 dark:text-slate-400 max-w-3xl">
          Complete step-by-step workflows, deliverables, and resources for each project. 
          Follow these guides to successfully complete your track requirements.
        </p>
      </div>

      <Separator className="my-8" />

      {/* Track-specific content */}
      {userTrack === 'DP' ? <DataProfessionalGuide /> : <FullStackGuide />}
    </div>
  )
}

function FullStackGuide() {
  return (
    <div className="space-y-16">
      {/* Project 1 */}
      <ProjectSection
        number={1}
        title="Responsive Portfolio Website"
        description="Build a professional portfolio using React, Tailwind CSS, and deploy to Netlify"
        duration="2-3 weeks (40 hours)"
        techStack={["React", "Vite", "Tailwind CSS", "Netlify"]}
        projectId={1}
        color="blue"
      >
        <ProjectObjectives>
          <ObjectiveItem text="Master React components and hooks" />
          <ObjectiveItem text="Style with Tailwind CSS utility classes" />
          <ObjectiveItem text="Deploy using Netlify CLI" />
          <ObjectiveItem text="Configure custom domains (optional)" />
        </ProjectObjectives>

        <ProjectSteps>
          <StepItem 
            number={1}
            title="Setup React Project"
            duration="2 hours"
            description="Create new React project with Vite, install Tailwind CSS, configure build tools, and test the setup."
          />
          <StepItem 
            number={2}
            title="Build Portfolio Components"
            duration="8 hours"
            description="Create Hero section with gradient, About section with profile, Projects showcase with cards, and Contact form with validation."
          />
          <StepItem 
            number={3}
            title="Make it Responsive"
            duration="4 hours"
            description="Add mobile navigation, test on different screen sizes (mobile, tablet, desktop), optimize images, and add smooth scrolling."
          />
          <StepItem 
            number={4}
            title="Deploy to Netlify"
            duration="2 hours"
            description="Install Netlify CLI, build production version, deploy to Netlify, and optionally configure custom domain."
          />
        </ProjectSteps>

        <ProjectDeliverables>
          <DeliverableItem text="Live Netlify deployment URL" required />
          <DeliverableItem text="GitHub repository with clean code" required />
          <DeliverableItem text="README with setup instructions" required />
          <DeliverableItem text="Screenshots (desktop & mobile)" />
        </ProjectDeliverables>

        <ProjectResources>
          <ResourceItem href="https://react.dev" text="React Documentation" />
          <ResourceItem href="https://tailwindcss.com/docs" text="Tailwind CSS Docs" />
          <ResourceItem href="https://docs.netlify.com/cli/get-started/" text="Netlify CLI Docs" />
          <ResourceItem href="https://vitejs.dev/guide/" text="Vite Guide" />
        </ProjectResources>
      </ProjectSection>

      <Separator className="my-12" />

      {/* Project 2 */}
      <ProjectSection
        number={2}
        title="E-Commerce Platform"
        description="Build a full-stack e-commerce platform with React, Django/Spring Boot, PostgreSQL, and Stripe"
        duration="4-5 weeks (80 hours)"
        techStack={["React", "Django", "PostgreSQL", "Stripe", "REST API"]}
        projectId={2}
        color="purple"
      >
        <ProjectObjectives>
          <ObjectiveItem text="Build REST APIs with Django/Spring Boot" />
          <ObjectiveItem text="Implement authentication and authorization" />
          <ObjectiveItem text="Integrate Stripe payment gateway" />
          <ObjectiveItem text="Design and query PostgreSQL database" />
          <ObjectiveItem text="Write unit and integration tests" />
        </ProjectObjectives>

        <ProjectSteps>
          <StepItem 
            number={1}
            title="Setup Backend API"
            duration="8 hours"
            description="Create Django/Spring Boot project, design database models (Product, Order, User), build REST API endpoints, and setup PostgreSQL connection."
          />
          <StepItem 
            number={2}
            title="Build Frontend"
            duration="10 hours"
            description="Create product listing with search/filter, shopping cart with Context API, user authentication flow, and checkout interface."
          />
          <StepItem 
            number={3}
            title="Integrate Stripe"
            duration="6 hours"
            description="Setup Stripe checkout sessions on backend, implement payment flow on frontend, handle success/cancel redirects, and test with Stripe test cards."
          />
          <StepItem 
            number={4}
            title="Testing & Deployment"
            duration="6 hours"
            description="Write unit tests for models and views, test payment flow end-to-end, deploy backend to Railway/Heroku, and deploy frontend to Vercel."
          />
        </ProjectSteps>

        <ProjectDeliverables>
          <DeliverableItem text="Live demo URL (frontend + backend)" required />
          <DeliverableItem text="GitHub repositories (frontend + backend)" required />
          <DeliverableItem text="Stripe test payment proof (screenshot)" required />
          <DeliverableItem text="API documentation (Postman or README)" required />
        </ProjectDeliverables>

        <ProjectResources>
          <ResourceItem href="https://www.django-rest-framework.org/" text="Django REST Framework" />
          <ResourceItem href="https://stripe.com/docs" text="Stripe Documentation" />
          <ResourceItem href="https://www.postgresqltutorial.com/" text="PostgreSQL Tutorial" />
        </ProjectResources>
      </ProjectSection>

      <Separator className="my-12" />

      {/* Project 3 */}
      <ProjectSection
        number={3}
        title="Social Dashboard + DevOps (Capstone)"
        description="Build a real-time social dashboard with WebSockets, Docker, CI/CD, and cloud deployment"
        duration="6-8 weeks (120 hours)"
        techStack={["React", "Django", "WebSockets", "Redis", "Docker", "Terraform", "AWS/GCP"]}
        projectId={3}
        color="teal"
      >
        <ProjectObjectives>
          <ObjectiveItem text="Implement real-time features with WebSockets" />
          <ObjectiveItem text="Use Redis for caching and pub/sub" />
          <ObjectiveItem text="Containerize with Docker" />
          <ObjectiveItem text="Setup CI/CD pipeline" />
          <ObjectiveItem text="Deploy to cloud (AWS/GCP)" />
          <ObjectiveItem text="Infrastructure as Code with Terraform" />
        </ProjectObjectives>

        <ProjectSteps>
          <StepItem 
            number={1}
            title="Build Social Dashboard"
            duration="12 hours"
            description="Create real-time chat with WebSockets, notifications system, activity feed with live updates, and Redis pub/sub integration."
          />
          <StepItem 
            number={2}
            title="Containerize with Docker"
            duration="6 hours"
            description="Create Dockerfiles for frontend and backend, write docker-compose.yml for multi-container setup, and test local deployment."
          />
          <StepItem 
            number={3}
            title="Setup CI/CD Pipeline"
            duration="6 hours"
            description="Configure GitHub Actions for automated testing, setup deployment workflow, and implement automated builds on push to main."
          />
          <StepItem 
            number={4}
            title="Deploy to Cloud"
            duration="8 hours"
            description="Use Terraform to provision AWS/GCP infrastructure (ECS/Cloud Run), deploy containers to cloud, configure networking and load balancing."
          />
        </ProjectSteps>

        <ProjectDeliverables>
          <DeliverableItem text="Cloud-deployed app URL" required />
          <DeliverableItem text="GitHub repository (Docker + Terraform + CI/CD)" required />
          <DeliverableItem text="Demo video (5-10 minutes)" required />
          <DeliverableItem text="Architecture diagram" required />
        </ProjectDeliverables>

        <ProjectResources>
          <ResourceItem href="https://docs.docker.com/" text="Docker Documentation" />
          <ResourceItem href="https://learn.hashicorp.com/terraform" text="Terraform AWS Guide" />
          <ResourceItem href="https://docs.github.com/en/actions" text="GitHub Actions" />
          <ResourceItem href="https://docs.aws.amazon.com/ecs/" text="AWS ECS Guide" />
        </ProjectResources>
      </ProjectSection>

      {/* Submission Guidelines */}
      <div className="mt-16 p-8 bg-slate-50 dark:bg-slate-900/50 rounded-lg border-2 border-slate-200 dark:border-slate-700">
        <h2 className="text-2xl font-bold mb-4 text-slate-900 dark:text-slate-100">Submission Guidelines</h2>
        <div className="space-y-4 text-slate-700 dark:text-slate-300">
          <div>
            <h3 className="font-semibold mb-2">Code Quality</h3>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>Clean, readable code with proper comments</li>
              <li>Consistent formatting and naming conventions</li>
              <li>No hardcoded credentials or sensitive data</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-2">Documentation</h3>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>README with clear setup instructions</li>
              <li>API documentation (if applicable)</li>
              <li>Architecture diagrams (for Project 3)</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-2">Testing</h3>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>Unit tests (minimum 70% coverage for Projects 2 & 3)</li>
              <li>Integration tests where applicable</li>
              <li>Manual testing checklist completed</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

function DataProfessionalGuide() {
  return (
    <div className="space-y-16">
      {/* Project 1 */}
      <ProjectSection
        number={1}
        title="Business Analytics Dashboard"
        description="Build an interactive dashboard using Python, PostgreSQL, and Apache Superset"
        duration="2-3 weeks (40 hours)"
        techStack={["Python", "Pandas", "PostgreSQL", "Apache Superset", "Jupyter"]}
        projectId={1}
        color="blue"
      >
        <ProjectObjectives>
          <ObjectiveItem text="Clean and transform data with Python/Pandas" />
          <ObjectiveItem text="Load data into PostgreSQL database" />
          <ObjectiveItem text="Write complex SQL queries for insights" />
          <ObjectiveItem text="Build interactive dashboards in Superset" />
        </ProjectObjectives>

        <ProjectSteps>
          <StepItem 
            number={1}
            title="Clean Raw CSV Dataset"
            duration="4 hours"
            description="Use Jupyter Lab to load, explore, and clean the provided dataset. Handle missing values, fix data types, and remove duplicates."
          />
          <StepItem 
            number={2}
            title="Load Data into PostgreSQL"
            duration="2 hours"
            description="Connect to your PostgreSQL schema and load the cleaned data using SQLAlchemy or psycopg2."
          />
          <StepItem 
            number={3}
            title="Write SQL Queries"
            duration="4 hours"
            description="Create SQL queries to calculate key metrics, aggregations, and business insights."
          />
          <StepItem 
            number={4}
            title="Build Superset Dashboard"
            duration="6 hours"
            description="Connect Superset to PostgreSQL, create visualizations, add filters, and design an interactive dashboard."
          />
        </ProjectSteps>

        <ProjectDeliverables>
          <DeliverableItem text="Superset Dashboard URL" required />
          <DeliverableItem text="SQL queries (GitHub repo or file)" required />
          <DeliverableItem text="PDF Insights Report (1 page)" required />
          <DeliverableItem text="Python cleaning script (optional)" />
        </ProjectDeliverables>

        <ProjectResources>
          <ResourceItem href="https://pandas.pydata.org/docs/" text="Pandas Documentation" />
          <ResourceItem href="https://www.postgresql.org/docs/" text="PostgreSQL Docs" />
          <ResourceItem href="https://superset.apache.org/docs/intro" text="Apache Superset Docs" />
        </ProjectResources>
      </ProjectSection>

      <Separator className="my-12" />

      {/* Project 2 */}
      <ProjectSection
        number={2}
        title="Automated ETL Pipeline"
        description="Build an automated data pipeline with Prefect orchestration"
        duration="3-4 weeks (60 hours)"
        techStack={["Python", "Prefect", "PostgreSQL", "REST API", "Pandas"]}
        projectId={2}
        color="purple"
      >
        <ProjectObjectives>
          <ObjectiveItem text="Extract data from REST APIs" />
          <ObjectiveItem text="Transform data with Pandas" />
          <ObjectiveItem text="Load data into PostgreSQL" />
          <ObjectiveItem text="Orchestrate pipeline with Prefect" />
          <ObjectiveItem text="Schedule and monitor workflows" />
        </ProjectObjectives>

        <ProjectSteps>
          <StepItem 
            number={1}
            title="Extract Data from API"
            duration="4 hours"
            description="Use Python requests library to pull data from a public API. Handle pagination and error cases."
          />
          <StepItem 
            number={2}
            title="Transform Data"
            duration="6 hours"
            description="Clean, normalize, and transform the API data using Pandas. Apply business logic and data validation."
          />
          <StepItem 
            number={3}
            title="Load to PostgreSQL"
            duration="4 hours"
            description="Insert transformed data into your database schema. Handle upserts and data conflicts."
          />
          <StepItem 
            number={4}
            title="Orchestrate with Prefect"
            duration="6 hours"
            description="Build a Prefect flow to orchestrate the ETL pipeline. Set up scheduling, monitoring, and email notifications."
          />
        </ProjectSteps>

        <ProjectDeliverables>
          <DeliverableItem text="Python ETL script (GitHub repo)" required />
          <DeliverableItem text="Prefect workflow DAG" required />
          <DeliverableItem text="PostgreSQL table with loaded data" required />
          <DeliverableItem text="Email report screenshot" required />
        </ProjectDeliverables>

        <ProjectResources>
          <ResourceItem href="https://docs.prefect.io/" text="Prefect Documentation" />
          <ResourceItem href="https://requests.readthedocs.io/" text="Python Requests" />
          <ResourceItem href="https://pandas.pydata.org/" text="Pandas Guide" />
        </ProjectResources>
      </ProjectSection>

      <Separator className="my-12" />

      {/* Project 3 */}
      <ProjectSection
        number={3}
        title="End-to-End Analytics Solution (Capstone)"
        description="Build a cloud-hosted analytics solution with BigQuery/Redshift"
        duration="5-6 weeks (100 hours)"
        techStack={["Python", "BigQuery/Redshift", "dbt", "Looker/Tableau", "Airflow"]}
        projectId={3}
        color="teal"
      >
        <ProjectObjectives>
          <ObjectiveItem text="Combine multiple data sources" />
          <ObjectiveItem text="Load data to cloud data warehouse" />
          <ObjectiveItem text="Write optimized SQL queries" />
          <ObjectiveItem text="Build production-grade dashboards" />
          <ObjectiveItem text="Document insights and recommendations" />
        </ProjectObjectives>

        <ProjectSteps>
          <StepItem 
            number={1}
            title="Combine Data Sources"
            duration="8 hours"
            description="Extract data from multiple sources (APIs, databases, files). Merge and reconcile data from different systems."
          />
          <StepItem 
            number={2}
            title="Load to Cloud Warehouse"
            duration="6 hours"
            description="Setup BigQuery/Redshift, design schema, and load data. Optimize for query performance."
          />
          <StepItem 
            number={3}
            title="Transform with dbt"
            duration="10 hours"
            description="Use dbt to create data models, apply transformations, and build analytics-ready tables."
          />
          <StepItem 
            number={4}
            title="Build Cloud Dashboard"
            duration="12 hours"
            description="Create interactive dashboards in Looker/Tableau. Add filters, drill-downs, and export capabilities."
          />
        </ProjectSteps>

        <ProjectDeliverables>
          <DeliverableItem text="Cloud-hosted dashboard URL" required />
          <DeliverableItem text="SQL scripts (GitHub repo)" required />
          <DeliverableItem text="PDF Case Study Report" required />
        </ProjectDeliverables>

        <ProjectResources>
          <ResourceItem href="https://cloud.google.com/bigquery/docs" text="BigQuery Documentation" />
          <ResourceItem href="https://docs.getdbt.com/" text="dbt Documentation" />
          <ResourceItem href="https://airflow.apache.org/docs/" text="Apache Airflow" />
        </ProjectResources>
      </ProjectSection>

      {/* Submission Guidelines */}
      <div className="mt-16 p-8 bg-slate-50 dark:bg-slate-900/50 rounded-lg border-2 border-slate-200 dark:border-slate-700">
        <h2 className="text-2xl font-bold mb-4 text-slate-900 dark:text-slate-100">Submission Guidelines</h2>
        <div className="space-y-4 text-slate-700 dark:text-slate-300">
          <div>
            <h3 className="font-semibold mb-2">Code Quality</h3>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>Clean, readable code with proper comments</li>
              <li>Consistent formatting and naming conventions</li>
              <li>No hardcoded credentials or sensitive data</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-2">Documentation</h3>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>README with clear setup instructions</li>
              <li>SQL query documentation</li>
              <li>Data dictionary and schema diagrams</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-2">Analysis</h3>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>Clear insights and recommendations</li>
              <li>Data-driven conclusions</li>
              <li>Professional presentation</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

// Component Helpers
function ProjectSection({ 
  number, 
  title, 
  description, 
  duration, 
  techStack, 
  projectId,
  color,
  children 
}: { 
  number: number
  title: string
  description: string
  duration: string
  techStack: string[]
  projectId: number
  color: string
  children: React.ReactNode
}) {
  const colorClasses = {
    blue: "from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700",
    purple: "from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700",
    teal: "from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700"
  }

  return (
    <section className="space-y-8">
      {/* Project Header */}
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-12 h-12 rounded-full bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 font-bold text-xl">
            {number}
          </div>
          <div>
            <h2 className="text-3xl font-bold text-slate-900 dark:text-slate-100">{title}</h2>
          </div>
        </div>
        <p className="text-lg text-slate-600 dark:text-slate-400">{description}</p>
        
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
            <Clock className="h-4 w-4" />
            <span className="text-sm font-medium">{duration}</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {techStack.map((tech, i) => (
              <Badge key={i} variant="outline" className="text-xs">{tech}</Badge>
            ))}
          </div>
        </div>
      </div>

      {/* Project Content */}
      <div className="space-y-8">
        {children}
      </div>

      {/* Start Project Button */}
      <Button 
        asChild 
        size="lg" 
        className={`w-full bg-gradient-to-r ${colorClasses[color as keyof typeof colorClasses]}`}
      >
        <Link href={`/student/projects/${projectId}`}>
          Start Project {number}
          <ArrowRight className="ml-2 h-4 w-4" />
        </Link>
      </Button>
    </section>
  )
}

function ProjectObjectives({ children }: { children: React.ReactNode }) {
  return (
    <div className="space-y-3">
      <h3 className="text-lg font-semibold flex items-center gap-2 text-slate-900 dark:text-slate-100">
        <Target className="h-5 w-5" />
        Learning Objectives
      </h3>
      <div className="space-y-2">
        {children}
      </div>
    </div>
  )
}

function ObjectiveItem({ text }: { text: string }) {
  return (
    <div className="flex items-start gap-3 py-1">
      <CheckCircle2 className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
      <span className="text-slate-700 dark:text-slate-300">{text}</span>
    </div>
  )
}

function ProjectSteps({ children }: { children: React.ReactNode }) {
  return (
    <div className="space-y-3">
      <h3 className="text-lg font-semibold flex items-center gap-2 text-slate-900 dark:text-slate-100">
        <BookOpen className="h-5 w-5" />
        Step-by-Step Workflow
      </h3>
      <div className="space-y-2 border-l-2 border-slate-200 dark:border-slate-700 pl-4">
        {children}
      </div>
    </div>
  )
}

function StepItem({ number, title, duration, description }: { number: number; title: string; duration: string; description: string }) {
  return (
    <div className="flex gap-4 py-3">
      <div className="flex-shrink-0 w-7 h-7 rounded-full bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 flex items-center justify-center font-bold text-sm">
        {number}
      </div>
      <div className="flex-1 space-y-1">
        <div className="flex items-center justify-between gap-4">
          <h4 className="font-semibold text-slate-900 dark:text-slate-100">{title}</h4>
          <span className="text-xs text-slate-500 dark:text-slate-400 whitespace-nowrap">{duration}</span>
        </div>
        <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">{description}</p>
      </div>
    </div>
  )
}

function ProjectDeliverables({ children }: { children: React.ReactNode }) {
  return (
    <div className="space-y-3">
      <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Deliverables</h3>
      <div className="space-y-1 border-l-2 border-slate-200 dark:border-slate-700 pl-4">
        {children}
      </div>
    </div>
  )
}

function DeliverableItem({ text, required = false }: { text: string; required?: boolean }) {
  return (
    <div className="flex items-center justify-between py-2">
      <div className="flex items-center gap-3">
        <div className="w-5 h-5 rounded-full border-2 border-emerald-600 flex items-center justify-center flex-shrink-0">
          <div className="w-2 h-2 rounded-full bg-emerald-600"></div>
        </div>
        <span className="text-slate-700 dark:text-slate-300">{text}</span>
      </div>
      {required && (
        <Badge variant="destructive" className="text-xs">Required</Badge>
      )}
    </div>
  )
}

function ProjectResources({ children }: { children: React.ReactNode }) {
  return (
    <div className="space-y-3">
      <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Resources</h3>
      <div className="grid gap-2">
        {children}
      </div>
    </div>
  )
}

function ResourceItem({ href, text }: { href: string; text: string }) {
  return (
    <a 
      href={href} 
      target="_blank" 
      rel="noopener noreferrer"
      className="flex items-center gap-2 py-2 text-blue-600 dark:text-blue-400 hover:underline group"
    >
      <ExternalLink className="h-4 w-4 flex-shrink-0" />
      <span className="text-sm">{text}</span>
    </a>
  )
}
