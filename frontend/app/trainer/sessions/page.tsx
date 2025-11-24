'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import { Video, Calendar, Clock, Users, Plus, RefreshCw } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Session {
  id: number;
  title: string;
  description: string;
  session_type: string;
  status: string;
  scheduled_at: string;
  duration_minutes: number;
  meet_link: string;
  student_count: number;
  is_upcoming: boolean;
}

export default function TrainerSessionsPage() {
  const router = useRouter();
  const [sessions, setSessions] = useState<Session[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'upcoming' | 'past' | 'all'>('upcoming');

  useEffect(() => {
    fetchSessions();
  }, [filter]);

  const fetchSessions = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      let url = `${API_URL}/api/sessions/`;
      
      if (filter === 'upcoming') {
        url += 'upcoming/';
      } else if (filter === 'past') {
        url += 'past/';
      }

      const response = await axios.get(url, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setSessions(response.data);
    } catch (error) {
      console.error('Error fetching sessions:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusBadge = (status: string) => {
    const styles = {
      'SCHEDULED': 'bg-blue-500/10 text-blue-400 border-blue-500/20',
      'IN_PROGRESS': 'bg-green-500/10 text-green-400 border-green-500/20',
      'COMPLETED': 'bg-gray-500/10 text-gray-400 border-gray-500/20',
      'CANCELLED': 'bg-red-500/10 text-red-400 border-red-500/20',
    };
    return styles[status as keyof typeof styles] || styles.SCHEDULED;
  };

  return (
    <div className="min-h-screen bg-background p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-foreground mb-2">Live Sessions</h1>
          <p className="text-muted-foreground">Schedule and manage your class sessions</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={fetchSessions}
            className="px-4 py-2 rounded-lg border border-border bg-card hover:bg-accent transition-colors flex items-center gap-2"
          >
            <RefreshCw className="h-4 w-4" />
            Refresh
          </button>
          <button
            onClick={() => router.push('/trainer/sessions/create')}
            className="px-6 py-2 rounded-lg bg-purple-600 hover:bg-purple-700 text-white transition-colors flex items-center gap-2 font-semibold"
          >
            <Plus className="h-5 w-5" />
            Schedule New Session
          </button>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2 mb-6 border-b border-border">
        {[
          { key: 'upcoming', label: 'Upcoming' },
          { key: 'past', label: 'Past' },
          { key: 'all', label: 'All' }
        ].map((tab) => (
          <button
            key={tab.key}
            onClick={() => setFilter(tab.key as any)}
            className={`px-4 py-2 font-medium transition-colors relative ${
              filter === tab.key
                ? 'text-purple-400'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            {tab.label}
            {filter === tab.key && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-purple-500" />
            )}
          </button>
        ))}
      </div>

      {/* Loading State */}
      {loading ? (
        <div className="flex justify-center items-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
        </div>
      ) : sessions.length === 0 ? (
        /* Empty State */
        <div className="text-center py-20">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-purple-500/10 mb-4">
            <Video className="h-8 w-8 text-purple-400" />
          </div>
          <h3 className="text-xl font-semibold text-foreground mb-2">No sessions found</h3>
          <p className="text-muted-foreground mb-6">
            {filter === 'upcoming' ? "You haven't scheduled any upcoming sessions yet" : "No sessions in this category"}
          </p>
          <button
            onClick={() => router.push('/trainer/sessions/create')}
            className="px-6 py-2 rounded-lg bg-purple-600 hover:bg-purple-700 text-white transition-colors inline-flex items-center gap-2"
          >
            <Plus className="h-5 w-5" />
            Schedule Your First Session
          </button>
        </div>
      ) : (
        /* Sessions Grid */
        <div className="grid gap-4">
          {sessions.map((session) => (
            <div
              key={session.id}
              className="bg-card border border-border rounded-lg p-6 hover:border-purple-500/50 transition-all cursor-pointer group"
              onClick={() => router.push(`/trainer/sessions/${session.id}`)}
            >
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-xl font-semibold text-foreground group-hover:text-purple-400 transition-colors">
                      {session.title}
                    </h3>
                    <span className={`px-2.5 py-1 rounded-md text-xs font-medium border ${getStatusBadge(session.status)}`}>
                      {session.status}
                    </span>
                  </div>
                  {session.description && (
                    <p className="text-muted-foreground mb-4">{session.description}</p>
                  )}
                  <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                    <div className="flex items-center gap-2">
                      <Calendar className="h-4 w-4" />
                      <span>{formatDate(session.scheduled_at)}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Clock className="h-4 w-4" />
                      <span>{session.duration_minutes} min</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Users className="h-4 w-4" />
                      <span>{session.student_count} students</span>
                    </div>
                    <div className="flex items-center gap-2 px-2 py-1 rounded-md bg-purple-500/10 text-purple-400">
                      <span className="text-xs font-medium">{session.session_type.replace('_', ' ')}</span>
                    </div>
                  </div>
                </div>
              </div>

              {session.meet_link && (
                <div className="flex gap-2 pt-4 border-t border-border">
                  <a
                    href={session.meet_link}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={(e) => e.stopPropagation()}
                    className="px-4 py-2 rounded-lg bg-green-600 hover:bg-green-700 text-white transition-colors flex items-center gap-2 font-medium"
                  >
                    <Video className="h-4 w-4" />
                    Join Google Meet
                  </a>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      navigator.clipboard.writeText(session.meet_link);
                      alert('Link copied!');
                    }}
                    className="px-4 py-2 rounded-lg border border-border hover:bg-accent transition-colors text-sm"
                  >
                    Copy Link
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
