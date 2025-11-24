'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { MessageCircle, Clock, User, Loader2, AlertCircle } from 'lucide-react'
import apiClient from '@/lib/apiClient'

export default function TrainerSupportPage() {
  const router = useRouter()
  const [allTickets, setAllTickets] = useState([])
  const [myTickets, setMyTickets] = useState([])
  const [stats, setStats] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('my-tickets')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [allResponse, myResponse, statsResponse] = await Promise.all([
        apiClient.get('/support/tickets/'),
        apiClient.get('/support/tickets/assigned_to_me/'),
        apiClient.get('/support/tickets/stats/')
      ])

      setAllTickets(allResponse.data)
      setMyTickets(myResponse.data)
      setStats(statsResponse.data)
    } catch (err) {
      console.error('Error fetching tickets:', err)
    } finally {
      setLoading(false)
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

  const renderTicketCard = (ticket: any) => (
    <Card
      key={ticket.id}
      className="cursor-pointer hover:shadow-md transition-shadow"
      onClick={() => router.push(`/trainer/support/${ticket.id}`)}
    >
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
              <User className="h-4 w-4" />
              {ticket.student_name}
            </span>
            <span className="flex items-center gap-1">
              <Clock className="h-4 w-4" />
              {new Date(ticket.created_at).toLocaleDateString()}
            </span>
            {ticket.message_count > 0 && (
              <span className="flex items-center gap-1">
                <MessageCircle className="h-4 w-4" />
                {ticket.message_count}
              </span>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  )

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    )
  }

  return (
    <div className="container mx-auto p-6 max-w-7xl">
      <div className="mb-6">
        <h1 className="text-3xl font-bold">Support Tickets</h1>
        <p className="text-muted-foreground">Manage student support requests</p>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Total</CardDescription>
              <CardTitle className="text-3xl">{stats.total}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Open</CardDescription>
              <CardTitle className="text-3xl text-blue-600">{stats.open}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>In Progress</CardDescription>
              <CardTitle className="text-3xl text-yellow-600">{stats.in_progress}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Waiting</CardDescription>
              <CardTitle className="text-3xl text-purple-600">{stats.waiting_student}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardDescription>Resolved</CardDescription>
              <CardTitle className="text-3xl text-green-600">{stats.resolved}</CardTitle>
            </CardHeader>
          </Card>
        </div>
      )}

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="mb-4">
          <TabsTrigger value="my-tickets">
            My Tickets ({myTickets.length})
          </TabsTrigger>
          <TabsTrigger value="all-tickets">
            All Tickets ({allTickets.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="my-tickets" className="space-y-4">
          {myTickets.length === 0 ? (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <MessageCircle className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold mb-2">No tickets assigned</h3>
                <p className="text-muted-foreground text-center">
                  You don't have any tickets assigned to you yet
                </p>
              </CardContent>
            </Card>
          ) : (
            myTickets.map(renderTicketCard)
          )}
        </TabsContent>

        <TabsContent value="all-tickets" className="space-y-4">
          {allTickets.length === 0 ? (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <MessageCircle className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold mb-2">No tickets</h3>
                <p className="text-muted-foreground text-center">
                  No support tickets have been created yet
                </p>
              </CardContent>
            </Card>
          ) : (
            allTickets.map(renderTicketCard)
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}
