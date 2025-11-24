'use client'

import { useState, useEffect } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { ArrowLeft, Send, Loader2, CheckCircle, AlertCircle, User, Clock, Paperclip } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import apiClient from '@/lib/apiClient'

export default function TrainerTicketDetailPage() {
  const router = useRouter()
  const params = useParams()
  const ticketId = params.id

  const [ticket, setTicket] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [updating, setUpdating] = useState(false)
  const [resolving, setResolving] = useState(false)
  const [message, setMessage] = useState('')
  const [attachmentUrl, setAttachmentUrl] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    fetchTicket()
  }, [ticketId])

  const fetchTicket = async () => {
    try {
      const response = await apiClient.get(`/support/tickets/${ticketId}/`)
      setTicket(response.data)
    } catch (err) {
      console.error('Error fetching ticket:', err)
      setError('Failed to load ticket')
    } finally {
      setLoading(false)
    }
  }

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!message.trim()) return

    setSending(true)
    setError('')
    setSuccess('')

    try {
      await apiClient.post(`/support/tickets/${ticketId}/add_message/`, {
        message: message.trim(),
        attachment_url: attachmentUrl || undefined
      })

      setSuccess('Message sent!')
      setMessage('')
      setAttachmentUrl('')
      fetchTicket()
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to send message')
    } finally {
      setSending(false)
    }
  }

  const handleUpdateStatus = async (newStatus: string) => {
    setUpdating(true)
    setError('')

    try {
      await apiClient.patch(`/support/tickets/${ticketId}/`, {
        status: newStatus
      })

      setSuccess('Status updated!')
      fetchTicket()
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to update status')
    } finally {
      setUpdating(false)
    }
  }

  const handleResolveTicket = async () => {
    setResolving(true)
    setError('')

    try {
      await apiClient.post(`/support/tickets/${ticketId}/resolve/`, {
        message: message.trim() || 'Issue resolved'
      })

      setSuccess('Ticket resolved!')
      setMessage('')
      fetchTicket()
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to resolve ticket')
    } finally {
      setResolving(false)
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

  if (!ticket) {
    return (
      <div className="container mx-auto p-6 max-w-4xl">
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>Ticket not found</AlertDescription>
        </Alert>
        <Button onClick={() => router.push('/trainer/support')} className="mt-4">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Tickets
        </Button>
      </div>
    )
  }

  const isResolved = ticket.status === 'RESOLVED' || ticket.status === 'CLOSED'

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <Button variant="ghost" onClick={() => router.push('/trainer/support')} className="mb-4">
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Tickets
      </Button>

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

      {/* Ticket Header */}
      <Card className="mb-6">
        <CardHeader>
          <div className="flex items-start justify-between">
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
              <CardTitle className="text-2xl">{ticket.title}</CardTitle>
              <CardDescription className="mt-2">
                Created by {ticket.student_name} on {new Date(ticket.created_at).toLocaleString()}
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h3 className="font-semibold mb-2">Description</h3>
              <p className="text-muted-foreground whitespace-pre-wrap">{ticket.description}</p>
            </div>

            {ticket.attachment_url && (
              <div>
                <h3 className="font-semibold mb-2">Attachment</h3>
                <a
                  href={ticket.attachment_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline flex items-center gap-1"
                >
                  <Paperclip className="h-4 w-4" />
                  View Attachment
                </a>
              </div>
            )}

            <div className="grid grid-cols-2 gap-4 pt-4 border-t">
              <div>
                <p className="text-sm text-muted-foreground">Category</p>
                <p className="font-medium">{ticket.category.replace('_', ' ')}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Student</p>
                <p className="font-medium">{ticket.student_name}</p>
              </div>
              {ticket.project_title && (
                <div>
                  <p className="text-sm text-muted-foreground">Related Project</p>
                  <p className="font-medium">{ticket.project_title}</p>
                </div>
              )}
              {ticket.resolved_at && (
                <div>
                  <p className="text-sm text-muted-foreground">Resolved At</p>
                  <p className="font-medium">{new Date(ticket.resolved_at).toLocaleString()}</p>
                </div>
              )}
            </div>

            {/* Status Update */}
            {!isResolved && (
              <div className="pt-4 border-t">
                <Label htmlFor="status">Update Status</Label>
                <Select
                  value={ticket.status}
                  onValueChange={handleUpdateStatus}
                  disabled={updating}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="OPEN">Open</SelectItem>
                    <SelectItem value="IN_PROGRESS">In Progress</SelectItem>
                    <SelectItem value="WAITING_STUDENT">Waiting for Student</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Messages */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Conversation</CardTitle>
          <CardDescription>
            {ticket.messages?.length || 0} {ticket.messages?.length === 1 ? 'message' : 'messages'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {ticket.messages && ticket.messages.length > 0 ? (
              ticket.messages.map((msg: any) => (
                <div
                  key={msg.id}
                  className={`p-4 rounded-lg ${
                    msg.sender_role === 'student'
                      ? 'bg-blue-50 ml-8'
                      : 'bg-gray-50 mr-8'
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <User className="h-4 w-4" />
                      <span className="font-semibold">{msg.sender_name}</span>
                      <Badge variant="outline" className="text-xs">
                        {msg.sender_role}
                      </Badge>
                    </div>
                    <span className="text-xs text-muted-foreground flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {new Date(msg.created_at).toLocaleString()}
                    </span>
                  </div>
                  <p className="text-sm whitespace-pre-wrap">{msg.message}</p>
                  {msg.attachment_url && (
                    <a
                      href={msg.attachment_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline text-sm flex items-center gap-1 mt-2"
                    >
                      <Paperclip className="h-3 w-3" />
                      View Attachment
                    </a>
                  )}
                </div>
              ))
            ) : (
              <p className="text-center text-muted-foreground py-8">
                No messages yet. Be the first to respond!
              </p>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Reply Form */}
      {!isResolved && (
        <Card>
          <CardHeader>
            <CardTitle>Add Reply</CardTitle>
            <CardDescription>Respond to the student</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSendMessage} className="space-y-4">
              <div>
                <Label htmlFor="message">Message *</Label>
                <Textarea
                  id="message"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Type your response here..."
                  rows={4}
                  required
                />
              </div>

              <div>
                <Label htmlFor="attachment">Attachment URL (Optional)</Label>
                <Input
                  id="attachment"
                  type="url"
                  value={attachmentUrl}
                  onChange={(e) => setAttachmentUrl(e.target.value)}
                  placeholder="https://example.com/screenshot.png"
                />
              </div>

              <div className="flex gap-2">
                <Button type="submit" disabled={sending || !message.trim()}>
                  {sending ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Sending...
                    </>
                  ) : (
                    <>
                      <Send className="h-4 w-4 mr-2" />
                      Send Message
                    </>
                  )}
                </Button>

                <Button
                  type="button"
                  variant="outline"
                  onClick={handleResolveTicket}
                  disabled={resolving}
                >
                  {resolving ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Resolving...
                    </>
                  ) : (
                    <>
                      <CheckCircle className="h-4 w-4 mr-2" />
                      Resolve & Send
                    </>
                  )}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
