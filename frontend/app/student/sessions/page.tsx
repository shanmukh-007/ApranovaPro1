'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Session {
  id: number;
  title: string;
  description: string;
  trainer_name: string;
  session_type: string;
  status: string;
  scheduled_at: string;
  duration_minutes: number;
  meet_link: string;
  is_upcoming: boolean;
}

export default function StudentSessionsPage() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'upcoming' | 'past'>('upcoming');

  useEffect(() => {
    fetchSessions();
  }, [filter]);

  const fetchSessions = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const url = filter === 'upcoming' 
        ? `${API_URL}/api/sessions/upcoming/`
        : `${API_URL}/api/sessions/past/`;

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

  const handleJoinSession = async (sessionId: number, meetLink: string) => {
    try {
      const token = localStorage.getItem('access_token');
      await axios.post(
        `${API_URL}/api/sessions/${sessionId}/join_session/`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      // Open Google Meet in new tab
      window.open(meetLink, '_blank');
    } catch (error) {
      console.error('Error joining session:', error);
      alert('Failed to join session');
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

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'SCHEDULED': return 'bg-blue-100 text-blue-800';
      case 'IN_PROGRESS': return 'bg-green-100 text-green-800';
      case 'COMPLETED': return 'bg-gray-100 text-gray-800';
      case 'CANCELLED': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">My Live Sessions</h1>
        <p className="text-gray-600">Join scheduled classes with your trainer</p>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-4 mb-6 border-b">
        <button
          onClick={() => setFilter('upcoming')}
          className={`pb-2 px-4 ${
            filter === 'upcoming'
              ? 'border-b-2 border-purple-600 text-purple-600 font-semibold'
              : 'text-gray-600'
          }`}
        >
          Upcoming Sessions
        </button>
        <button
          onClick={() => setFilter('past')}
          className={`pb-2 px-4 ${
            filter === 'past'
              ? 'border-b-2 border-purple-600 text-purple-600 font-semibold'
              : 'text-gray-600'
          }`}
        >
          Past Sessions
        </button>
      </div>

      {/* Sessions List */}
      {sessions.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <div className="text-6xl mb-4">📅</div>
          <p className="text-gray-600 text-lg mb-2">
            {filter === 'upcoming' ? 'No upcoming sessions' : 'No past sessions'}
          </p>
          <p className="text-gray-500 text-sm">
            Your trainer will schedule sessions for you
          </p>
        </div>
      ) : (
        <div className="grid gap-4">
          {sessions.map((session) => (
            <div
              key={session.id}
              className="bg-white border rounded-lg p-6 hover:shadow-lg transition"
            >
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-xl font-semibold text-gray-900">
                      {session.title}
                    </h3>
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(session.status)}`}>
                      {session.status}
                    </span>
                  </div>
                  
                  {session.description && (
                    <p className="text-gray-600 mb-3">{session.description}</p>
                  )}
                  
                  <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                    <div className="flex items-center gap-1">
                      <span>👨‍🏫</span>
                      <span>{session.trainer_name}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <span>📅</span>
                      <span>{formatDate(session.scheduled_at)}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <span>⏱️</span>
                      <span>{session.duration_minutes} min</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <span>📚</span>
                      <span>{session.session_type.replace('_', ' ')}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              {session.meet_link && session.status !== 'CANCELLED' && (
                <div className="flex gap-2 mt-4">
                  {session.is_upcoming && (
                    <button
                      onClick={() => handleJoinSession(session.id, session.meet_link)}
                      className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition flex items-center gap-2 font-semibold"
                    >
                      <span>📹</span>
                      Join Google Meet
                    </button>
                  )}
                  <a
                    href={session.meet_link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 transition flex items-center gap-2"
                  >
                    <span>🔗</span>
                    Copy Link
                  </a>
                </div>
              )}

              {session.status === 'CANCELLED' && (
                <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-red-800 text-sm">
                    ⚠️ This session has been cancelled. Your trainer will reschedule.
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
