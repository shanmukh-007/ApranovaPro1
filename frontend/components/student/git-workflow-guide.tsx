"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { 
  GitBranch, 
  GitPullRequest, 
  GitMerge, 
  CheckCircle2,
  Code,
  UserCheck,
  Info
} from "lucide-react"
import { useState } from "react"
import { Button } from "@/components/ui/button"

interface GitWorkflowGuideProps {
  repoUrl?: string
  hasRepo: boolean
  hasPR?: boolean
  isApproved?: boolean
  isMerged?: boolean
}

export default function GitWorkflowGuide({ 
  repoUrl, 
  hasRepo, 
  hasPR = false, 
  isApproved = false, 
  isMerged = false 
}: GitWorkflowGuideProps) {
  const [showGuide, setShowGuide] = useState(true)

  const steps = [
    {
      icon: <GitBranch className="h-5 w-5" />,
      title: "Repository Created",
      description: "Your project repository is ready",
      completed: hasRepo,
      command: repoUrl ? `git clone ${repoUrl}` : null
    },
    {
      icon: <Code className="h-5 w-5" />,
      title: "Work on Develop Branch",
      description: "Make your changes on the develop branch",
      completed: hasRepo,
      command: "git checkout develop\ngit add .\ngit commit -m \"Your message\"\ngit push origin develop"
    },
    {
      icon: <GitPullRequest className="h-5 w-5" />,
      title: "Create Pull Request",
      description: "Open PR from develop to main on GitHub",
      completed: hasPR,
      command: null
    },
    {
      icon: <UserCheck className="h-5 w-5" />,
      title: "Trainer Review",
      description: "Wait for trainer to review and approve",
      completed: isApproved,
      command: null
    },
    {
      icon: <GitMerge className="h-5 w-5" />,
      title: "Merge Pull Request",
      description: "Merge PR after approval",
      completed: isMerged,
      command: null
    }
  ]

  return (
    <Card className="border-2 shadow-lg">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <GitBranch className="h-5 w-5" />
              Git Workflow Guide
            </CardTitle>
            <CardDescription>Follow these steps to submit your project</CardDescription>
          </div>
          <Button 
            variant="ghost" 
            size="sm"
            onClick={() => setShowGuide(!showGuide)}
          >
            {showGuide ? 'Hide' : 'Show'}
          </Button>
        </div>
      </CardHeader>
      
      {showGuide && (
        <CardContent className="space-y-6">
          {!hasRepo && (
            <Alert>
              <Info className="h-4 w-4" />
              <AlertDescription>
                <p className="font-semibold mb-2">Repository Not Created Yet</p>
                <p className="text-sm">
                  Click the "Start Project" button to create your GitHub repository from the template. 
                  Once created, you'll see the complete Git workflow guide here.
                </p>
              </AlertDescription>
            </Alert>
          )}

          {hasRepo && (
            <div className="space-y-3">
              {steps.map((step, index) => (
                <div 
                  key={index}
                  className={`flex items-start gap-4 p-4 rounded-lg border-2 transition-all ${
                    step.completed 
                      ? 'border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-950/30' 
                      : 'border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/50'
                  }`}
                >
                  <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                    step.completed 
                      ? 'bg-emerald-500 text-white' 
                      : 'bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-400'
                  }`}>
                    {step.completed ? <CheckCircle2 className="h-5 w-5" /> : step.icon}
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h4 className="font-semibold text-slate-900 dark:text-slate-100">
                        {step.title}
                      </h4>
                      {step.completed && (
                        <Badge variant="outline" className="text-xs bg-emerald-100 text-emerald-700 border-emerald-300">
                          Complete
                        </Badge>
                      )}
                    </div>
                    <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">
                      {step.description}
                    </p>
                    
                    {step.command && (
                      <div className="mt-2">
                        <pre className="text-xs bg-slate-900 dark:bg-slate-950 text-slate-100 p-3 rounded overflow-x-auto">
                          <code>{step.command}</code>
                        </pre>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}

          {hasRepo && (
            <Alert>
              <Info className="h-4 w-4" />
              <AlertDescription>
                <div className="space-y-2">
                  <p className="font-semibold">Important Notes:</p>
                  <ul className="text-sm space-y-1 ml-4 list-disc">
                    <li>Always work on the <code className="bg-slate-200 dark:bg-slate-800 px-1 rounded">develop</code> branch</li>
                    <li>Never push directly to <code className="bg-slate-200 dark:bg-slate-800 px-1 rounded">main</code> (it's protected)</li>
                    <li>Create a Pull Request on GitHub when ready for review</li>
                    <li>Wait for trainer approval before merging</li>
                    <li>Commit frequently with clear messages</li>
                  </ul>
                </div>
              </AlertDescription>
            </Alert>
          )}

          {repoUrl && (
            <div className="flex gap-3">
              <Button asChild variant="outline" size="sm">
                <a href={repoUrl} target="_blank" rel="noopener noreferrer">
                  View Repository
                </a>
              </Button>
              {hasRepo && !hasPR && (
                <Button asChild variant="outline" size="sm">
                  <a 
                    href={`${repoUrl}/compare/main...develop?expand=1`} 
                    target="_blank" 
                    rel="noopener noreferrer"
                  >
                    Create Pull Request
                  </a>
                </Button>
              )}
            </div>
          )}
        </CardContent>
      )}
    </Card>
  )
}
