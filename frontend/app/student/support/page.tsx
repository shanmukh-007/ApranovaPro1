'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { MessageCircle, Plus, Clock, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'
import apiClient from '@/lib/apiClient'

export default function StudentSupportPage() {
  const router = useRouter()
  const [tickets, setTickets] = useState([])
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [creating, setCreating] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'CONCEPT',
    priority: 'MEDIUM',
    project: '',
    attachment_url: ''
  })

  useEffect(() => {
    fetchTickets()
    fetchProjects()
  }, [])

  const fetchTickets = async () => {
    try {
      const response = await apiClient.get('/support/tickets/my_tickets/')
      setTickets(response.data)
    } catch (err) {
      console.error('Error fetching tickets:', err)
    } finally {
      setLoading(false)
    }
  }

  const fetchProjects = async () => {
    try {
      const response = await apiClient.get('/curriculum/projects/')
      setProjects(response.data)
    } catch (err) {
      console.error('Error fetching projects:', err)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setCreating(true)
    setError('')
    setSuccess('')

    try {
      const payload = {
        ...formData,
        project: formData.project && formData.project !== 'none' ? formData.project : null
      }
      
      await apiClient.post('/support/tickets/', payload)
      
      setSuccess('Ticket created successfully! Your trainer will be notified.')
      setFormData({
        title: '',
        description: '',
        category: 'CONCEPT',
        priority: 'MEDIUM',
        project: '',
        attachment_url: ''
      })
      setShowCreateForm(false)
      fetchTickets()
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to create ticket')
    } finally {
      setCreating(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'OPEN': return 'bg-blue-100 text-blue-800'
      case 'IN_PROGRESS': return 'bg-yellow-100 text-yellow-800'
      case 'WAITING_STUDENT': return 'bg-purple-100 text-purple-800'
      case 'RESOLVED': return 'bg-green-100 text-green-800'
      case 'CLOSED': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'URGENT': return 'bg-red-100 text-red-800'
      case 'HIGH': return 'bg-orange-100 text-orange-800'
      case 'MEDIUM': return 'bg-blue-100 text-blue-800'
      case 'LOW': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    )
  }

  return (
    <div className="container mx-auto p-6 max-w-6xl">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold">Support & Help</h1>
          <p className="text-muted-foreground">Get help from your trainer</p>
        </div>
        <Button onClick={() => setShowCreateForm(!showCreateForm)}>
          <Plus className="h-4 w-4 mr-2" />
          New Ticket
        </Button>
      </div>

      {success && (
        <Alert className="mb-6 bg-green-50 border-green-200">
          <CheckCircle className="h-4 w-4 text-green-600" />
          <AlertDescription className="text-green-800">{success}</AlertDescription>
        </Alert>
      )}

      {error && (
        <Alert className="mb-6" variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {showCreateForm && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Create Support Ticket</CardTitle>
            <CardDescription>Describe your issue or question</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="title">Title *</Label>
                <Input
                  id="title"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="Brief description of your issue"
                  required
                />
              </div>

              <div>
                <Label htmlFor="description">Description *</Label>
                <Textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Explain your issue in detail..."
                  rows={5}
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="category">Category *</Label>
                  <Select value={formData.category} onValueChange={(value) => setFormData({ ...formData, category: value })}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="TECHNICAL">Technical Issue</SelectItem>
                      <SelectItem value="PROJECT">Project Help</SelectItem>
                      <SelectItem value="CONCEPT">Concept Doubt</SelectItem>
                      <SelectItem value="SUBMISSION">Submission Issue</SelectItem>
                      <SelectItem value="WORKSPACE">Workspace Issue</SelectItem>
                      <SelectItem value="PAYMENT">Payment Issue</SelectItem>
                      <SelectItem value="OTHER">Other</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="priority">Priority *</Label>
                  <Select value={formData.priority} onValueChange={(value) => setFormData({ ...formData, priority: value })}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="URGENT">🔴 Urgent - Blocked</SelectItem>
                      <SelectItem value="HIGH">🟠 High - Important</SelectItem>
                      <SelectItem value="MEDIUM">🟡 Medium - Normal</SelectItem>
                      <SelectItem value="LOW">⚪ Low - Minor</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div>
                <Label htmlFor="project">Related Project (Optional)</Label>
                <Select value={formData.project || undefined} onValueChange={(value) => setFormData({ ...formData, project: value })}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a project" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="none">None</SelectItem>
                    {projects.map((project: any) => (
                      <SelectItem key={project.id} value={project.id.toString()}>
                        {project.title}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="attachment">Attachment URL (Optional)</Label>
                <Input
                  id="attachment"
                  type="url"
                  value={formData.attachment_url}
                  onChange={(e) => setFormData({ ...formData, attachment_url: e.target.value })}
                  placeholder="https://example.com/screenshot.png"
                />
                <p className="text-xs text-muted-foreground mt-1">
                  Upload screenshot to Imgur or similar and paste URL
                </p>
              </div>

              <div className="flex gap-2">
                <Button type="submit" disabled={creating}>
                  {creating ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Creating...
                    </>
                  ) : (
                    'Create Ticket'
                  )}
                </Button>
                <Button type="button" variant="outline" onClick={() => setShowCreateForm(false)}>
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      <div className="space-y-4">
        {tickets.length === 0 ? (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <MessageCircle className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold mb-2">No tickets yet</h3>
              <p className="text-muted-foreground text-center mb-4">
                Create a ticket to get help from your trainer
              </p>
              <Button onClick={() => setShowCreateForm(true)}>
                <Plus className="h-4 w-4 mr-2" />
                Create First Ticket
              </Button>
            </CardContent>
          </Card>
        ) : (
          tickets.map((ticket: any) => (
            <Card key={ticket.id} className="cursor-pointer hover:shadow-md transition-shadow" onClick={() => router.push(`/student/support/${ticket.id}`)}>
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <Badge className={getStatusColor(ticket.status)}>
                        {ticket.status.replace('_', ' ')}
                      </Badge>
                      <Badge className={getPriorityColor(ticket.priority)}>
                        {ticket.priority}
                      </Badge>
                      <span className="text-sm text-muted-foreground">
                        {ticket.ticket_number}
                      </span>
                    </div>
                    <CardTitle className="text-xl">{ticket.title}</CardTitle>
                    <CardDescription className="mt-2">
                      {ticket.description.substring(0, 150)}
                      {ticket.description.length > 150 && '...'}
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between text-sm text-muted-foreground">
                  <div className="flex items-center gap-4">
                    <span className="flex items-center gap-1">
                      <Clock className="h-4 w-4" />
                      {new Date(ticket.created_at).toLocaleDateString()}
                    </span>
                    {ticket.assigned_to_name && (
                      <span>Assigned to: {ticket.assigned_to_name}</span>
                    )}
                    {ticket.message_count > 0 && (
                      <span className="flex items-center gap-1">
                        <MessageCircle className="h-4 w-4" />
                        {ticket.message_count} {ticket.message_count === 1 ? 'reply' : 'replies'}
                      </span>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  )
}
