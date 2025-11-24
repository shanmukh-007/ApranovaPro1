"use client"

import { useState } from "react"
import { HelpCircle, Search, Book, MessageCircle, Mail, Phone, FileText, Video, ExternalLink, Send } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { useToast } from "@/hooks/use-toast"

export default function StudentHelpPage() {
  const { toast } = useToast()
  const [searchQuery, setSearchQuery] = useState("")
  const [message, setMessage] = useState("")
  const [subject, setSubject] = useState("")
  const [submitting, setSubmitting] = useState(false)

  const handleSubmitTicket = async () => {
    if (!subject || !message) {
      toast({
        title: "Error",
        description: "Please fill in all fields",
        variant: "destructive",
      })
      return
    }
    
    setSubmitting(true)
    
    // Simulate API call
    setTimeout(() => {
      toast({
        title: "Ticket Submitted Successfully!",
        description: "Our support team will get back to you within 24 hours",
      })
      setSubject("")
      setMessage("")
      setSubmitting(false)
    }, 1000)
  }

  const faqs = [
    {
      question: "How do I start a project?",
      answer: "Navigate to your project page and click the 'Start Project' button. If you're in the FSD track, make sure to connect your GitHub account first. The system will automatically create a repository from the template for you."
    },
    {
      question: "How do I connect my GitHub account?",
      answer: "Go to Settings page and click 'Connect GitHub Account'. You'll be redirected to GitHub to authorize the connection. Once connected, you can start projects and submit via Pull Requests."
    },
    {
      question: "How do I submit my project?",
      answer: "For FSD track: Create a Pull Request from your develop branch to main branch on GitHub. The system will automatically detect and create a submission. For DP track: Use the Submit page to upload your deliverables."
    },
    {
      question: "How does the sequential project flow work?",
      answer: "You must complete and get approval for Project 1 before accessing Project 2, and Project 2 before Project 3. Your trainer will review your submissions and approve them, unlocking the next project."
    },
    {
      question: "Where can I find project instructions?",
      answer: "Click 'Project Guide' from the sidebar or the project page. You'll find step-by-step workflows, deliverables, resources, and Git workflow instructions for each project."
    },
    {
      question: "How do I access my development tools?",
      answer: "Each project page shows the relevant tools for that project. For FSD: VS Code Server, GitHub, deployment tools. For DP: Jupyter Lab, PostgreSQL, Apache Superset. Click the 'Open' button to access each tool."
    },
    {
      question: "Can I change my password?",
      answer: "Yes! Go to Settings > Security section. Enter your current password, then your new password twice, and click 'Change Password'."
    },
    {
      question: "How do I track my progress?",
      answer: "Your dashboard shows your current project, overall progress, completed steps, and project status. Each project page also shows detailed progress with step completion tracking."
    },
    {
      question: "What if I need my project revised?",
      answer: "If your trainer requests revisions, you'll see feedback on your submission. Make the requested changes, push to your develop branch (FSD) or resubmit (DP), and your trainer will review again."
    },
    {
      question: "How do I contact my trainer?",
      answer: "Your assigned trainer's information is shown on your dashboard. You can also submit a support ticket below with 'Trainer Query' as the subject, and we'll route it to your trainer."
    }
  ]

  const resources = [
    {
      icon: Book,
      title: "Project Guide",
      description: "Complete step-by-step project instructions",
      link: "/student/project-guide"
    },
    {
      icon: FileText,
      title: "Documentation",
      description: "Platform guides and tutorials",
      link: "#"
    },
    {
      icon: MessageCircle,
      title: "Discord Community",
      description: "Connect with other students",
      link: "#"
    },
    {
      icon: Video,
      title: "Video Tutorials",
      description: "Watch step-by-step guides",
      link: "#"
    }
  ]

  const filteredFaqs = faqs.filter(faq =>
    searchQuery === "" ||
    faq.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
    faq.answer.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-20">
      {/* Page Header */}
      <div className="space-y-3">
        <h1 className="text-4xl font-bold text-slate-900 dark:text-slate-100">
          Help & Support
        </h1>
        <p className="text-lg text-slate-600 dark:text-slate-400">
          Find answers to common questions or get in touch with our support team
        </p>
      </div>

      {/* Search */}
      <Card className="border-2 shadow-lg">
        <CardContent className="pt-6">
          <div className="relative">
            <Search className="absolute left-4 top-4 h-5 w-5 text-slate-400" />
            <Input
              placeholder="Search for help articles, FAQs, or topics..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-12 h-14 text-base"
            />
          </div>
          {searchQuery && (
            <p className="mt-3 text-sm text-slate-600 dark:text-slate-400">
              Found {filteredFaqs.length} result{filteredFaqs.length !== 1 ? 's' : ''} for "{searchQuery}"
            </p>
          )}
        </CardContent>
      </Card>

      {/* Quick Links */}
      <div>
        <h2 className="text-2xl font-bold mb-4 text-slate-900 dark:text-slate-100">Quick Links</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {resources.map((resource, index) => {
            const Icon = resource.icon
            return (
              <Card key={index} className="border-2 hover:border-blue-400 dark:hover:border-blue-600 transition-colors cursor-pointer">
                <a href={resource.link} className="block">
                  <CardContent className="pt-6 pb-6">
                    <div className="flex flex-col items-center gap-3 text-center">
                      <div className="w-14 h-14 rounded-full bg-blue-100 dark:bg-blue-900/50 flex items-center justify-center">
                        <Icon className="h-7 w-7 text-blue-600 dark:text-blue-400" />
                      </div>
                      <div>
                        <div className="font-semibold text-slate-900 dark:text-slate-100 mb-1">{resource.title}</div>
                        <div className="text-sm text-slate-600 dark:text-slate-400">{resource.description}</div>
                      </div>
                    </div>
                  </CardContent>
                </a>
              </Card>
            )
          })}
        </div>
      </div>

      {/* FAQs */}
      <Card className="border-2 shadow-lg">
        <CardHeader>
          <CardTitle className="text-2xl">Frequently Asked Questions</CardTitle>
          <CardDescription>Find quick answers to common questions</CardDescription>
        </CardHeader>
        <CardContent>
          {filteredFaqs.length > 0 ? (
            <Accordion type="single" collapsible className="w-full">
              {filteredFaqs.map((faq, index) => (
                <AccordionItem key={index} value={`item-${index}`}>
                  <AccordionTrigger className="text-left hover:no-underline">
                    <span className="font-semibold text-slate-900 dark:text-slate-100">{faq.question}</span>
                  </AccordionTrigger>
                  <AccordionContent className="text-slate-600 dark:text-slate-400 leading-relaxed">
                    {faq.answer}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          ) : (
            <p className="text-center py-8 text-slate-600 dark:text-slate-400">
              No FAQs found matching your search. Try different keywords or submit a support ticket below.
            </p>
          )}
        </CardContent>
      </Card>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Contact Support */}
        <Card className="border-2 shadow-lg">
          <CardHeader>
            <CardTitle className="text-xl">Contact Information</CardTitle>
            <CardDescription>Get in touch with our support team</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <a 
              href="mailto:support@apranova.com"
              className="flex items-center gap-3 p-4 rounded-lg border-2 border-slate-200 dark:border-slate-700 hover:border-blue-400 dark:hover:border-blue-600 transition-colors"
            >
              <div className="w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-900/50 flex items-center justify-center flex-shrink-0">
                <Mail className="h-5 w-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <div className="font-semibold text-slate-900 dark:text-slate-100">Email Support</div>
                <div className="text-sm text-slate-600 dark:text-slate-400">support@apranova.com</div>
              </div>
            </a>
            
            <div className="flex items-center gap-3 p-4 rounded-lg border-2 border-slate-200 dark:border-slate-700">
              <div className="w-10 h-10 rounded-full bg-emerald-100 dark:bg-emerald-900/50 flex items-center justify-center flex-shrink-0">
                <MessageCircle className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
              </div>
              <div>
                <div className="font-semibold text-slate-900 dark:text-slate-100">Discord Community</div>
                <div className="text-sm text-slate-600 dark:text-slate-400">Join our community server</div>
              </div>
            </div>
            
            <div className="flex items-center gap-3 p-4 rounded-lg border-2 border-slate-200 dark:border-slate-700">
              <div className="w-10 h-10 rounded-full bg-purple-100 dark:bg-purple-900/50 flex items-center justify-center flex-shrink-0">
                <Phone className="h-5 w-5 text-purple-600 dark:text-purple-400" />
              </div>
              <div>
                <div className="font-semibold text-slate-900 dark:text-slate-100">Office Hours</div>
                <div className="text-sm text-slate-600 dark:text-slate-400">Mon-Fri, 9 AM - 6 PM EST</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Submit Ticket */}
        <Card className="border-2 shadow-lg">
          <CardHeader>
            <CardTitle className="text-xl">Submit a Support Ticket</CardTitle>
            <CardDescription>Can't find what you're looking for? Send us a message</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="subject">Subject</Label>
              <Input
                id="subject"
                placeholder="Brief description of your issue"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="message">Message</Label>
              <Textarea
                id="message"
                placeholder="Describe your issue in detail..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                rows={5}
              />
            </div>
            <Button 
              onClick={handleSubmitTicket} 
              className="w-full"
              disabled={submitting}
            >
              {submitting ? (
                <>Submitting...</>
              ) : (
                <>
                  <Send className="mr-2 h-4 w-4" />
                  Submit Ticket
                </>
              )}
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
